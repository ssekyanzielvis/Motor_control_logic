from abc import ABC, abstractmethod

class IMotorController(ABC):
    @abstractmethod
    def start_motor(self):
        pass

    @abstractmethod
    def stop_motor(self):
        pass

    @abstractmethod
    def set_speed(self, speed):
        pass

    @abstractmethod
    def get_status(self):
        pass