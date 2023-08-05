from selve.communication import Command
from selve.protocol import *
from selve.commands import *

class CommeoServicePing(Command):
    def __init__(self):
        super().__init__(CommeoServiceCommand.PING)

class CommeoServiceGetState(Command):
    def __init__(self):
        super().__init__(CommeoServiceCommand.GETSTATE)
        self.status = None
    
    def process_response(self, methodResponse):
        super().process_response(methodResponse)

        if(isinstance(methodResponse.parameters[0][1], int)):
            self.status = ServiceState(int(methodResponse.parameters[0][1]))
        else:
            self.status = methodResponse.parameters[0][1]


class CommeoServiceGetVersion(Command):
    def __init__(self):
        super().__init__(CommeoServiceCommand.GETVERSION)
    
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.serial = str(methodResponse.parameters[0][1])
        self.version = int(methodResponse.parameters[1][1]) + "." + int(methodResponse.parameters[2][1]) + "." + int(methodResponse.parameters[3][1]) + "." + int(methodResponse.parameters[6][1])
        self.spec = int(methodResponse.parameters[4][1]) + "." + int(methodResponse.parameters[5][1])
        

class CommeoServiceReset(Command):
    def __init__(self):
        super().__init__(CommeoServiceCommand.RESET)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])
    
class CommeoServiceFactoryReset(Command):
    def __init__(self):
        super().__init__(CommeoServiceCommand.FACTORYRESET)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])
    
class CommeoServiceSetLed(Command):
    def __init__(self, ledMode):
        super().__init__(CommeoServiceCommand.SETLED, [(ParameterType.INT, ledMode)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])
    
class CommeoServiceGetLed(Command):
    def __init__(self):
        super().__init__(CommeoServiceCommand.GETLED)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.ledmode = LEDMode(int(methodResponse.parameters[0][1]))
    
class CommeoParamSetForward(Command):
    def __init__(self, forwarding):
        super().__init__(CommeoParamCommand.SETFORWARD, [(ParameterType.INT, forwarding)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])
    
class CommeoParamGetForward(Command):
    def __init__(self):
        super().__init__(CommeoParamCommand.GETFORWARD)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.forwarding = Forwarding(int(methodResponse.parameters[0][1]))
    
class CommeoParamSetEvent(Command):
    def __init__(self, eventDevice, eventSensor, eventSender, eventLogging, eventDuty):
        super().__init__(CommeoParamCommand.SETEVENT, [(ParameterType.INT, eventDevice), (ParameterType.INT, eventSensor), (ParameterType.INT, eventSender), (ParameterType.INT, eventLogging), (ParameterType.INT, eventDuty)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])
    
class CommeoParamGetEvent(Command):
    def __init__(self):
        super().__init__(CommeoParamCommand.GETEVENT)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.eventDevice = bool(methodResponse.parameters[0][1])
        self.eventSensor = bool(methodResponse.parameters[1][1])
        self.eventSender = bool(methodResponse.parameters[2][1])
        self.eventLogging = bool(methodResponse.parameters[3][1])
        self.eventDuty = bool(methodResponse.parameters[4][1])
    
class CommeoParamGetDuty(Command):
    def __init__(self):
        super().__init__(CommeoParamCommand.GETDUTY)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.dutyMode = DutyMode(int(methodResponse.parameters[0][1]))
        self.rfTraffic = int(methodResponse.parameters[1][1])
    
class CommeoParamGetRF(Command):
    def __init__(self):
        super().__init__(CommeoParamCommand.GETRF)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.netAddress = int(methodResponse.parameters[0][1])
        self.resetCount = int(methodResponse.parameters[1][1])
        self.rfBaseId = int(methodResponse.parameters[2][1])
        self.sensorNetAddress = int(methodResponse.parameters[3][1])
        self.rfSensorId = int(methodResponse.parameters[4][1])
        self.iveoResetCount = int(methodResponse.parameters[5][1])
        self.rfIveoId = int(methodResponse.parameters[6][1])
    