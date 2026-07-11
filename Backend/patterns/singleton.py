"""
Singleton Pattern Implementation
Garantiza que una clase tenga solo una instancia
"""

from threading import Lock 
from typing import Dict


class SingletonMeta(type):
    """
    Metaclase Singleton que es segura para subprocesos (thread-safe).
    Utiliza un mecanismo de bloqueo para evitar "race conditions" cuando
    múltiples hilos intentan crear una instancia simultáneamente.
    """
    _instances : Dict[type,object]={}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]  
    

   

class Singleton(metaclass=SingletonMeta):
    """
    Clase base que cualquier otra clase puede heredar para convertirse en un Singleton.
    Al heredar de esta, automáticamente utilizará SingletonMeta para su creación.
    """


    pass

if __name__ == "__main__":
    # Ejemplo de uso del patrón Singleton
    class MySingleton(Singleton):
        def __init__(self, value):
            self.value = value

    singleton1 = MySingleton(10)

    print(singleton1.value)  # Salida: 10
