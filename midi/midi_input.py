import mido
import threading
from midi.midi_bindings import MidiBindings
from observer import Observed, Observer
from datetime import datetime

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
        self.timing = timing
        self.last_presses = list()
        generic_listener.register_observer(self, MidiGenericInputListener.EVENT_NOTE_ON)

    def notify(self, source, event_type, value):
        if value == MidiBindings.BUTTON_BPM:
            self._pressed()

    def _pressed(self):
        self.last_presses.append(datetime.now())

        # Only keep the latest presses
        while len(self.last_presses) > 4:
            self.last_presses.pop(0)

        # Only keep for less than 10 seconds
        while len(self.last_presses) > 0 and \
                (datetime.now() - self.last_presses[0]).total_seconds() > 10:
            self.last_presses.pop(0)

        if len(self.last_presses) >= 3:
            self._change_bpm()

    def _change_bpm(self):
        if len(self.last_presses) < 2:
            return
        deltas = [(self.last_presses[i + 1] - self.last_presses[i]).total_seconds()
                  for i in range(len(self.last_presses) - 1)]
        average = sum(deltas) / float(len(deltas))
        bpm = 60.0 / average
        self.timing.set_bpm(bpm)
