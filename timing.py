from copy import deepcopy
from observer import Observed
import time, threading

class Timing(Observed):

    EVENT_TYPE_STEP_CHANGED = "TIMING_STEP_CHANGED"
    EVENT_TYPE_STEP_STATUS_CHANGED = "TIMING_STEP_STATUS_CHANGED"
    EVENT_TYPE_BPM_CHANGED = "TIMING_BPM_CHANGED"

    def __init__(self, number_of_steps, beats_per_step):
        super().__init__()
        self._beats_per_step = float(beats_per_step)
        self._steps = [False for _ in range(number_of_steps)]
        self._bpm = 120.0
        self._step = 0

    def start_ticking(self):
        threading.Thread(target=self._tick, daemon=True, args=()).start()

    def _tick(self):
        while(True):
            bpm = self.get_bpm()
            time.sleep(60.0 / bpm * self._beats_per_step)
            self.next_step()

    def next_step(self):
        self._step += 1
        if self._step >= len(self._steps):
            self._step = 0
        self.notify_observers(self.EVENT_TYPE_STEP_CHANGED)

    def get_current_step(self):
        return self._step

    def get_steps_status(self):
        return deepcopy(self._steps)

    def get_step_status(self, step):
        if step >= len(self._steps):
            return None
        return self._steps[step]

    def set_step_status(self, step, is_on):
        self._steps[step] = is_on
        self.notify_observers(self.EVENT_TYPE_STEP_STATUS_CHANGED)

    def get_bpm(self):
        return self._bpm

    def set_bpm(self, bpm):
        self._bpm = bpm
        self.notify_observers(self.EVENT_TYPE_BPM_CHANGED)
