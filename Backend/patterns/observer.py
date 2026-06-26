from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Any

class Event:
    """
    Clase simple para representar un evento con un tipo y datos asociados.
    """
    def __init__(self, event_type: str, data: dict[str, Any]):
        self.type = event_type
        self.data = data

class Observer(ABC):
    """La interfaz Observer declara el método de actualización."""
    @abstractmethod
    def update(self, event: Event) -> None:
        pass

class Subject:
    """La clase Subject gestiona los observadores y las notificaciones."""
    _observers: List[Observer]

    def __init__(self) -> None:
        self._observers = []

    def attach(self, observer: Observer) -> None:
        """Adjunta un observador al sujeto."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Separa un observador del sujeto."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: Event) -> None:
        """Notifica a todos los observadores sobre un evento."""
        for observer in self._observers:
            observer.update(event)