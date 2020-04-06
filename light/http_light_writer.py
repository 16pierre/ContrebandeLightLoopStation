from light.light_writer import LightWriter
import requests
import threading
import time

class HttpLightWriter(LightWriter):
    """ HTTP LightWriter, based on the ESPEASY protocols

    Example URL to control a GPIO switch:
    http://192.168.1.72/control?cmd=gpio,12,1
    """

    def __init__(self, ip, port, gpio):
        self.ip = ip
        self.port = port
        self.gpio = gpio
        self._is_strobbing = False

    def _switch_gpio(self, value):
        r = requests.get("http://%s:%d/control?cmd=gpio,%d,%d" %
                         (self.ip, self.port, self.gpio, value))
        r.raise_for_status()
        #print(r.elapsed.total_seconds())

    def on(self):
        self._is_strobbing = False
        threading.Thread(target=self._switch_gpio, daemon=True, args=(1,)).start()

    def off(self):
        self._is_strobbing = False
        threading.Thread(target=self._switch_gpio, daemon=True, args=(0,)).start()

    def strobe(self):
        self._is_strobbing = True
        threading.Thread(target=self._strobe, daemon=True).start()

    def _strobe(self):
        while self._is_strobbing:
            if self._is_strobbing:
                self._switch_gpio(1)
            time.sleep(0.01)
            if self._is_strobbing:
                self._switch_gpio(0)
            time.sleep(0.01)

    def neutral(self):
        self.off()
