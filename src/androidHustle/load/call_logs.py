from . import Tools
from ..utils import split_line, validate_int
import os, json
from tqdm import tqdm
from datetime import datetime


class Call(Tools):
    def __init__(self, conn):
        super().__init__(conn)
        
    def get_call_logs(self):
        """
        will extract the call logs
        Saves two files:
            ./logs/raw_call_logs.txt -> raw call logs
            ./logs/save_call_logs.json -> processed call logs
        """
        data= {}
        ind= 0

        if not os.path.exists(os.path.join(self.conn.DIRECTORY_PATH, "logs")):
            os.mkdir(os.path.join(self.conn.DIRECTORY_PATH, 'logs'))

        def make_dict(line):
            """
            takes each log data as python string
            modifies the nonlocal data dictionary
            """

            # calltype code table
            callTypeCode= {
                1: "incoming",
                2: "outgoing",
                3: "missed calls",
                4: "voicemail",
                5: "rejected", 
                6: "blocked",
                7: "answered"
            }

            nonlocal data, ind

            # variables used
            num= None
            name= None
            duration= None
            countryIso= None
            geoCodedLoc= None
            via= None
            date= None
            callType= None
            
            for i in split_line(line):
                j= i.split('=')
                if len(j) != 1:
                    a, b= j[0].strip(), j[1].strip()
                    if a == "number":
                        num = b
                    elif a == "name":
                        name = b
                    elif a == "date":
                        date = b
                    elif a == "geocoded_location":
                        geoCodedLoc = b
                    elif a == "phone_account_address":
                        via = b
                    elif a == "countryiso":
                        countryIso = b
                    elif a == "duration":
                        duration = b
                    elif a == "type":
                        callType = b            
                
            data[ind]= {
                "name": name,
                "number": num,
                "date": datetime.fromtimestamp(int(date) // 1000).strftime("%Y-%m-%d %H") if validate_int(date) else None,
                "duration": int(duration)/60 if validate_int(duration) else None, 
                "geocoded_location": geoCodedLoc,
                "via": via,
                "country_iso": countryIso,
                "call_type": callTypeCode[int(callType)] if validate_int(callType) else None
            }
            ind += 1
                    

        def dump_query(conn):
            f = conn.socket.makefile('r', encoding='utf-8')
            lineChunk= ""
            with open(self.conn.CALL_LOG_RAW_DEFAULT_PATH, "w", encoding="utf-8") as out:
                for ind, line in enumerate(tqdm(f, desc= "call logs...", leave= False)):
                    if line.startswith("Row:") and ind != 0:
                        # ensuring each lineChunk is a complete single raw data entity
                        make_dict(lineChunk)
                        lineChunk = line
                    else:
                        lineChunk += line
                    out.write(line)
                # ensures the last lineChunk data
                make_dict(line)
                f.close()
            conn.close()

        # query the call content table
        self.device.shell("content query --uri content://call_log/calls", handler= dump_query)

        with open(self.conn.CALL_LOG_SAVE_DEFAULT_PATH, "w") as file:
            # save data
            json.dump(data, file, indent= 4)
        