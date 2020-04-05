from light.http_light_writer import HttpLightWriter
from light.light_timing import LightStepListener
from light.priority_light_writer import PriorityLightWriterFactory
from timing import Timing
from midi.midi_output import MidiOutputBpm, MidiOutputTime
import time
import midi.midi_bindings as bindings
from midi.midi_input import MidiInputSteps, MidiInputBpm


DEFAULT_IP = "192.168.1.72"
DEFAULT_PORT = 80
DEFAULT_GPIO = 12

if __name__ == "__main__":
    timing = Timing(4 * 8, 1.0 / 4.0)
    midi_binding = bindings.APC_KEY_25

    light_writer = HttpLightWriter(DEFAULT_IP, DEFAULT_PORT, DEFAULT_GPIO)
    priority_light_writer_factory = PriorityLightWriterFactory(light_writer)

    light_step_listener = LightStepListener(timing, priority_light_writer_factory.low())

    output_steps = MidiOutputTime(timing, midi_binding)
    output_bpm = MidiOutputBpm(timing, midi_binding)
    output_bpm.start_bpm_thread()

    input_bpm = MidiInputBpm(timing, midi_binding)
    input_bpm.start_listening()
    input_steps = MidiInputSteps(timing, midi_binding)
    input_steps.start_listening()


    timing.start_ticking()

    while(True):
        time.sleep(100)