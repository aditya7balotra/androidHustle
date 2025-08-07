

import argparse
from .connect.connect import Connection
from .load import (   
    Contacts,
    Metadata,
    Call,
    Sms,
    DeviceMedia,
    Telegram,
    WhatsApp
)


DATA_CLASSES = {
    "whatsapp": {
        "names": ["-wha", "--whatsapp"],
        "func": WhatsApp,
        "options": ["img", "aud", "docs", "vnotes", "vidnotes", "vid"],
        "method": lambda toolObj: toolObj.get_data
    },
    "telegram": {
        "names": ["-tel", "--telegram"],
        "func": Telegram,
        "options": ["cache", "aud", "vid", "file", "docs", "img"],
        "method": lambda toolObj: toolObj.get_data
    },
    "device": {
        "names": ["-dev", "--device"],
        "func": DeviceMedia,
        "options": ["vid", "aud", "file", "img"],
        "method": lambda toolObj: toolObj.get_device_data
    },
    "calllog": {
        "names": ["-clog", "--calllog"],
        "func": Call,
        "options": None,
        "method": lambda toolObj: toolObj.get_call_logs
    },
    "msglog": {
        "names": ["-mlog", "--msglog"],
        "func": Sms,
        "options": None,
        "method": lambda toolObj: toolObj.get_sms_logs
    },
    "contact": {
        "names": ["-cont", "--contact"],
        "func": Contacts,
        "options": None,
        "method": lambda toolObj: toolObj.get_contacts
    },
    "metadata": {
        "names": ["-met", "--metadata"],
        "func": Metadata,
        "options": None,
        "method": lambda toolObj: toolObj.get_metadata
    }
}

def cli():
    
    
    parser = argparse.ArgumentParser()

    for i in DATA_CLASSES.keys():
        if DATA_CLASSES[i]["options"]:
            parser.add_argument(
                *DATA_CLASSES[i]["names"],
                choices= DATA_CLASSES[i]["options"],
                nargs="*"
            )
        else:
            parser.add_argument(
                *DATA_CLASSES[i]["names"],
                action= "store_true"
            )

    parser.add_argument(
        "--index-dev",
        "-ind",
        default= 0,
        help= "index of the adb device",
        type= int
    )

    parser.add_argument(
        "--list-devices",
        "-ldevs",
        action= "store_true",
        help= "list the available adb devices"
    )
    

    args= parser.parse_args()
    if args.list_devices:
        given_args = [arg for arg in vars(args) if getattr(args, arg) not in [None, False] and arg != 'list_devices' and arg != "index_dev"]
        if given_args:
            parser.error("--list-devices cannot be used with other options")
        else:
            conn= Connection()
            serials= conn.get_avl()
            print("List of devices")
            for i in range(len(serials)):
                print(f"[{i}] {serials[i]}")
            return
    conn= Connection()
    serials= conn.get_avl()
    
    try:
        conn.connect(serials[args.index_dev])
    except IndexError as e:
        parser.error("No device found")

    choices= vars(args)
    for tool in DATA_CLASSES:
        if choices[tool] not in [None, False]:
            toolObj= DATA_CLASSES[tool]["func"](conn)
            if DATA_CLASSES[tool]["options"]:
                # indicating options
                DATA_CLASSES[tool]["method"](toolObj)(choices[tool]) if len(choices[tool]) != 0 else DATA_CLASSES[tool]["method"](toolObj)(DATA_CLASSES[tool]["options"])
            else:
                DATA_CLASSES[tool]["method"](toolObj)()

    

if __name__ == "__main__":
    cli()