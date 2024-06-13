
__app__ = "pyHomie"
__version__ = "0.0.4"
__date__= "2024/06/11"

import re
import sys
import yaml
import json
import logging


from jsonschema import validate
from jsonschema.exceptions import ValidationError

from pyHomie import homieSchema
from pyHomie import properties, device, node, mqttClient, watchdog


class pyHomie(object):
    def __init__(self,logger='pyHomie')-> None:

        _libName = str(__name__.rsplit('.', 1)[-1])
        self._logHandler = logger + '.' + _libName
        self._log = logging.getLogger(self._logHandler + '.' + self.__class__.__name__)

        self._log.info('Start %s, %s' % (__app__, __version__))

        self.mqttClient = mqttClient.mqttClient(logger)

        #simulate mqtt
       # self.mqttClient = mqttClient.mqttStub(logger)

    def __del__(self):
        self._log.info('Shutdown %s'%__app__)
        self.mqttClient.disconnect()


    def init(self,configFile='config.yaml'):

        config = self.openConfigFile(configFile)

        if config is not False:
            mqttConfig = config.get('mqtt',None)
            homieConfig = config.get('homie',None)
        else:
            return False

        if mqttConfig is None:
     #       self.initMqtt(mqttConfig)
      #  else:
            self._log.critical('Cannot start MQTT no Config File')
            return False

        if homieConfig is None:
            self._log.error('Cannot start pyHomie no Config File')
            return False

        if not self.initHomie(homieConfig,mqttConfig):
            return False

        if not self.startHomie():
            return False

        return True

    def openConfigFile(self,configFile='config.yaml') ->str:
        try:
            with open(configFile, 'r') as f:
                config = yaml.safe_load(f)
                self._log.debug('Startup of Homie with config: %s'% config)
        except Exception as e:
            self._log.error('Failed to open Configuration file %s Error Type %s'%(configFile,repr(e)))
            return False

        return config


    def initMqtt(self,config):
        if not self.mqttClient.connect(config.get('host','192.168.2.20')):
            self._log.critical('MQTT cannot be started')
            exit(-1)


    def initHomie(self,homieConfig,mqttConfig):
        self._log.debug('Start pyHomie with configuration %s'% homieConfig)

        if not self.lexicalCheck(homieConfig):
            self._log.error('Lexical check failed of configuration')
            return False

        if not self.initHomieDevice(homieConfig,mqttConfig):
            self._log.error('Failed to crate Homie Device')

        else:
            self._log.info('Homie Device created')

        return True

    def initHomieDevice(self,homieConfig,mqttConfig):
        for deviceId, deviceValue in homieConfig.items():
            deviceObj = device.device(id=deviceId, mqttObj=self.mqttClient, mqttConfig=mqttConfig, topic=deviceValue.get('topic', 'homie'), homie=deviceValue.get('homie', '4.0'), name=deviceValue.get('name', None), state=deviceValue.get('state', 'init'), logger=self._logHandler)
            setattr(self,deviceId,deviceObj)
            self._log.debug('Create device with ID: %s'%(deviceId))
            if not self.initHomieNode(deviceValue.get('nodes',[]),deviceObj):
                self._log.error('Failed to create Nodes')
                return False

        return True

    def initHomieNode(self,config,deviceObj):
        for nodeItem in config:
        #    print('item',nodeItem)
            for nodeId,nodeValue in nodeItem.items():
         #       print('nodeid',nodeId)
                nodeObj = node.node(id=nodeId, device=deviceObj, name=nodeValue.get('name', ''), type=nodeValue.get('type', ''), logger=self._logHandler)
               # setattr(self,nodeId, nodeObj)
               # print(nodeId,nodeObj)
          #print(deviceObj)
                deviceObj.registerNode(nodeId,nodeObj)
                self._log.debug('Create node with ID: %s' % (nodeId))
                if not self.initHomieProperty(nodeValue.get('properties',[]),nodeObj):
                    self._log.error('Failed to create Properties')
                    return False

        return True

    def initHomieProperty(self,config,nodeObj):
        for propertyItem in config:
            for propertyId, propertyValue in propertyItem.items():
                _type = getattr(properties, propertyValue.get('type', 'switch'))
                self._log.debug('Get property type %s of propertyID %s' % (_type, propertyId))

             #   propertyObj = _type(propertyId, nodeObj, logger=self._logHandler, **propertyValue)
                propertyObj = _type(propertyId, nodeObj, logger=self._logHandler, **propertyValue)
                nodeObj.registerProperty(propertyId, propertyObj)

        return True

    def lexicalCheck(self,config):

        try:
            validate(instance=config,schema=homieSchema.homieSchema)
            self._log.debug('Homie config validation completed successfully')

        except ValidationError as e:
            self._log.error('Homie config validation failed with error code %s '% (e.message))
            self._log.error('Failed at path %s'%(e.json_path))
            return False

        return True



    def startHomie(self):
        self._log.debug('Start Homie Interface')

        try:
           # if isinstance(value,device) in self.__dict__.va
            for id,instance in self.__dict__.items():
                #print(_instance_object,isinstance(_object,device))
                if isinstance(instance, device.device):
                   # print('True',device)
                    if not instance.init():
                        self._log.error('Error failed to start Homie interface')
                        return False
        except Exception as e:
            self._log.error('Failed to start pyHomie interface with messge %s'%(e.message))
            return False


        return True

    def start(self):
        self._log.info('Homie Application Start Running')
       # self.deviceRegister[0].init()
        self._updateTimer= watchdog.watchdog(60, self.stateUpdate)
        self._updateTimer.start()
        self._timeoutTimer= watchdog.watchdog(120, self.watchdogTimeout)
        self._timeoutTimer.start()

        for id, instance in self.__dict__.items():
            if isinstance(instance, device.device):
                instance.setState('ready')
        return True

    def stop(self):
        self._log.info('Homie Application Stop Running')
        self._updateTimer.cancel()
        self._timeoutTimer.cancel()

        for id, instance in self.__dict__.items():
            if isinstance(instance, device.device):
                instance.setState('disconnected')

        self.mqttClient.disconnect()

        return True

    def stateUpdate(self,value):
        self._log.debug('Homie $state update')
        for id,instance in self.__dict__.items():
            if isinstance(instance, device.device):
               # print('True',key,value)
                instance.updateStats()
        #self.deviceRegister[0].updateStates(value)
     # self._updateTimer.restart()
        self._updateTimer.cancel()
        self._updateTimer= watchdog.watchdog(60, self.stateUpdate)
        self._updateTimer.start()

    def watchdogTimeout(self,value):
        if 'TIMEOUT' in value:
            self._log.critical('Watchdog timeout, set Homie $state to lost')
            for id,instance in self.__dict__.items():
                if isinstance(instance, device.device):
                    # print('True',key,value)
                    instance.setState('lost')
           # self.deviceRegister[0].setState('lost')
        else:
            self._timeoutTimer.restart()

        return True

    def updateWatchdog(self) -> None:
        self._log.debug('Watchdog reset')
        self._timeoutTimer.restart()


    def getDevices(self) -> list:
        deviceList = []
        for id,instance in self.__dict__.items():
           # print(id,instance)
            if isinstance(instance, device.device):
                deviceList.append((id,instance))
        return deviceList

    def getNodes(self,device=None) -> list:
        nodeList = []
        for id, instance in self.getDevices():
            for id,instance in instance.__dict__.items():
                if isinstance(instance, node.node):
                    nodeList.append((id,instance))
        return nodeList



        return nodeList

    def getProperties(self) -> list:
        _list = []
        for id, instance in self.__dict__.items():
            if isinstance(instance, properties.propertyBase):
                _list.append(id)
        return _list


#unused
    def _validateId(self,id):
        if isinstance(id, str):
            r = re.compile("(^(?!\\-)[a-z0-9\\-]+(?<!\\-)$)")
            if r.match(id):
                if id in self.__dict__:
                    self._log.critical('Validation of ID failed: Duplicate ID: %s' % id)
                else:
                    self._log.debug('Validation of ID %s succeeded' % id)
                    return True
            else:
                self._log.critical('Validation of ID failed: Invalid ID %s provided'% id)
                return False



