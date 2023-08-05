from enum import Enum

class CommeoServiceCommand(Enum):
    PING = "service.ping"
    GETSTATE = "service.getState"
    GETVERSION = "service.getVersion"
    RESET = "service.reset"
    FACTORYRESET = "service.factoryReset"
    SETLED = "service.setLED"
    GETLED = "service.getLED"
    
class CommeoParamCommand(Enum):
    SETFORWARD = "param.setForward"
    GETFORWARD = "param.getForward"
    SETEVENT = "param.setEvent"
    GETEVENT = "param.getEvent"
    GETDUTY = "param.getDuty"
    GETRF = "param.getRF"

class CommeoDeviceCommand(Enum):
    SCANSTART = "device.scanStart"
    SCANSTOP = "device.scanStop"
    SCANRESULT = "device.scanResult"
    SAVE = "device.save"
    GETIDS = "device.getIDs"
    GETINFO = "device.getInfo"
    GETVALUES = "device.getValues"
    SETFUNCTION = "device.setFunction"
    SETLABEL = "device.setLabel"
    SETTYPE = "device.setType"
    DELETE = "device.delete"
    WRITEMANUAL = "device.writeManual"
    
class CommeoSensorCommand(Enum):
    TEACHSTART = "sensor.teachStart"
    TEACHSTOP = "sensor.teachStop"
    TEACHRESULT = "sensor.teachResult"
    GETIDS = "sensor.getIDs"
    GETINFO = "sensor.getInfo"
    GETVALUES = "sensor.getValues"
    SETLABEL = "sensor.setLabel"
    DELETE = "sensor.delete"
    WRITEMANUAL = "sensor.writeManual"

class CommeoSenSimCommand(Enum):
    STORE = "senSim.store"
    DELETE = "senSim.delete"
    GETCONFIG = "senSim.getConfig"
    SETCONFIG = "senSim.setConfig"
    SETLABEL = "senSim.setLabel"
    SETVALUES = "senSim.setValues"
    GETVALUES = "senSim.getValues"
    GETIDS = "senSim.getIDs"
    FACTORY = "senSim.factory"
    DRIVE = "senSim.drive"
    SETTEST = "senSim.setTest"
    GETTEST = "senSim.getTest"
    
class CommeoSenderCommand(Enum):
    TEACHSTART = "sender.teachStart"
    TEACHSTOP = "sender.teachStop"
    TEACHRESULT = "sender.teachResult"
    GETIDS = "sender.getIDs"
    GETINFO = "sender.getInfo"
    GETVALUES = "sender.getValues"
    SETLABEL = "sender.setLabel"
    DELETE = "sender.delete"
    WRITEMANUAL = "sender.writeManual"

class CommeoGroupCommand(Enum):
    READ = "group.read"
    WRITE = "group.write"
    GETIDS = "group.getIDs"
    DELETE = "group.delete"

class CommeoCommandCommand(Enum):
    DEVICE = "command.device"
    GROUP = "command.group"
    GROUPMAN = "command.groupMan"
    RESULT = "command.result"
    
class CommeoEventCommand(Enum):
    DEVICE = "event.device"
    SENSOR = "event.sensor"
    SENDER = "event.sender"
    LOG = "event.log"
    DUTYCYCLE = "event.dutyCycle"

class IveoCommand(Enum):
    FACTORY = "iveo.factory"
    SETCONFIG = "iveo.setConfig"
    GETCONFIG = "iveo.getConfig"
    GETIDS = "iveo.getIDs"
    SETREPEATER = "iveo.setRepeater"
    GETREPEATER = "iveo.getRepeater"
    SETLABEL = "iveo.setLabel"
    TEACH = "iveo.commandTeach"
    LEARN = "iveo.commandLearn"
    MANUAL = "iveo.commandManual"
    AUTOMATIC = "iveo.commandAutomatic"
    RESULT = "iveo.commandResult"
    

class Commands(Enum):
    SERVICE = CommeoServiceCommand   
    PARAM = CommeoParamCommand
    DEVICE = CommeoDeviceCommand
    SENSOR = CommeoSensorCommand
    SENSIM = CommeoSenSimCommand
    SENDER = CommeoSenderCommand
    GROUP = CommeoGroupCommand
    COMMAND = CommeoCommandCommand
    EVENT = CommeoEventCommand
    IVEO = IveoCommand