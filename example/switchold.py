
__app__ ='SwitchHomie'

from src.pyHomie import pyHomie
import logging
import time

logging.basicConfig(level=logging.INFO)



def switch01(value):
    print('Switch01',value)

if __name__ == "__main__":
    logger = logging.getLogger(__app__)
    logger.info('Starting Example: %s'% __app__)
    homieSwitch = pyHomie.pyHomie(__app__)
  #  homieSwitch.enable_logger(logger)
    homieSwitch.init('switch.yaml')
    homieSwitch.switch21.value = 'OFF'
    homieSwitch.switch11.value = False
    homieSwitch.switch22.value = 0.0
    time.sleep(10)
    homieSwitch.start()
    time.sleep(2)
    print('Devices: ',homieSwitch.getDevices())
    print('Nodes: ',homieSwitch.getNodes())
    print('Properties: ',homieSwitch.getProperties())
    switch22value = 0.0
    counter = 0
    while counter < 3:
        counter = counter + 1
        homieSwitch.updateWatchdog()
        homieSwitch.switch21.value = 'ON'
        homieSwitch.switch22.value = switch22value
        homieSwitch.switch11.value = True
        homieSwitch.switch12.value = False
        switch22value = switch22value + 0.2
        time.sleep(5)
        homieSwitch.switch21.value = 'OFF'
        homieSwitch.switch22.value = switch22value
        homieSwitch.switch11.value = False
        homieSwitch.switch12.value = True
        time.sleep(5)
        switch22value = switch22value + 0.2

    print('completed')
    time.sleep(1)
    homieSwitch.stop()
    time.sleep(10)
