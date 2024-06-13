
import logging
from pyHomie import properties

class node(object):
    def __init__(self,id,device,name='',type='',logger='logger'):

        _libName = str(__name__.rsplit('.', 1)[-1])
        self._log = logging.getLogger(logger + '.' + _libName + '.' + self.__class__.__name__)

        self.id = id
        self.device = device
        self.name = name
        self.type = type

        self._log.info('Create Node Objact ID: %s' % (self.id))

    def __del__(self):
        self._log.debug('Delete node %s'%(self.id))

    def registerProperty(self,id,propertyObj):
        self._log.info('PropertyID %s registered at Node %s' % (id, self.id))
        #print('regisertNode',id)
        setattr(self,id,propertyObj)
       # self.nodesRegister[id] = nodeObj
      #  print(self.__dict__)
        return True

    def init(self,mqttObj,baseTopic):
        self._log.info('Start initalisation of node ID: %s' % self.id)
        self.mqttObj = mqttObj
        self.topic = "/".join((baseTopic, self.id))
        self.publish()


        for id,instance in self.__dict__.items():
           # print('ID %s, Instance: %s)' %(id,instance))
           # print(properties.propertyBase)
           # print('init PROPERTY', id, instance, isinstance(instance, properties.propertyBase))
            #print()
            #if isinstance(instance, property):
        #    print(instance,properties.property)
          #  if issubclass(properties.property,instance):
           #     print('is Subclass of properties')
            if isinstance(instance, properties.propertyBase):
              #  print('init Property,', id, instance)
                if not instance.init(self.mqttObj,self.topic):
                    self._log.error('Error')
                    return False

        return True


    def publish(self):

        self.mqttObj.publish("{}/$name".format(self.topic), self.name, True, 1)
    #    self.mqttObj.publish("{}/$type".format(self.topic), self.type, True, 1)
        #if self.properties:
        propertiesList =[]
        for id, instance in self.__dict__.items():
            if isinstance(instance, properties.propertyBase):
                propertiesList.append(instance.id)

        self.mqttObj.publish("/".join((self.topic, "$properties")), ",".join(propertiesList), retain=True, qos=1)
