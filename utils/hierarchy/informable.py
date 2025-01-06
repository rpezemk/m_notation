class Informable():
    def set_state(self, state: bool):
        ...

class Informer():
    def __init__(self):
        self.informables: list[Informable] = []

    def set_state(self, state: bool):
        for informable in self.informables:
            informable.set_state(state)

    def bind_to(self, informable: Informable):
        self.informables.append(informable)
        return self