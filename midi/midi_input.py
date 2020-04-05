import mido
import threading
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

class MidiInputBpm:
    def __init__(self, timing, binding):
        self.binding = binding
        self.timing = timing
        self.last_presses = list()

    def start_listening(self):
        t = threading.Thread(target=self._listen, daemon=True, args=()).start()

    def _listen(self):
        with mido.open_input(self.binding.midi_port_name) as inport:
            for msg in inport:
                self.handle(msg)

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

    def handle(self, midi_msg):
        if midi_msg.type != "note_on":
            return
        note = midi_msg.note
        if self.binding.note_for_bpm != note:
            return

        self._pressed()
