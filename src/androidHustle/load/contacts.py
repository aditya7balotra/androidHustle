from . import Tools
from ..utils import split_line
from tqdm import tqdm
import json, os

class Contacts(Tools):
    def __init__(self, conn):
        super().__init__(conn)

        
    def get_contacts(self):
        """
        Loads the contacts form the adb device
        Saves two files:
            ./contacts/raw_contacts.txt => raw data
            ./contacts/saved_contacts.json => processed data
        """

        os.mkdir(os.path.join(self.conn.DIRECTORY_PATH, "contacts"))
        

        def make_dict(line):
            """
            takes each contact log data as a python string
            processes the input string to extract and save
            """

            nonlocal data

            if len(line) != 0:
                name, num= None, None
                for j in split_line(line):
                    a= j.split("=")
                
                    if a[0].strip() == "display_name":
                        name= a[1].strip()
                    elif a[0].strip() == "data4":
                        num= a[1].strip()

                    if num:
                        if num.lower() != "null":
                            data[num]= name


                
        def dump_query(conn):
            f = conn.socket.makefile('r', encoding='utf-8')
            lineChunk= ""
            with open(self.conn.CONTACTS_RAW_DEFAULT_PATH, "w", encoding="utf-8") as out:
                for ind, line in enumerate(tqdm(f, desc= "contacts...", leave= False)):
                    if line.startswith("Row:") and ind != 0:
                        # ensuring each lineChunk is a complete single raw data entity
                        make_dict(lineChunk)
                        lineChunk = line
                    else:
                        lineChunk += line
                    out.write(line)
                # ensures the last lineChunk data
                make_dict(lineChunk)
                f.close()
            conn.close()

        data= {}
        
        # query to the contact content table
        self.device.shell("content query --uri content://com.android.contacts/data/phones", handler=dump_query)

        # save the data
        with open(self.conn.SAVE_CONTACTS_DEFAULT_PATH, "w", encoding= "utf-8") as file:
                json.dump(data, file, indent= 4)
