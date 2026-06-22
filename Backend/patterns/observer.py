"""
Observer Pattern Implementation
Define una dependencia de uno-a-muchos entre objetos
"""

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class Event:
    """Representa un evento en el sistema"""

    def __init__(self, event_type: str, data: dict):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"Event(type={self.event_type}, timestamp={self.timestamp})"


class Observer(ABC):
    """Interfaz para observadores"""

    @abstractmethod
    def update(self, event: Event) -> None:
        """Llamado cuando ocurre un evento"""
        pass


class NotificationObserver(Observer):
    """Observador que envía notificaciones"""

    def update(self, event: Event) -> None:
        print(f"[NOTIFICATION] {event.event_type}: {event.data}")


class LogObserver(Observer):
    """Observador que registra eventos en logs"""

    def update(self, event: Event) -> None:
        from Backend.logger.logger import LoggerManager
        logger = LoggerManager().get_logger()
        logger.info(f"EVENT: {event.event_type} - Data: {event.data}")


class EventSubject:
    """Sujeto que notifica a observadores"""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Suscribir observador"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Desuscribir observador"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: Event) -> None:
        """Notificar a todos los observadores"""
        for observer in self._observers:
            observer.update(event)

    def get_observers_count(self) -> int:
        """Retorna cantidad de observadores"""
        return len(self._observers)
