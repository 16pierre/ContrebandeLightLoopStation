from timing import Timing
from observer import Observer


class LightStepListener(Observer):

    def __init__(self, timing, light_writer):
        super().__init__()
        self.timing = timing
        self.light_writer = light_writer

        self.timing.register_observer(self, Timing.EVENT_TYPE_STEP_CHANGED)

    def notify(self, source, event_type):
        current_step_status = self.timing.get_step_status(
            self.timing.get_current_step())
        if current_step_status:
            self.light_writer.on()
        else:
            self.light_writer.off()



