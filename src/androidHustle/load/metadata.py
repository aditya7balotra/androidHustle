from . import Tools
from tqdm import tqdm


class Metadata(Tools):
    """
    Loads the metadata
    """
    def __init__(self, conn):
        super().__init__(conn)

        
    def get_metadata(self):
        def dump_query(conn):
            f = conn.socket.makefile('r', encoding='utf-8')
            with open(self.conn.METADATA_DEFAULT_PATH, "w", encoding="utf-8") as out:
                for line in tqdm(f, desc= "metadata...", leave= False):
                    out.write(line)
                f.close()
            conn.close()

        def show_metadata():
            """
            will print some specific metadata
            """

            specifics= [
                # ["current user/ ", "echo $UID"],
                ["Model/ ", "getprop ro.product.model"],
                ["Manufacturer/ ", "getprop ro.product.manufacturer"],
                # ["Total storage/ ", "echo"],
                # ["Available storage/ ", "echo"],
                ["Battery percentage/", "dumpsys battery | grep level"],
                ["Screen resolution/ ", "wm size"],
                ["Android version/ ","getprop ro.build.version.release"],
                ["SDK/ ", "getprop ro.build.version.sdk"],
                ["cpu arch/ ", "getprop ro.product.cpu.abi"],
                
                ]
            print("### METADATA")

            for i in specifics:
                print(
                    i[0],
                    self.device.shell(f"{i[1]}").strip()
                    )
            print("###\n\n")


        self.device.shell("getprop", handler= dump_query)
        show_metadata()

