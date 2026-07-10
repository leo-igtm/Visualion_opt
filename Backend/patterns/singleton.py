"""
Singleton Pattern Implementation
Garantiza que una clase tenga solo una instancia
"""

from typing import  TypeVar
import threading

T = TypeVar('T')
W

class SingletonMeta(type):
    """
    Metaclase Singleton que es segura para subprocesos (thread-safe).
    Utiliza un mecanismo de bloqueo para evitar "race conditions" cuando
    múltiples hilos intentan crear una instancia simultáneamente.
    """
    # Diccionario para almacenar la única instancia de cada clase Singleton.
    _instances: dict[type, object] = {}
    
    # Objeto de bloqueo para sincronizar hilos.
    _lock: threading.Lock = threading.Lock()

    def __call__(cls: type[T], *args, **kwargs) -> T:
        # Cuando se intenta crear un objeto (ej: MiClase()), Python llama a este método.
        # Adquirimos el bloqueo para asegurar que solo un hilo pueda ejecutar este bloque a la vez.
        with cls._lock():
            # Si la clase aún no tiene una instancia creada...
            if cls not in cls._instances:
                # ...creamos una nueva instancia llamando al __call__ de la clase padre (type).
                instance = super().__call__(*args, **kwargs)
                # ...y la guardamos en nuestro diccionario.
                cls._instances[cls] = instance
        # Devolvemos la instancia (ya sea la recién creada o la que ya existía).
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    """
    Clase base que cualquier otra clase puede heredar para convertirse en un Singleton.
    Al heredar de esta, automáticamente utilizará SingletonMeta para su creación.
    """
    pass
