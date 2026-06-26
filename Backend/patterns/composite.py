from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Any

class ComponenteOrden(ABC):
    """
    La interfaz Componente declara operaciones comunes tanto para elementos
    simples como para los complejos de una composición.
    """
    @property
    def padre(self) -> ComponenteOrden | None:
        return self._padre

    @padre.setter
    def padre(self, padre: ComponenteOrden | None):
        self._padre = padre

    def agregar(self, componente: ComponenteOrden) -> None:
        pass

    def quitar(self, componente: ComponenteOrden) -> None:
        pass

    def es_compuesto(self) -> bool:
        return False

    @abstractmethod
    def obtener_tiempo(self) -> int:
        """Devuelve el tiempo estimado para completar la etapa (en minutos)."""
        pass

    @abstractmethod
    def mostrar(self) -> dict[str, Any]:
        """Devuelve una representación en diccionario de la estructura."""
        pass

class EtapaSimple(ComponenteOrden):
    """La clase 'Hoja' representa los objetos finales de una composición."""
    def __init__(self, nombre: str, tiempo: int):
        self.nombre = nombre
        self.tiempo = tiempo

    def obtener_tiempo(self) -> int:
        return self.tiempo

    def mostrar(self) -> dict[str, Any]:
        return {"nombre": self.nombre, "tiempo": self.tiempo, "tipo": "etapa"}

class Caja(ComponenteOrden):
    """La clase 'Composite' representa los componentes complejos que pueden tener hijos."""
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._hijos: List[ComponenteOrden] = []

    def agregar(self, componente: ComponenteOrden) -> None:
        self._hijos.append(componente)
        componente.padre = self

    def obtener_tiempo(self) -> int:
        return sum(hijo.obtener_tiempo() for hijo in self._hijos)

    def mostrar(self) -> dict[str, Any]:
        return {
            "nombre": self.nombre,
            "tipo": "caja",
            "tiempo_subtotal": self.obtener_tiempo(),
            "hijos": [hijo.mostrar() for hijo in self._hijos]
        }

# Alias para claridad semántica
Orden = Caja
Etapa = EtapaSimple