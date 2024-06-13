import pytest

from pyHomie import pyHomie
import logging
logging.basicConfig(level=logging.INFO)

__app__ = 'TEST'
def test_open_config_file() -> None:
    logger = logging.getLogger(__app__)
    logger.info('Starting Example: %s' % __app__)
    pyhomieSwitch = pyHomie(__app__)
    x = pyhomieSwitch.init('fixtures/switchTest.yaml')
    print(x)
    assert pyhomieSwitch.init('fixtures/switchTest.yaml') == True

if __name__ == "__main__":
    test_open()