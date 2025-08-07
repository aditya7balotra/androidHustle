from ppadb.client import Client as adbClient
from ..configs import ConfigBuilder


class Connection(ConfigBuilder):

    def __init__(self, host= "localhost", port= 5037, fname= "ahustleExtracts"):
        """
        Initialises connection with the abd client
        Args:
            host: host address
            port: port number
            fname: folder name, where to save the works
        """
        self.client= adbClient(host= host, port= port)
        self.device= None
        try:
            self.client.create_connection()
        except RuntimeError as e:
            raise

        super().__init__(fname)



    def connect(self, serial):
        """
        connect to the device using its serial number

        Args:
            serial: serial number of the device
        Return:
            device object of the given serial number
        """
        conn_device= self.client.device(serial)
        if not conn_device:
            raise ValueError(f"No device found with serial: {serial}")
        self.device= conn_device
        return conn_device

    def get_avl(self):
        """
        Will return the list of available adb device serial numbers.

        Return:
            list of available adb device serial numbers.
        """
        devices= self.client.devices()
        return [device.serial for device in devices]


if __name__ == "__main__":
    obj= Connection()
    obj.get_avl()