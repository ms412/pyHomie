
__app__ ='SwitchHomie'

from src.pyHomie import pyHomie
import logging
import time

logging.basicConfig(level=logging.INFO)


class HomieSwitch(object):
    def __init__(self):
        self.logger = logging.getLogger(__app__)
        self.logger.info('Starting Example: %s' % __app__)

        self.homieSwitch = pyHomie.pyHomie(__app__)

    def initSwitch(self):
        #load configuration and setup mqtt
        self.homieSwitch.init('switch.yaml')

        #set default values
        self.homieSwitch.switch21.value = 'OFF'
        self.homieSwitch.switch11.value = False
        self.homieSwitch.switch22.value = 0.0

        #start homieDevice
        self.homieSwitch.start()

        #print configuration
        print('Devices: ',self.homieSwitch.getDevices())
        print('Nodes: ',self.homieSwitch.getNodes())
        print('Properties: ',self.homieSwitch.getProperties())

    def run(self):
        switch22value = 0.0
        counter = 0
        while counter < 3:
            counter = counter + 1
            self.homieSwitch.updateWatchdog()
            self.homieSwitch.switch21.value = 'ON'
            self.homieSwitch.switch22.value = switch22value
            self.homieSwitch.switch11.value = True
            self.homieSwitch.switch12.value = False
            switch22value = switch22value + 0.2
            time.sleep(5)
            self.homieSwitch.switch21.value = 'OFF'
            self.homieSwitch.switch22.value = switch22value
            self.homieSwitch.switch11.value = False
            self.homieSwitch.switch12.value = True
            time.sleep(5)
            switch22value = switch22value + 0.2

    def stop(self):
        self.homieSwitch.stop()

if __name__ == "__main__":
    homieDevice = HomieSwitch()
    homieDevice.initSwitch()
    homieDevice.run()
    time.sleep(10)
    homieDevice.stop()

