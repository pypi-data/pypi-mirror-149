from selve.protocol import DayMode, DeviceType, DutyMode, LogType, MethodCall, MovementState, ParameterType, SensorState, lightDigital, process_response, rainDigital, senderEvents, tempDigital, windDigital
from selve.utils import *
import logging

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

## Commands ##

class Command(MethodCall):

    def __init__(self, method_name, parameters = []):
         super().__init__("selve.GW." + method_name.value, parameters)

class CommandSingle(Command):

    def __init__(self, method_name, iveoID):
        super().__init__(method_name, [(ParameterType.INT, iveoID)])

class CommandMask(Command):

    def __init__(self, method_name, mask, command):
        super().__init__(method_name, [(ParameterType.BASE64, mask), (ParameterType.INT, command.value)])


## Events ##

# Handling all Events

def incomingEvent(value:str):
    parameters = process_response(value)
    methodName = parameters[0][1]
    output = []
    if(methodName == "selve.GW.event.device"):
        output.name = parameters[0][1]
        output.movementState = MovementState(int(parameters[2][1]))
        output.value = valueToPercentage(int(parameters[3][1]))
        output.targetValue = valueToPercentage(int(parameters[4][1]))

        bArr = intToBoolarray(int(parameters[5][1]))
        output.unreachable = bArr[0]
        output.overload = bArr[1]
        output.obstructed = bArr[2]
        output.alarm = bArr[3]
        output.lostSensor = bArr[4]
        output.automaticMode = bArr[5]
        output.gatewayNotLearned = bArr[6]
        output.windAlarm = bArr[7]
        output.rainAlarm = bArr[8]
        output.freezingAlarm = bArr[9]
        
        output.dayMode = DayMode(int(parameters[6][1]))
        output.deviceType = DeviceType(int(parameters[7][1]))

    if(methodName == "selve.GW.event.sensor"):
        output.sensorId = int(parameters[0][1])
        output.windDigital = windDigital(int(parameters[1][1]))
        output.rainDigital = rainDigital(int(parameters[2][1]))
        output.tempDigital = tempDigital(int(parameters[3][1]))
        output.lightDigital = lightDigital(int(parameters[4][1]))
        output.sensorState = SensorState(int(parameters[5][1]))
        output.tempAnalog = int(parameters[6][1])
        output.windAnalog = int(parameters[7][1])
        output.sun1Analog = int(parameters[8][1])
        output.dayLightAnalog = int(parameters[9][1])
        output.sun2Analog = int(parameters[10][1])
        output.sun3Analog = int(parameters[11][1])

    if(methodName == "selve.GW.event.sender"):
        output.senderId = int(parameters[0][1])
        output.lastEvent = senderEvents(int(parameters[1][1]))

    if(methodName == "selve.GW.event.log"):
        output.logCode = str(parameters[0][1])
        output.logStamp = str(parameters[1][1])
        output.logValue = str(parameters[2][1])
        output.logDescription = str(parameters[3][1])
        output.logType = LogType(int(parameters[4][1]))
    
    if(methodName == "selve.GW.event.dutyCycle"):
        output.dutyMode = DutyMode(int(parameters[0][1]))
        output.rfTraffic = int(parameters[1][1])
        
    
    _LOGGER.debug("Received event " + methodName)
    output.methodName = methodName
    return output