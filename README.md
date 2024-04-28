
## Motivation

easy to use and flexible library in python for <a href="https://homieiot.github.io">homie</a> convention

Python 3
Homie 4.0.0

configuration of homie device is mainly carried out in a Yaml file

mqtt configuration in section mqtt
~~~~yaml
mqtt:
    host: 192.168.2.20
    port: 1889 <optional>
    user: markus <optional>
    passwd: Geheim <optional>
~~~~
homie section
~~~~yaml
homie:
    device01:
        topic: homieTest
        id: device01
        name: Dishwasher
        node01:
            name: Program
            switch01:
                name: Power1
                type: switch
                settable: True
            float02:
                name: Power2
                type: string
                settable: True
        node02:
            name: Program
            string21:
                name: Power1
                type: string
                settable: True
            switch22:
                name: Power2
                type: switch
                settable: True
~~~~
## Example

~~~~python
import pyhomie

if __name__ == "__main__":
    homie = pyhomie()
    homie.init('config.yaml')
    homie.run()
    homie.switch01('True')
~~~~