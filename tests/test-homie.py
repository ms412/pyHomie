
import pytest
import pyhomie


@pytest.mark.read_only
@pytest.mark.parametrize("ip_addr",
                         [
         ('192.168.2.20')
    ]
)

def test_read_only(ip_addr):
    homie = homie()
    homie.init()
