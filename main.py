from light.http_light_writer import HttpLightWriter
from light.light_timing import LightStepListener
from light.priority_light_writer import PriorityLightWriterFactory
from timing import Timing
from midi.midi_output import MidiOutputBpm, MidiOutputTime
import time
import midi.midi_bindings as bindings
from midi.midi_input import *


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

    input_steps = MidiInputSteps(timing, midi_binding)
    input_steps.start_listening()

    generic_midi_input = MidiGenericInputListener(midi_binding)
    generic_midi_input.start_listening()

    input_bpm = MidiInputBpm(timing, generic_midi_input)
    midi_light_controller = MidiLightWriterController(
        priority_light_writer_factory.high(),
        generic_midi_input,
        midi_binding
    )

    midi_play_pause_controller = MidiPlayPauseController(
        timing,
        generic_midi_input,
        midi_binding
    )

    timing.start_ticking()

    while(True):
        time.sleep(100)