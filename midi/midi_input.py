import mido
import threading
import math
from midi.midi_bindings import MidiBindings
from observer import Observed, Observer
from datetime import datetime
from midi.midi_output import MidiOutputGeneric


class MidiInputSteps:

    def __init__(self, timing, binding):
        self.binding = binding
        self.timing = timing

    def start_listening(self):
        t = threading.Thread(target=self._listen, daemon=True, args=()).start()

    def _listen(self):
        with mido.open_input(self.binding.midi_port_name) as inport:
            for msg in inport:
                self.handle(msg)

    def handle(self, midi_msg):
        if midi_msg.type != "note_on":
            return
        note = midi_msg.note
        try:
            step_index = self.binding.notes_for_time.index(note)
            self.timing.set_step_status(step_index, not self.timing.get_step_status(step_index))
        except ValueError:
            return

class MidiGenericInputListener(Observed):

    EVENT_NOTE_ON = "MIDI_NOTE_ON"
    EVENT_NOTE_OFF = "MIDI_NOTE_OFF"

    def __init__(self, binding):
        super().__init__()
        self.binding = binding

    def start_listening(self):
        t = threading.Thread(target=self._listen, daemon=True, args=()).start()

    def _listen(self):
        with mido.open_input(self.binding.midi_port_name) as inport:
            for msg in inport:
                self.handle(msg)

    def handle(self, midi_msg):
        if midi_msg.type not in ["note_on", "note_off"]:
            return

        note = midi_msg.note
        for (k, v) in self.binding.generic_midi.items():
            if v == note:
                event_type = self.EVENT_NOTE_ON if midi_msg.type == "note_on" \
                        else self.EVENT_NOTE_OFF
                self.notify_observers(event_type, k)


class MidiInputBpm(Observer):
    def __init__(self, timing, generic_listener):
        super().__init__()
        self.timing = timing
        self.last_presses = list()
        generic_listener.register_observer(self, MidiGenericInputListener.EVENT_NOTE_ON)
        self.counter = 0

    def notify(self, source, event_type, value):
        if value == MidiBindings.BUTTON_BPM:
            self._pressed()

    def _pressed(self):
        self.last_presses.append(datetime.now())

        while len(self.last_presses) > 64:
            self.last_presses.pop(0)

        if len(self.last_presses) > 0 and \
                (datetime.now() - self.last_presses[len(self.last_presses) - 1]).total_seconds() > 3:
            self.last_presses.clear()

        if len(self.last_presses) >= 3:
            self._change_bpm()

    def _change_bpm(self):
        if len(self.last_presses) < 2:
            return
        deltas = [(self.last_presses[i + 1] - self.last_presses[i]).total_seconds()
                  for i in range(len(self.last_presses) - 1)]
        average = sum(deltas) / float(len(deltas))
        bpm = 60.0 / average

        if len(deltas) < 8:
            bpm = math.ceil(bpm)
        elif len(deltas) < 16:
            bpm = math.ceil(bpm * 2.0) / 2.0
        else:
            bpm = math.ceil(bpm * 4.0) / 4.0

        self.timing.set_bpm(bpm)
        print("New BPM: %s, deltas: %s" % (bpm, deltas))

class MidiLightWriterController(Observer):
    def __init__(self, light_writer, generic_listener, bindings):
        super().__init__()
        self.light_writer = light_writer
        self.generic_output = MidiOutputGeneric(bindings)
        self.bindings = bindings
        generic_listener.register_observer(self, MidiGenericInputListener.EVENT_NOTE_OFF)
        generic_listener.register_observer(self, MidiGenericInputListener.EVENT_NOTE_ON)

        self.generic_output.green(
            bindings.generic_midi[MidiBindings.BUTTON_FORCE_ON],
            blink=True)

    def notify(self, source, event_type, value = None):
        if value == MidiBindings.BUTTON_FORCE_ON:
            if event_type == MidiGenericInputListener.EVENT_NOTE_OFF:
                self.light_writer.neutral()
                self.generic_output.green(
                    self.bindings.generic_midi[MidiBindings.BUTTON_FORCE_ON],
                    blink=True)
            if event_type == MidiGenericInputListener.EVENT_NOTE_ON:
                self.light_writer.on()
                self.generic_output.green(
                    self.bindings.generic_midi[MidiBindings.BUTTON_FORCE_ON],
                    blink=False)


class MidiPlayPauseController(Observer):
    def __init__(self, timing, generic_listener, bindings):
        super().__init__()
        self.timing = timing
        self.generic_output = MidiOutputGeneric(bindings)
        self.bindings = bindings
        generic_listener.register_observer(self, MidiGenericInputListener.EVENT_NOTE_ON)

        self.generic_output.red(
            bindings.generic_midi[MidiBindings.BUTTON_PLAY_PAUSE],
            blink=True)
        self.generic_output.yellow(
            bindings.generic_midi[MidiBindings.BUTTON_RESET],
            blink=False)

    def notify(self, source, event_type, value = None):
        if value == MidiBindings.BUTTON_PLAY_PAUSE:
            if self.timing.is_paused():
                self.timing.play()
                self.generic_output.red(
                        self.bindings.generic_midi[MidiBindings.BUTTON_PLAY_PAUSE],
                        blink=True)
            else:
                self.timing.pause()
                self.generic_output.red(
                    self.bindings.generic_midi[MidiBindings.BUTTON_PLAY_PAUSE],
                    blink=False)

        if value == MidiBindings.BUTTON_RESET:
            self.timing.reset()
            self.timing.play()

