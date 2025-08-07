from ._android import *
import os, shutil

class ConfigBuilder:
    """
    Handles the dynamic configuration setup
    """
    def __init__(self, fname):
        self._generate_config(fname)
        self._clean()
    
    def _generate_config(self, fname):
        """
        Params:
            fname: folder name
        """
        self.DIRECTORY_PATH = os.path.join(os.getcwd(), fname)

        self.METADATA_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "metadata.txt")

        self.WHATSAPP_DESTINATION_IMAGES_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "whatsapp", "image")
        self.WHATSAPP_DESTINATION_AUDIO_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "whatsapp", "audio")
        self.WHATSAPP_DESTINATION_VIDEO_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "whatsapp", "video")
        self.WHATSAPP_DESTINATION_VIDEO_NOTES_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "whatsapp", "videoNote")
        self.WHATSAPP_DESTINATION_VOICE_NOTES_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "whatsapp", "voiceNote")
        self.WHATSAPP_DESTINATION_DOCUMENTS_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "whatsapp", "documents")

        self.CONTACTS_RAW_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "contacts", "raw_contacts.txt")
        self.SAVE_CONTACTS_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "contacts", "saved_contacts.json")

        self.CALL_LOG_RAW_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "logs", "raw_call_logs.txt")
        self.CALL_LOG_SAVE_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "logs", "save_call_logs.json")

        self.SMS_LOG_RAW_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "logs", "raw_sms_logs.txt")
        self.SMS_LOG_SAVE_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "logs", "saved_sms_logs.json")

        self.TELEGRAM_DESTINATION__CACHE_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "telegram", "cache")
        self.TELEGRAM_DESTINATION_IMAGES_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "telegram", "images")
        self.TELEGRAM_DESTINATION__DOCUMENTS_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "telegram", "documents")
        self.TELEGRAM_DESTINATION__FILES_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "telegram", "files")
        self.TELEGRAM_DESTINATION__AUDIO_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "telegram", "audio")
        self.TELEGRAM_DESTINATION__VIDEO_DEFAULT_PATH = os.path.join(self.DIRECTORY_PATH, "telegram", "video")

    def _clean(self):
        """
        cleaning
        """
        try:
            shutil.rmtree(self.DIRECTORY_PATH)
        except FileNotFoundError:
            pass
        os.mkdir(self.DIRECTORY_PATH)



