from timing import Timing
from observer import Observer
import mido
import threading
import time

COLOR_BLACK = 0
COLOR_GREEN = 1
COLOR_RED = 3
COLOR_YELLOW = 5
# Note: +1 => blink


def red(port, note):
    msg = mido.Message('note_on', note=note, velocity=COLOR_RED)
    port.send(msg)


def green(port, note):
    msg = mido.Message('note_on', note=note, velocity=COLOR_GREEN)
    port.send(msg)


def black(port, note):
    msg = mido.Message('note_on', note=note, velocity=COLOR_BLACK)
    port.send(msg)


def yellow(port, note):
    msg = mido.Message('note_on', note=note, velocity=COLOR_YELLOW)
    port.send(msg)


class MidiOutputBpm:

    def __init__(self, timing, binding):
        self.binding = binding
        self.timing = timing
        self.port = mido.open_output(binding.midi_port_name)

    def start_bpm_thread(self):
        t = threading.Thread(target=self._tick_bpm, daemon=True, args=()).start()

    def _tick_bpm(self):
        while(True):
            bpm = self.timing.get_bpm()
            time.sleep(60.0 / bpm / 2.0)
            green(self.port, self.binding.note_for_bpm)
            time.sleep(60.0 / bpm / 2.0)
            black(self.port, self.binding.note_for_bpm)


class MidiOutputTime(Observer):

    def __init__(self, timing, binding):
        super().__init__()
        self.binding = binding
        self.timing = timing
        self.port = mido.open_output(binding.midi_port_name)
        self.last_step = 0

        for note in self.binding.notes_for_time:
            black(self.port, note)

        timing.register_observer(self, Timing.EVENT_TYPE_STEP_CHANGED)

    def notify(self, source, event_type):
        self._refresh_output()

    def _refresh_output(self):
        current_step = self.timing.get_current_step()
        for step in range(len(self.binding.notes_for_time)):
            if step == current_step:
                yellow(self.port, self.binding.notes_for_time[step])
            else:
                if self.timing.get_step_status(step):
                    green(self.port, self.binding.notes_for_time[step])
                else:
                    black(self.port, self.binding.notes_for_time[step])

