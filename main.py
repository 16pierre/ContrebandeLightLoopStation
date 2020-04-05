from http_light_writer import HttpLightWriter
from timing import Timing
from midi.midi_output import MidiOutputBpm, MidiOutputTime
import time
import midi.midi_bindings as bindings
from midi.midi_input import MidiInputSteps


DEFAULT_IP = "192.168.1.72"
DEFAULT_PORT = 80
DEFAULT_GPIO = 12

if __name__ == "__main__":
    light_writer = HttpLightWriter(DEFAULT_IP, DEFAULT_PORT, DEFAULT_GPIO)

    for i in range(00):
        light_writer.on()
        time.sleep(0.1)
        light_writer.off()
        time.sleep(0.1)

    timing = Timing(4 * 8, 1.0 / 4.0)
    midi_binding = bindings.APC_KEY_25
    output_bpm = MidiOutputBpm(timing, midi_binding)
    output_bpm.start_bpm_thread()

    output_steps = MidiOutputTime(timing, midi_binding)
    timing.start_ticking()

    input_steps = MidiInputSteps(timing, midi_binding)
    input_steps.start_listening()

    time.sleep(2^32)