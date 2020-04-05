
class LightWriter:
    """ Interface representing a light output controller """

    def __init__(self):
        pass

    def on(self):
        raise NotImplementedError()

    def off(self):
        raise NotImplementedError()
