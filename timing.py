from copy import deepcopy
from observer import Observed
import time, threading
from light.light_state import LightState

DELTA_NS_LIGHT_HEAT = 200_000_000.0


class Timing(Observed):

    EVENT_TYPE_STEP_CHANGED = "TIMING_STEP_CHANGED"
    EVENT_TYPE_STEP_STATUS_CHANGED = "TIMING_STEP_STATUS_CHANGED"
    EVENT_TYPE_BPM_CHANGED = "TIMING_BPM_CHANGED"

    def __init__(self, number_of_steps, beats_per_step):
        super().__init__()
        self._beats_per_step = float(beats_per_step)
        self._steps = [LightState.OFF for _ in range(number_of_steps)]
        self._bpm = 120.0
        self._step = 0
        self._clock_thread = None
        self._stopped = False  # TODO: make this thread safe
        self._last_step_ns = 0
        self._step_delta_ns = 1
        self._recalculate_step_delta_ns()

    def start_ticking(self):
        self._clock_thread = threading.Thread(target=self._tick, daemon=True, args=())
        self._clock_thread.start()

    def _recalculate_step_delta_ns(self):
        self._step_delta_ns = 60.0 / self.get_bpm() * self._beats_per_step * float(1_000_000_000)

    def _tick(self):
        while(True):
            if self.is_paused():
                time.sleep(0.001)
                continue

            current_ns = time.clock_gettime_ns(time.CLOCK_REALTIME)
            if current_ns - self._last_step_ns > self._step_delta_ns:
                self._last_step_ns = current_ns
                threading.Thread(target=self.next_step, daemon=True, args=()).start()

    def reset(self):
        self._step = 0
        self._last_step_ns = time.clock_gettime_ns(time.CLOCK_REALTIME) - DELTA_NS_LIGHT_HEAT
        self.notify_observers(self.EVENT_TYPE_STEP_CHANGED)

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

    def set_step_status(self, step, state):
        if step >= len(self._steps):
            return
        self._steps[step] = state
        self.notify_observers(self.EVENT_TYPE_STEP_STATUS_CHANGED)

    def get_bpm(self):
        return self._bpm

    def set_bpm(self, bpm):
        self._bpm = bpm
        print("New BPM: %s" % bpm)
        self.notify_observers(self.EVENT_TYPE_BPM_CHANGED)

    def pause(self):
        self._stopped = True

    def play(self):
        self._stopped = False

    def is_paused(self):
        return self._stopped
