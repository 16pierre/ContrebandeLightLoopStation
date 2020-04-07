from timing import Timing
from light.light_state import LightState
from observer import Observer
from midi.midi_bindings import MidiBindings
import mido
import threading
import time

COLOR_BLACK = 0
COLOR_GREEN = 1
COLOR_RED = 3
COLOR_YELLOW = 5
# Note: +1 => blink

class MidiOutputGeneric:
    def __init__(self, binding):
        self.port = mido.open_output(binding.midi_port_name)

    def _send_velocity(self, note, velocity, blink):
        if blink:
            velocity = velocity + 1
        msg = mido.Message('note_on', note=note, velocity=velocity)
        self.port.send(msg)

    def red(self, note, blink=False):
        self._send_velocity(note, COLOR_RED, blink)

    def green(self, note, blink=False):
        self._send_velocity(note, COLOR_GREEN, blink)

    def black(self, note):
        self._send_velocity(note, COLOR_BLACK, False)

    def yellow(self, note, blink=False):
        self._send_velocity(note, COLOR_YELLOW, blink)


class MidiOutputBpm:

    def __init__(self, timing, binding):
        self.binding = binding
        self.timing = timing
        self.generic_output = MidiOutputGeneric(binding)

    def start_bpm_thread(self):
        t = threading.Thread(target=self._tick_bpm, daemon=True, args=()).start()

    def _tick_bpm(self):
        while(True):
            # TODO: Replace this with a StepListener
            bpm = self.timing.get_bpm()
            self.generic_output.green(self.binding.generic_midi[MidiBindings.BUTTON_TAP_BPM])
            time.sleep(60.0 / bpm / 4.0)
            self.generic_output.black(self.binding.generic_midi[MidiBindings.BUTTON_TAP_BPM])
            time.sleep(60.0 / bpm / 4.0 * 3.0)


class MidiOutputTime(Observer):

    def __init__(self, timing, binding):
        super().__init__()
        self.binding = binding
        self.timing = timing
        self.generic_output = MidiOutputGeneric(binding)
        self.last_step = 0

        for note in self.binding.notes_for_time:
            self.generic_output.black(note)

        timing.register_observer(self, Timing.EVENT_TYPE_STEP_CHANGED)
        timing.register_observer(self, Timing.EVENT_TYPE_STEP_STATUS_CHANGED)

    def notify(self, source, event_type, value = None):
        self._refresh_output()

    def _refresh_output(self):
        current_step = self.timing.get_current_step()
        for step in range(len(self.binding.notes_for_time)):
            if step == current_step:
                self.generic_output.yellow(self.binding.notes_for_time[step])
            else:
                if self.timing.get_step_status(step) == LightState.STROBE:
                    self.generic_output.red(self.binding.notes_for_time[step])
                elif self.timing.get_step_status(step) == LightState.ON:
                    self.generic_output.green(self.binding.notes_for_time[step])
                else:
                    self.generic_output.black(self.binding.notes_for_time[step])

