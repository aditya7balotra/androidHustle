from . import Tools
from ..utils import split_line
from tqdm import tqdm
import os

class DeviceMedia(Tools):
    def __init__(self, conn):
        super().__init__(conn)

        
    def get_device_data(self, dtype):
        """
        Loads the given dtype from the adb device
        Params: 
            dtype: list either of ["vid", "aud", "file", "img"]
        """
        options= ["vid", "aud", "file", "img"]
        if not all(dt in options for dt in dtype):
            # incase of invalid dtype
            raise ValueError(
                'Must be in ["vid", "aud", "file", "img"]'
            )
        
        if not os.path.exists(os.path.join(self.conn.DIRECTORY_PATH, "device")):
            os.mkdir(os.path.join(self.conn.DIRECTORY_PATH, "device"))

        
        def dump_query(conn):
            f = conn.socket.makefile('r', encoding='utf-8')
            lineChunk= ""
            for ind, line in enumerate(f):
                if line.startswith("Row:") and ind != 0:
                    # ensuring each lineChunk is a complete single raw data entity
                    make_dict(lineChunk)
                    lineChunk = line
                else:
                    lineChunk += line
            # ensures the last lineChunk data
            make_dict(lineChunk)
            f.close()
            conn.close()
        




        def make_dict(line):
            """
            takes each raw data as python string
            processes it to append the data in the dtypePaths list
            """

            nonlocal dtypePaths
            
            for i in split_line(line):          # changed
                j= i.split('=')
                path= None
                if len(j) != 1:
                    a, b= j[0].strip(), j[1].strip()
                    
                    if a == "_data":
                        path = b
                        break

                
            dtypePaths.append(path)

        # respective dtype uri table
        baseUri= "content://media/external"
        queryUri= {
            "vid": f"{baseUri}/video/media",
            "aud": f"{baseUri}/audio/media",
            "file": f"{baseUri}/file",
            "img": f"{baseUri}/images/media"
        }
        
        for elm in dtype:
            # list of paths respective to a particular dtype element
            dtypePaths= []

            # query the respective media content table
            self.device.shell(f"content query --uri {queryUri[elm]}", handler= dump_query)
            destPath= os.path.join(self.conn.DIRECTORY_PATH, "device", elm)
            os.mkdir(destPath)

            for i in tqdm(dtypePaths, desc= f"device {elm}...", leave= False):
                if i!= None:
                    # pull file
                    self.device.pull(i, os.path.join(destPath, i.split('/')[-1]))





