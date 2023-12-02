from abc import ABC, abstractmethod

class AbstractBulbControl(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def set_color(self, r, g, b):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def turn_on(self):
        pass
