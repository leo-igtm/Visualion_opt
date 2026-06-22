"""
Singleton Pattern Implementation
Garantiza que una clase tenga solo una instancia
"""

from typing import Dict, Type, TypeVar
from threading import Lock

T = TypeVar('T')


class SingletonMeta(type):
    """
    Metaclase Singleton thread-safe
    Usa lock para evitar race conditions
    """
    _instances: Dict[Type, object] = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-check locking
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    Clase base para singletons
    """
    pass
