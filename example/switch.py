
#__name__ ='SwitchHomie'

from src.pyHomie import pyHomie
import logging
import time

logging.basicConfig(level=logging.DEBUG)



def switch01(value):
    print('Switch01',value)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info('Starting')
    homieSwitch = pyHomie.pyHomie(__name__)
  #  homieSwitch.enable_logger(logger)
    homieSwitch.init('switch.yaml')
    homieSwitch.run()
    time.sleep(2)
    print('Devices: ',homieSwitch.getDevices())
    print('Nodes: ',homieSwitch.getNodes())
    print('Properties: ',homieSwitch.getProperties())
    while True:
        homieSwitch.updateWatchdog()
        homieSwitch.switch11.value = True
        homieSwitch.switch12.value = False
        time.sleep(10)
        homieSwitch.switch11.value = False
        homieSwitch.switch12.value = True
        time.sleep(10)