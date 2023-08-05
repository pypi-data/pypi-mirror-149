import asyncio
from selve.communication import *
from selve.protocol import *
import logging
_LOGGER = logging.getLogger(__name__)

class Device():

    def __init__(self, gateway, ID, deviceType:DeviceType = DeviceType.UNKNOWN):
        self.ID = ID
        self.gateway = gateway
        self.mask = singlemask(ID)
        self.device_type = deviceType
        self.name = "Not defined"
        self.deviceClass = DeviceClass.UNKOWN
        self.communicationType = CommunicationType.UNKNOWN
    
    async def discover_properties(self):
        pass

    def __str__(self):
        return "Device " + self.device_type.name + " of type: " + self.communicationType.name + " on channel " + str(self.ID) + " with name " + self.name