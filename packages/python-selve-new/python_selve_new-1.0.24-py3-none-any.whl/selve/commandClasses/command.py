from selve.utils import b64bytes_to_bitlist, true_in_list
import logging
from selve.protocol import DeviceCommandTypes, ParameterType
from selve.commands import CommeoCommandCommand
from selve.communication import Command
_LOGGER = logging.getLogger(__name__)


class CommeoCommandDevice(Command):
    def __init__(self, deviceId, command, commmandType = DeviceCommandTypes.MANUAL, parameter = 0):
        super().__init__(CommeoCommandCommand.DEVICE, [(ParameterType.INT, deviceId), (ParameterType.INT, command.value), (ParameterType.INT, commmandType.value), (ParameterType.INT, parameter)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoCommandGroup(Command):
    def __init__(self, deviceId, command, commmandType = DeviceCommandTypes.MANUAL, parameter = 0):
        super().__init__(CommeoCommandCommand.GROUP, [(ParameterType.INT, deviceId), (ParameterType.INT, command.value), (ParameterType.INT, commmandType.value), (ParameterType.INT, parameter)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoCommandGroupMan(Command):
    def __init__(self, command, commandType, deviceIdMask, parameter = 0):
        super().__init__(CommeoCommandCommand.GROUPMAN, [(ParameterType.INT, command.value), (ParameterType.INT, commandType.value), (ParameterType.BASE64, deviceIdMask), (ParameterType.INT, parameter)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)


