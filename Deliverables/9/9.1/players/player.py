from abc import ABC, abstractmethod


class Player(ABC):
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def receive_stones(self, stone):
        pass

    @abstractmethod
    def make_a_move(self, boards):
        pass

    @abstractmethod
    def end_game(self):
        pass
