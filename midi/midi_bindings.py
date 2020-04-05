
class MidiBindings:
    """ Data structure representing which buttons to use on a midi controller """

    BUTTON_FORCE_ON = "FORCE_ON"
    BUTTON_BPM = "BPM"
    BUTTON_PLAY_PAUSE = "PLAY_PAUSE"


    def __init__(self, notes_for_time, midi_port_name, generic_midi):
        """
        :param notes_for_time: list[int], note for each beat/time
        :param midi_port: string, name of midi controller
        :param generic_midi: dict[string, int]: translates keys to symbols to be handled
        """
        self.notes_for_time = notes_for_time
        self.midi_port_name = midi_port_name
        self.generic_midi = generic_midi


"""
APC Key Pad Mapping:

32 ...
24 ...
16 ...
8 9 10 ... 15
0 1 2 ...  7

Round buttons under the pads:
64 ... 71

"""

APC_KEY_25 = MidiBindings(
    [i + 32 for i in range(8)] +
    [i + 24 for i in range(8)] +
    [i + 16 for i in range(8)] +
    [i + 8 for i in range(8)],
    "APC Key 25",
    {
        MidiBindings.BUTTON_FORCE_ON: 83, # SOLO button
        MidiBindings.BUTTON_BPM: 71,  # DEVICE button
        MidiBindings.BUTTON_PLAY_PAUSE: 1
    }

)
