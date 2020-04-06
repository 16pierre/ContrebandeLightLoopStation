from light.light_state import LightState

class LightWriter:
    """ Interface representing a light output controller """

    def __init__(self):
        pass

    def on(self):
        raise NotImplementedError()

    def off(self):
        raise NotImplementedError()

    def strobe(self):
        raise NotImplementedError()

    def neutral(self):
        raise NotImplementedError()

    def set_state(self, light_state):
        if light_state == LightState.NEUTRAL:
            self.neutral()
        if light_state == LightState.OFF:
            self.off()
        if light_state == LightState.ON:
            self.on()
        if light_state == LightState.STROBE:
            self.strobe()

