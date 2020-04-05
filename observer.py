from collections import defaultdict

class Observer:
    def __init__(self):
        pass

    def notify(self, source, event_type, value = None):
        raise NotImplementedError()

class Observed:
    def __init__(self):
        self._observers = defaultdict(set)

    def register_observer(self, obs, event_type):
        self._observers[event_type].add(obs)

    def notify_observers(self, event_type, value = None):
        for obs in self._observers[event_type]:
            obs.notify(self, event_type, value)
