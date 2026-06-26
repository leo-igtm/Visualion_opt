from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Any


class Observer(ABC):
    """
    La interfaz Observer declara el método de actualización, utilizado por los sujetos.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Recibe la actualización del sujeto.
        """
        pass


class Subject:
    """
    La clase Subject gestiona los observadores y las notificaciones.
    Puede ser usada como una clase base (herencia) o a través de composición.
    """

    _observers: List[Observer]

    def __init__(self, **kwargs: Any) -> None:
        # Se usa **kwargs: Any y super().__init__ para que esta clase pueda ser
        # usada en herencia múltiple (ej. con modelos de SQLAlchemy).
        # Esto corrige el error de tipo en 'kwargs'.
        super().__init__(**kwargs)
        self._observers = []

    def attach(self, observer: Observer) -> None:
        """
        Adjunta un observador al sujeto.
        Al tipar 'observer: Observer', corregimos los errores de tipo.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Separa un observador del sujeto.
        Al tipar 'observer: Observer', corregimos los errores de tipo.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        """
        Notifica a todos los observadores sobre un evento.
        """
        for observer in self._observers:
            observer.update(self)


# Ejemplo de un observador concreto que podrías usar
class EmailNotifier(Observer):
    def update(self, subject: Subject) -> None:
        # Aquí iría la lógica para reaccionar a la notificación.
        # Por ejemplo, si el sujeto es una OrdenDeTrabajo:
        # if isinstance(subject, OrdenTrabajo):
        #     print(f"EmailNotifier: La orden {subject.id} cambió a {subject.estado}")
        print("EmailNotifier: Reaccionando al evento y enviando un email.")