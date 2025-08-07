from ..configs import _android

class Tools():
    def __init__(self, conn):
        """
        Params:
            conn: connect.Connection object
        """
        self.conn= conn
        self.device= conn.device

        
from .call_logs import Call
from .contacts import Contacts
from .device_media import DeviceMedia
from .metadata import Metadata
from .sms_logs import Sms
from .telegram import Telegram
from .whatsapp import WhatsApp


