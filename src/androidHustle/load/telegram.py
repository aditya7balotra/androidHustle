from ..utils import check_package
from . import _android
from . import Tools
import os
from tqdm import tqdm


class Telegram(Tools):

    def __init__(self, conn):
        super().__init__(conn)

        
    def get_data(self, dtype):
        """
        Loads the respective dtype from the adb device's whatsapp

        Paramas:
            dtype: list either of ["cache", "aud", "vid", "file", "docs", "img"]
        """
        if not check_package("org.telegram.messenger", self.device):
            print("can't find telegram")
            return
        
        options= ["cache", "aud", "vid", "file", "docs", "img"]
        if not all(dt in options for dt in dtype):
            # incase of invalid dtype
            raise ValueError(
                'Must be in ["cache", "aud", "vid", "file", "docs", "img"]'
            )

        if not os.path.exists(os.path.join(self.conn.DIRECTORY_PATH, "telegram")):
            os.mkdir(os.path.join(self.conn.DIRECTORY_PATH, "telegram"))
        

        srcPath= [
            _android.TELEGRAM_CACHE_DEFAULT_PATH_ON_ANDROID,
            _android.TELEGRAM_AUDIO_DEFAULT_PATH_ON_ANDROID,
            _android.TELEGRAM_VIDEO_DEFAULT_PATH_ON_ANDROID,
            _android.TELEGRAM_FILES_DEFAULT_PATH_ON_ANDROID,
            _android.TELEGRAM_DOCUMENTS_DEFAULT_PATH_ON_ANDROID,
            _android.TELEGRAM_IMAGES_DEFAULT_PATH_ON_ANDROID
        ]

        destPath= [
            self.conn.TELEGRAM_DESTINATION__CACHE_DEFAULT_PATH,
            self.conn.TELEGRAM_DESTINATION__AUDIO_DEFAULT_PATH,
            self.conn.TELEGRAM_DESTINATION__VIDEO_DEFAULT_PATH,
            self.conn.TELEGRAM_DESTINATION__FILES_DEFAULT_PATH,
            self.conn.TELEGRAM_DESTINATION__DOCUMENTS_DEFAULT_PATH,
            self.conn.TELEGRAM_DESTINATION_IMAGES_DEFAULT_PATH
        ]

        
        # get the index of each element in dtype
        ind= [options.index(elm) for elm in dtype]
        
        for elm in ind:
            # ensruring the path
            os.mkdir(destPath[elm])

            # get files path
            res= self.device.shell(f'ls -1 "{srcPath[elm]}"')
            if 'no such file' in res.lower():
                # case of wrong source path
                raise ValueError(res)
            
            res= res.splitlines()
            for file in tqdm(res, desc= f"telegram {options[elm]}...", leave= False):
                # pull the files
                self.device.pull(f"{srcPath[elm]}/{file}", os.path.join(destPath[elm], file))