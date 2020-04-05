import mido
import threading

class MidiInputSteps:

    def __init__(self, timing, binding):
        self.binding = binding
        self.timing = timing

    def start_listening(self):
        t = threading.Thread(target=self._listen, daemon=True, args=()).start()

    def _listen(self):
        print("Listening")
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

