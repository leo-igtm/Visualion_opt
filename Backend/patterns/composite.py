"""
Composite Pattern Implementation
Compone objetos en estructuras de árbol
"""

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta


class OrdenComponente(ABC):
    """Componente base para órdenes"""

    @abstractmethod
    def obtener_duracion_estimada(self) -> timedelta:
        """Retorna duración estimada"""
        pass

    @abstractmethod
    def obtener_costo(self) -> float:
        """Retorna costo estimado"""
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Retorna descripción"""
        pass


class EtapaOtrabajo(OrdenComponente):
    """Etapa individual (hoja en el árbol)"""

    def __init__(self, nombre: str, duracion_horas: float, costo: float):
        self.nombre = nombre
        self.duracion_horas = duracion_horas
        self.costo = costo
        self.completada = False

    def obtener_duracion_estimada(self) -> timedelta:
        return timedelta(hours=self.duracion_horas)

    def obtener_costo(self) -> float:
        return self.costo

    def obtener_descripcion(self) -> str:
        return f"Etapa: {self.nombre} ({self.duracion_horas}h)"

    def marcar_completada(self):
        self.completada = True

    def __repr__(self):
        return f"Etapa({self.nombre}, {self.duracion_horas}h, ${self.costo})"


class OrdenCompuesta(OrdenComponente):
    """Orden que agrupa múltiples etapas (composite)"""

    def __init__(self, numero_orden: str):
        self.numero_orden = numero_orden
        self.etapas: List[OrdenComponente] = []
        self.created_at = datetime.now()

    def agregar_etapa(self, etapa: OrdenComponente) -> None:
        """Agregar etapa a la orden"""
        self.etapas.append(etapa)

    def remover_etapa(self, etapa: OrdenComponente) -> None:
        """Remover etapa de la orden"""
        if etapa in self.etapas:
            self.etapas.remove(etapa)

    def obtener_duracion_estimada(self) -> timedelta:
        """Suma duraciones de todas las etapas"""
        total = timedelta()
        for etapa in self.etapas:
            total += etapa.obtener_duracion_estimada()
        return total

    def obtener_costo(self) -> float:
        """Suma costos de todas las etapas"""
        return sum(etapa.obtener_costo() for etapa in self.etapas)

    def obtener_descripcion(self) -> str:
        """Describe todas las etapas"""
        etapas_desc = [etapa.obtener_descripcion() for etapa in self.etapas]
        return f"Orden {self.numero_orden}:\n  " + "\n  ".join(etapas_desc)

    def obtener_cantidad_etapas(self) -> int:
        """Retorna cantidad total de etapas"""
        return len(self.etapas)

    def __repr__(self):
        return f"Orden({self.numero_orden}, {len(self.etapas)} etapas)"
