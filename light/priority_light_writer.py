from light.light_writer import LightWriter
from light.light_state import LightState


class LightWriterCallback(LightWriter):

    def __init__(self, callback_on, callback_off, callback_neutral, callback_strobe):
        self.on = callback_on
        self.off = callback_off
        self.neutral = callback_neutral
        self.strobe = callback_strobe


class PriorityLightWriterFactory:

    PRIORITY_HIGH = 100
    PRIORITY_LOW = 1

    def __init__(self, light_writer):
        self._priority_to_order_dict = dict()
        self._light_writer = light_writer

    def _build_callback_writer(self, priority):
        return LightWriterCallback(
            lambda: self._on(priority),
            lambda: self._off(priority),
            lambda: self._neutral(priority),
            lambda: self._strobe(priority)
        )

    def high(self):
        return self._build_callback_writer(PriorityLightWriterFactory.PRIORITY_HIGH)

    def low(self):
        return self._build_callback_writer(PriorityLightWriterFactory.PRIORITY_LOW)

    def _neutral(self, priority):
        self._priority_to_order_dict.pop(priority)
        self._recalculate_lighting()

    def _on(self, priority):
        self._priority_to_order_dict[priority] = LightState.ON
        self._recalculate_lighting()

    def _off(self, priority):
        self._priority_to_order_dict[priority] = LightState.OFF
        self._recalculate_lighting()

    def _strobe(self, priority):
        self._priority_to_order_dict[priority] = LightState.STROBE
        self._recalculate_lighting()

    def _recalculate_lighting(self):
        k = max(self._priority_to_order_dict.keys())
        self._light_writer.set_state(self._priority_to_order_dict[k])

