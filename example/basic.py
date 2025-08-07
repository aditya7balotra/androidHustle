from androidHustle.connect import Connection
from androidHustle.load import (
    WhatsApp
    # Telegram,
    # Call,
    # Contacts,
    # Metadata,
    # DeviceMedia,
    # Sms   
)


conn= Connection(fname= "ahustleExtracts")
avl_devices= conn.get_avl()         #list of available devices serial no.
conn.connect(avl_devices[0])        # connect to the first device
whats= WhatsApp(conn)

whats.get_data(["img"])             # will load whatsapp images in fname