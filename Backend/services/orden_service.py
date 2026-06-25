"""
Orden Service - gestiona ordenes usando Composite Pattern.
"""

from typing import ClassVar, NotRequired, TypedDict

from Backend.constants import TallerConstants
from Backend.patterns.composite import EtapaOtrabajo, OrdenCompuesta


class EtapaOrdenData(TypedDict):
    nombre: str
    duracion_horas: NotRequired[float]
    costo: NotRequired[float]


class OrdenResumen(TypedDict):
    numero_orden: str
    cantidad_etapas: int
    duracion_horas: float
    costo_total: float
    fecha_creacion: str
    descripcion: str


class OrdenService:
    """Servicio para crear y calcular ordenes de trabajo."""

    TIEMPOS_ETAPAS: ClassVar[dict[str, float]] = {
        "biselado": float(TallerConstants.TIEMPO_BISELADO),
        "montaje": float(TallerConstants.TIEMPO_MONTAJE),
        "control_calidad": float(TallerConstants.TIEMPO_QC),
    }

    COSTOS_ETAPAS: ClassVar[dict[str, float]] = {
        "biselado": 150.00,
        "montaje": 100.00,
        "control_calidad": 50.00,
    }

    @classmethod
    def crear_orden_estandar(cls, numero_orden: str) -> OrdenCompuesta:
        """Crea una orden estandar con las tres etapas."""
        cls._validar_numero_orden(numero_orden)
        orden = OrdenCompuesta(numero_orden)

        for clave, nombre in (
            ("biselado", "Biselado"),
            ("montaje", "Montaje"),
            ("control_calidad", "Control de Calidad"),
        ):
            orden.agregar_etapa(
                EtapaOtrabajo(
                    nombre=nombre,
                    duracion_horas=cls.TIEMPOS_ETAPAS[clave],
                    costo=cls.COSTOS_ETAPAS[clave],
                )
            )

        return orden

    @classmethod
    def crear_orden_personalizada(
        cls,
        numero_orden: str,
        etapas: list[EtapaOrdenData],
    ) -> OrdenCompuesta:
        """Crea una orden personalizada."""
        cls._validar_numero_orden(numero_orden)
        if not etapas:
            raise ValueError("La orden debe incluir al menos una etapa")

        orden = OrdenCompuesta(numero_orden)

        for etapa_data in etapas:
            nombre = etapa_data.get("nombre")
            if not nombre or not nombre.strip():
                raise ValueError("Cada etapa debe incluir un nombre")

            duracion_horas = float(etapa_data.get("duracion_horas", 1.0))
            costo = float(etapa_data.get("costo", 0.0))
            if duracion_horas <= 0:
                raise ValueError("La duracion de una etapa debe ser mayor a cero")
            if costo < 0:
                raise ValueError("El costo de una etapa no puede ser negativo")

            orden.agregar_etapa(
                EtapaOtrabajo(
                    nombre=nombre.strip(),
                    duracion_horas=duracion_horas,
                    costo=costo,
                )
            )

        return orden

    @classmethod
    def calcular_resumen(cls, orden: OrdenCompuesta) -> OrdenResumen:
        """Calcula resumen de la orden."""
        duracion = orden.obtener_duracion_estimada()
        horas = duracion.total_seconds() / 3600

        return {
            "numero_orden": orden.numero_orden,
            "cantidad_etapas": orden.obtener_cantidad_etapas(),
            "duracion_horas": round(horas, 2),
            "costo_total": round(orden.obtener_costo(), 2),
            "fecha_creacion": orden.created_at.isoformat(),
            "descripcion": orden.obtener_descripcion(),
        }

    @staticmethod
    def _validar_numero_orden(numero_orden: str) -> None:
        if not numero_orden or not numero_orden.strip():
            raise ValueError("El numero de orden es requerido")
