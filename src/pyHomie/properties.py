


class propertyBase(object):
    def __init__(self,id,node,name="Switch",datatype='',settable=True,retained=True,unit='None',format='',value=None, callback=None):
        self.id = id
        self.node = node
        self.name = name
        self.datatype = datatype
        print('datatype2', self.datatype)
        self.format = format
        self.settable = settable
        self.retained = retained
        self.unit = unit
        self._value = True

        self.callback = None
   #     self.__dict__

    def init(self,mqttObj,baseTopic):
        self.mqttObj = mqttObj
        self.topic = "/".join((baseTopic,self.id))
        self.publish()
        print('init Property',self.id,self.node,self.topic)

        if self.settable:
            self.mqttObj.subscribe("{}/set".format(self.topic), self.on_message_callback)


    def publish(self):
        print('publish',self.topic,self.name)
        self.mqttObj.publish("{}/$name".format(self.topic), self.name, True, 1)
        self.mqttObj.publish("{}/$datatype".format(self.topic), str(self.datatype), True, 1)
       # print(self.settable)
        self.mqttObj.publish("{}/$settable".format(self.topic), str(self.settable).lower(), True, 1)
        self.mqttObj.publish("{}/$retained".format(self.topic), str(self.retained).lower(), True, 1)


        if self.datatype:
            print('datatype1',self.datatype)
            self.mqttObj.publish("{}/$datatype".format(self.topic), self.datatype, True, 1)

        print(self.unit)
        if self.unit:
            self.mqttObj.publish("{}/$unit".format(self.topic), self.unit, True, 1)

        if self.format is not None:
            self.mqttObj.publish("{}/$format".format(self.topic), self.format, True, 1)

        if self.value is not None:
            self.mqttObj.publish(self.topic, self.value, self.retained, 1)

    @property
    def value(self):
        print("Getting value...")
        return self._value

    @value.setter
    def value(self,value):
        print("Setting",value)
        if self.validate_value(value):
            print('topic',self.topic,self.retained,value)
            self.mqttObj.publish(self.topic, self.convertToPayload(value), self.retained, 1)
        else:
            print('validation error')


    def validate_value(self, value):
        return True #override as needed

    def convertFromPayload(self, value):
        return value #override as needed

    def on_message_callback(self,client,obj, msg):
        # This callback will only be called for messages with topics that match
        # $SYS/broker/messages/#
        print("MESSAGES: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        value = self.convertFromPayload(msg.payload.decode("utf-8"))
        print(value,type(value))
        self.value = value
        if self.callback is not None:
            self.callback(value)

    def registerCallback(self,callback):
        self.callback = callback


class switch(propertyBase):
   #def __init__(self,id:str, name:str="Switch", datatype:str=None, settable:bool=True ,retained:bool=True ,unit:str='None' ,dataformat:str='' ,value:str=None ,callback:None=None):
   # def __init__(self,id:str,name:str="Switch",**kwargs):
    def __init__(self,id,node,name,**kwargs):
        self._id = id
       # node = self._node
        self._node = node
        self._name = name
        self._datatype=kwargs.get("datatype",'boolean')

        self._format = kwargs.get("format",'OFF:ON')
        self._settable=kwargs.get("settable",False)
        self._retained=kwargs.get("retained",True)
        self._unit=kwargs.get("unit",None)

        self._value=kwargs.get("value",None)
        self._callback=kwargs.get("callback",None)

        super().__init__(id=id, node=self._node, name=name, settable=self._settable, retained=self._retained,unit=self._unit, datatype=self._datatype, format=self._format, value=self._value,callback=self._callback)
       # super().__init__(id, name, settable, retained, unit, datatype, format, value, callback):

    def validate_value(self, value):
        return value in[True, False]

    def convertFromPayload(self,payload):
        print(payload)
        if payload is not str:

            payload = str(payload)
            print(payload,type(payload))
        if payload == 'true':
            return 'ON'
        elif payload == 'false':
            return 'OFF'
        else:
            return None

    def convertToPayload(self,value):
        if value:
            return self._format.split(':')[1]
        elif not value:
            return self._format.split(':')[0]
        else:
            return None


class string(propertyBase):
    def __init__(self,id,node,name,**kwargs):
        self._id = id
        self._node=node
        self._name = name
        self._datatype=kwargs.get("datatype",'string')

        self._format = kwargs.get("format",None)
        self._settable=kwargs.get("settable",False)
        self._retained=kwargs.get("retained",True)
        self._unit=kwargs.get("unit",None)

        self._value=kwargs.get("value",None)
        self._callback=kwargs.get("callback",None)

        super().__init__(id=id, node=self._node,name=name, settable=self._settable, retained=self._retained,unit=self._unit, datatype=self._datatype, format=self._format, value=self._value,callback=self._callback)


    def validate_value(self, value):
        return value in [True,False]

    def convertFromPayload(self, payload):
        if payload == 'true':
            return 'ON'
        elif payload == 'false':
            return 'OFF'
        else:
            return None

    def convertToPayload(self, value):
        pass


class float(propertyBase):
    def __init__(self,id,node,name,**kwargs):
        self._id = id
        self._node=node
        self._name = name
        self._datatype=kwargs.get("datatype",'float')

        self._format = kwargs.get("format",None)
        self._settable=kwargs.get("settable",False)
        self._retained=kwargs.get("retained",True)
        self._unit=kwargs.get("unit",None)

        self._value=kwargs.get("value",None)
        self._callback=kwargs.get("callback",None)

        super().__init__(id=id, node=self._node,name=name, settable=self._settable, retained=self._retained,unit=self._unit, datatype=self._datatype, format=self._format, value=self._value,callback=self._callback)


   # def __init__(self, id: str, name: str = "Switch", datatype: type = bool, settable: bool = True,
     #            retained: bool = True, unit: str = None, dataformat: str = '', value: str = None,
    #             callback: None = None):

      #  super().__init__(id, name, datatype, settable, retained, unit, dataformat, value, callback)

    def validate_value(self, value):
        return value in ['ON', 'OFF']

    def convertFromPayload(self, payload):
        if payload == 'true':
            return 'ON'
        elif payload == 'false':
            return 'OFF'
        else:
            return None

if __name__ == "__main__":
    x = switch('id01','o','i')
    print(x)
    if isinstance(x, switch):
        print('True')