
class MidiBindings:
    """ Data structure representing which buttons to use on a midi controller """

    def __init__(self, notes_for_time, note_for_bpm, midi_port_name):
        """
        :param notes_for_time: list[int], note for each beat/time
        :param note_for_bpm: int, note used to tap/display bpm
        :param midi_port: string, name of midi controller
        """
        self.notes_for_time = notes_for_time
        self.note_for_bpm = note_for_bpm
        self.midi_port_name = midi_port_name


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
    [i + 8 for i in range(8)] +
    [i + 0 for i in range(8)],
    71,
    "APC Key 25"
)
