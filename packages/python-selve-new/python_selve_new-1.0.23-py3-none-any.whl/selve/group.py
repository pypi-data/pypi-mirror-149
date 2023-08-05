from selve.utils import *
from selve.communication import *
import logging
_LOGGER = logging.getLogger(__name__)

class Group():
    ## A group consists of multiple devices. We have to treat it like a device.

    def __init__(self, gateway, ID, communicationType, discover = False):
        self.ID = ID
        self.gateway = gateway
        self.mask = singlemask(ID)
        self.device_type = DeviceType.UNKNOWN ## Device type according to devices in group
        self.communicationType = communicationType
        self.name = "Not defined"
        if discover:
            self.discover_properties()
    
    def executeCommand(self, commandType, automatic = False):
        if automatic:
            command = CommeoDeviceCommand(self.mask, commandType)
        else:
            command = CommeoDeviceCommand(self.mask, commandType)
        command.execute(self.gateway)
        return command

    # def discover_properties(self):
    #     command = CommeoDeviceGetValues(self.ID)
    #     command.execute(self.gateway)
    #     self.device_type = command.deviceType
    #     self.name = command.name

    ## Actor ##


    ## Sensor ##


    ## SenSim ##


    ## Sender ##


    ## Iveo ##


    

    
    def __str__(self):
        return "Device " + self.device_type.name + " of type: " + self.communicationType + " on channel " + str(self.ID) + " with name " + self.name