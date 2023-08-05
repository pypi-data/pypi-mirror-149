from enum import Enum
from selve.communication import Command

from selve.protocol import MethodCall, ServiceState
from selve.protocol import ParameterType
from selve.protocol import DeviceType
from selve.protocol import CommandType
from selve.commands import Commands, CommeoCommandCommand, CommeoDeviceCommand, CommeoEventCommand, CommeoGroupCommand, CommeoParamCommand, CommeoSenSimCommand, CommeoSenderCommand, CommeoSensorCommand, CommeoServiceCommand
from selve.utils import singlemask
from selve.utils import true_in_list
from selve.utils import b64bytes_to_bitlist
import logging



_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

#######################
## Device Definition ##
#######################

