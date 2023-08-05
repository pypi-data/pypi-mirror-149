from selve.commandClasses.command import CommeoCommandGroup
from selve.device import Device
from selve.protocol import CommandType, CommunicationType, DeviceClass, DeviceCommandTypes, ParameterType
from selve.utils import b64bytes_to_bitlist, true_in_list
import logging
from selve.commands import CommeoDeviceCommand, CommeoGroupCommand
from selve.communication import Command, CommandSingle
_LOGGER = logging.getLogger(__name__)


class CommeoGroupRead(CommandSingle):
    def __init__(self, groupId):
        super().__init__(CommeoGroupCommand.READ, groupId)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[1][1]))]
        _LOGGER.debug(self.ids)
        self.name = str(methodResponse.parameters[2][1])

class CommeoGroupWrite(Command):
    def __init__(self, groupId, actorIdMask, name):
        super().__init__(CommeoGroupCommand.WRITE, [(ParameterType.INT, groupId), (ParameterType.BASE64, actorIdMask), (ParameterType.STRING, name)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoGroupGetIDs(Command):
    def __init__(self):
        super().__init__(CommeoGroupCommand.GETIDS)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommeoGroupDelete(CommandSingle):
    def __init__(self, groupId):
        super().__init__(CommeoGroupCommand.DELETE, groupId)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])

class GroupDevice(Device):
    def __init__(self, gateway, id):
        super().__init__(gateway, id)
        self.communicationType = CommunicationType.COMMEO
        self.deviceClass = DeviceClass.GROUP

    def discover_properties(self):
        try:
            command = CommeoGroupRead(self.ID)
            command.execute(self.gateway)
            self.device_type = "GROUP"
            self.name = command.name
            self.deviceClass = DeviceClass.GROUP
            self.communicationType = CommunicationType.COMMEO
        except Exception as e1:
            _LOGGER.exception ("not : " + str(e1))


    def readGroup(self, id):
        command = CommeoGroupRead(id)
        command.execute(self.gateway)
        return command

    def writeGroup(self, id, idMask, name):
        command = CommeoGroupWrite(id, idMask, name)
        command.execute(self.gateway)

    def deleteGroup(self, id):
        command = CommeoGroupDelete(id)
        command.execute(self.gateway)

    def executeCommand(self, command, commandType = DeviceCommandTypes.MANUAL, parameter=0):
        command = CommeoCommandGroup(self.ID, command, commandType, parameter)
        command.execute(self.gateway)
        return command
    
    def stop(self, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.STOP, type)

    def moveDown(self, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.DRIVEDOWN, type)
    
    def moveUp(self, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.DRIVEUP, type)
    
    def moveIntermediatePosition1(self, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.DRIVEPOS1, type)

    def moveIntermediatePosition2(self, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.DRIVEPOS2, type)
    
    def driveToPos(self, position, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.DRIVEPOS, type, position)

    def stepUp(self, degrees, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.STEPUP, type, degrees)

    def stepDown(self, degrees, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        self.executeCommand(CommandType.STEPDOWN, type, degrees)

    def setAutomatic(self, autoOn, forced=False):
        if forced:
            type=DeviceCommandTypes.FORCED
        else:
            type=DeviceCommandTypes.MANUAL

        if autoOn:
            self.executeCommand(CommandType.AUTOON, type)
        else:
            self.executeCommand(CommandType.AUTOOFF, type)
