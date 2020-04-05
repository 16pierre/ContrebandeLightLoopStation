import mido

DEFAULT_PORT = "APC Key 25"

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


def test_output():
    port = mido.open_output(DEFAULT_PORT)
    for i in range(100):
        msg = mido.Message('note_on', note=i, velocity=8)
        port.send(msg)

# Useful for debugging purposes
def test_input():
    with mido.open_input(DEFAULT_PORT) as inport:
        for msg in inport:
            print(msg)

if __name__ == "__main__":
    test_input()