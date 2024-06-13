
__app__ ='HomieSwitch'

from pyHomie import pyHomie
import logging
import time

logging.basicConfig(level=logging.DEBUG)


class HomieSwitch(object):
    def __init__(self):

        self.logger = logging.getLogger(__app__)
        self.logger.info('Starting Example: %s' % __app__)

        self.homieSwitch = pyHomie(__app__)

    def switch12Callback(self,value):
        print('Callback:',value)

    def initSwitch(self):
        #load configuration and setup mqtt
        if not self.homieSwitch.init('vzug.yaml'):
            print('Failed to init HomieSwitch object')
            return False

        #set default values
        #self.homieSwitch.node.switch21.value = 'OFF'
        self.homieSwitch.vzug01.program01.mashinestatus01.value = 'OFF'
       # self.homieSwitch.device01.node01.switch12.value = 'ON'
       # self.homieSwitch.device01.node01.switch12.registerCallback(self.switch12Callback)
       # self.homieSwitch.switch22.value = 0.0
        time.sleep(5)

        #start homieDevice
        if not self.homieSwitch.start():
            print('Failed')
            return False

        #print configuration
        print('Devices: ',self.homieSwitch.getDevices())
        print('Nodes: ',self.homieSwitch.getNodes('device01'))
        print('Nodes: ', self.homieSwitch.getNodes())
        print('Properties: ',self.homieSwitch.getProperties())

        return True

    def run(self):
        time.sleep(2)
        switch22value = 0.0
        counter = 0
        while counter < 3:
            counter = counter + 1
            self.homieSwitch.updateWatchdog()
        #    self.homieSwitch.switch21.value = 'ON'
         #   self.homieSwitch.switch22.value = switch22value
           # self.homieSwitch.device01.node01.switch11.value = 'ON'
          #  self.homieSwitch.switch12.value = False
           # switch22value = switch22value + 0.2
            time.sleep(5)
            #self.homieSwitch.switch21.value = 'OFF'
            #self.homieSwitch.switch22.value = switch22value
            #self.homieSwitch.device01.node01.switch11.value = 'OFF'
            #self.homieSwitch.switch12.value = True
            time.sleep(5)
           # switch22value = switch22value + 0.2

    def stop(self):
        self.homieSwitch.stop()

if __name__ == "__main__":
    homieDevice = HomieSwitch()
    if homieDevice.initSwitch():
        homieDevice.run()
        time.sleep(10)
        homieDevice.stop()

