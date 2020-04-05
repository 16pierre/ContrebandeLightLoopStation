from light.light_writer import LightWriter
import requests

class HttpLightWriter(LightWriter):
    """ HTTP LightWriter, based on the ESPEASY protocols

    Example URL to control a GPIO switch:
    http://192.168.1.72/control?cmd=gpio,12,1
    """

    def __init__(self, ip, port, gpio):
        self.ip = ip
        self.port = port
        self.gpio = gpio

    def _switch_gpio(self, value):
        r = requests.get("http://%s:%d/control?cmd=gpio,%d,%d" %
                         (self.ip, self.port, self.gpio, value))
        r.raise_for_status()

    def on(self):
        self._switch_gpio(1)

    def off(self):
        self._switch_gpio(0)

    def neutral(self):
        pass
