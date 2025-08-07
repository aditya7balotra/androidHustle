from . import _android
from . import Tools
from ..utils import check_package
from tqdm import tqdm
import os


class WhatsApp(Tools):

    def __init__(self, conn):
        super().__init__(conn)


    def get_data(self, dtype):
        """
        Loads the respective dtype from the adb device's whatsapp

        Params:
            dtype: takes list containing either of 
                    ["img", "aud", "docs", "vnotes", "vidnotes", "vid"]
        """
        if not check_package("com.whatsapp", self.device):
            print("can't find whatsapp")
            return

        options= ["img", "aud", "docs", "vnotes", "vidnotes", "vid"]

        if not all(dt in options for dt in dtype):
            # incase of invalid dtype
            raise ValueError(
                'Must be in ["img", "aud", "docs", "vnotes", "vidnotes", "vid"]'
            )
        
        if not os.path.exists(os.path.join(self.conn.DIRECTORY_PATH, "whatsapp")):
            os.mkdir(os.path.join(self.conn.DIRECTORY_PATH, "whatsapp"))
    
        srcPath= [
            _android.WHATSAPP_IMAGE_DEFAULT_PATH_ON_ANDROID,
            _android.WHATSAPP_AUDIO_DEFAULT_PATH_ON_ANDROID,
            _android.WHATSAPP_DOCUMENTS_DEFAULT_PATH_ON_ANDROID,
            _android.WHATSAPP_VOICE_NOTES_DEFAULT_PATH_ON_ANDROID,
            _android.WHATSAPP_VIDEO_NOTES_DEFAULT_PATH_ON_ANDROID,
            _android.WHATSAPP_VIDEO_DEFAULT_PATH_ON_ANDROID
        ]

        destPath= [
            self.conn.WHATSAPP_DESTINATION_IMAGES_DEFAULT_PATH,
            self.conn.WHATSAPP_DESTINATION_AUDIO_DEFAULT_PATH,
            self.conn.WHATSAPP_DESTINATION_DOCUMENTS_DEFAULT_PATH,
            self.conn.WHATSAPP_DESTINATION_VOICE_NOTES_DEFAULT_PATH,
            self.conn.WHATSAPP_DESTINATION_VIDEO_NOTES_DEFAULT_PATH,
            self.conn.WHATSAPP_DESTINATION_VIDEO_DEFAULT_PATH
        ]

         # getting the index of each dtype element
        ind= [options.index(i) for i in dtype]
        
        for elm in ind:
            # creating the destination path
            os.mkdir(destPath[elm])
            # get the list of available files's/folder's path
            res= self.device.shell(f'ls -1 "{srcPath[elm]}"')

            if "no such file" in res.lower():
                # case of wrong path
                raise ValueError(res)
                
            
            if options[elm] in ["vnotes", "vidnotes"]:
                # getting the folder names inside
                for folder in tqdm(res.splitlines(), desc= f"whatsapp {options[elm]}...", leave= False):
                    # paths
                    newPath= os.path.join(destPath[elm], folder)
                    newSrcPath= f'{srcPath[elm]}/{folder}'
                    
                    # ensruing the directory
                    os.mkdir(newPath)

                    # getting the files inside the subfolder
                    res2= self.device.shell(f'ls -1 "{newSrcPath}"')

                    for i in res2.splitlines():
                        # extracting files
                        self.device.pull(f"{newSrcPath}/{i}", os.path.join(newPath, i))
            else:
                res= res.splitlines()

                for i in tqdm(res, desc= f"whatsapp {options[elm]}...", leave= False):
                    # pulling the files
                    self.device.pull(f'{srcPath[elm]}/{i}', os.path.join(destPath[elm], i))