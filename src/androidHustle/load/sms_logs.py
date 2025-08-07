from . import Tools
from ..utils import split_line, validate_int
from tqdm import tqdm
import os, json
from datetime import datetime

class Sms(Tools):

    def __init__(self, conn):
        super().__init__(conn)

        
    def get_sms_logs(self):
        """
        Load the sms logs
        Saves two files:
            ./logs/raw_sms_logs.txt -> raw sms logs
            ./logs/saved_sms_logs.json -> processed sms logs
        """

        def make_dict(line):
            """
            takes each log as python string
            modifies the nonlocal data dictionary
            """

            # smstype code table
            smsTypeCode= {
                1: "inbox",
                2: "sent",
                3: "draft",
                4: "outbox",
                5: "failed", 
                6: "queued",
            }

            nonlocal data, ind
            adrs= None
            date= None
            dateSent= None
            msgType= None
            subj= None
            body= None
            service_center= None
            
            for i in split_line(line):
                j= i.split('=')
                if len(j) != 1:
                    a, b= j[0].strip(), j[1].strip()
                    if a == "address":
                        adrs = b
                    elif a == "date":
                        date = b
                    elif a == "date_sent":
                        dateSent = b
                    elif a == "type":
                        msgType = b
                    elif a == "subject":
                        subj = b
                    elif a == "body":
                        body = b
                    elif a == "service_center":
                        service_center = b

            data[ind]= {
                "adrs": adrs,
                "date": datetime.fromtimestamp(int(date) // 1000).strftime("%Y-%m-%d %H") if validate_int(date) else None,
                "date_sent": datetime.fromtimestamp(int(dateSent) // 1000).strftime("%Y-%m-%d %H") if validate_int(dateSent) else None,
                "msg_type": smsTypeCode[int(msgType)] if validate_int(msgType) else None,
                "subject": subj,
                "body": body,
                "service_center": service_center
            }
            ind += 1
                    

        def dump_query(conn):
            f = conn.socket.makefile('r', encoding='utf-8')
            lineChunk= ""
            with open(self.conn.SMS_LOG_RAW_DEFAULT_PATH, "w", encoding="utf-8") as out:
                for ind, line in enumerate(tqdm(f, desc= "sms logs...", leave= False)):
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
        ind= 0

        if not os.path.exists(os.path.join(self.conn.DIRECTORY_PATH, "logs")):
            os.mkdir(os.path.join(self.conn.DIRECTORY_PATH, "logs"))

        # query the sms content table
        self.device.shell("content query --uri content://sms/", handler= dump_query)

        with open(self.conn.SMS_LOG_SAVE_DEFAULT_PATH, "w", encoding= "utf-8") as file:
            json.dump(data, file, indent= 4)
        