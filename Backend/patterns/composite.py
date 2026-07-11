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
        componente.padre = self

        pass

    def quitar(self, componente: ComponenteOrden) -> None:
        componente.padre = None
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

class OrdenCompuesta(Caja):
    """La clase 'OrdenCompuesta' representa la orden completa, que puede contener múltiples cajas y etapas."""
    def __init__(self, nombre: str):
        super().__init__(nombre)
        self.nombre = nombre

    def obtener_tiempo(self) -> int:
        return sum(hijo.obtener_tiempo() for hijo in self._hijos)

    def mostrar(self) -> dict[str, Any]:
        return {
            "nombre": self.nombre,
            "tipo": "orden",
            "tiempo_subtotal": self.obtener_tiempo(),
            "hijos": [hijo.mostrar() for hijo in self._hijos]
        }

class EtapaOtrabajo(EtapaSimple):
    """Clase que representa una etapa de trabajo específica dentro de una orden."""
    def __init__(self, nombre: str, tiempo: int):
        super().__init__(nombre, tiempo)
        self.nombre = nombre
        self.tiempo = tiempo
        self.padre = None
        self._hijos: List[ComponenteOrden] = []
        
    def agregar_etapa(self, etapa: EtapaSimple) -> None:
        self._hijos.append(etapa)
        etapa.padre = self
        
        



# Alias para claridad semántica
Orden = Caja
Etapa = EtapaSimple