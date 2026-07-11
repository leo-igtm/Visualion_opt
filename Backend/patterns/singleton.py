"""
Singleton Pattern Implementation
Garantiza que una clase tenga solo una instancia
"""

from threading import Lock 
from typing import Any, Dict

class SingletonMeta(type):
    """
    Metaclase Singleton que es segura para subprocesos (thread-safe).
    Utiliza un mecanismo de bloqueo para evitar "race conditions" cuando
    múltiples hilos intentan crear una instancia simultáneamente.
    """
    _instances : Dict[type,object]={}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any):
        with cls._lock:
            instance = cls._instances.get(cls)
            if instance is None:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
    
    
   

class Singleton(metaclass=SingletonMeta):
    """
    Clase base que cualquier otra clase puede heredar para convertirse en un Singleton.
    Al heredar de esta, automáticamente utilizará SingletonMeta para su creación.
    """
    def some_business_logic(self):
        """
        Método de ejemplo que puede ser sobrescrito por subclases.
        Representa la lógica de negocio que un Singleton podría tener.
        """
        pass
    def __init__(self):
        """
        Inicializa la instancia del Singleton.
        Se puede sobrescribir en las subclases, pero se recomienda llamar a super().__init__() para asegurar
        que la inicialización de la metaclase se realice correctamente.
        """
        pass