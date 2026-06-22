"""
Orden Service - Gestiona órdenes usando Composite Pattern
"""

from Backend.patterns.composite import OrdenCompuesta, EtapaOtrabajo
from Backend.constants import TallerConstants
from datetime import timedelta


class OrdenService:
    """Servicio para crear y calcular órdenes de trabajo"""

    # Tiempos y costos estándar por etapa
    TIEMPOS_ETAPAS = {
        "biselado": TallerConstants.TIEMPO_BISELADO,
        "montaje": TallerConstants.TIEMPO_MONTAJE,
        "control_calidad": TallerConstants.TIEMPO_QC,
    }

    COSTOS_ETAPAS = {
        "biselado": 150.00,
        "montaje": 100.00,
        "control_calidad": 50.00,
    }

    @classmethod
    def crear_orden_estandar(cls, numero_orden: str) -> OrdenCompuesta:
        """Crea una orden estándar con las tres etapas"""
        orden = OrdenCompuesta(numero_orden)

        orden.agregar_etapa(EtapaOtrabajo(
            nombre="Biselado",
            duracion_horas=cls.TIEMPOS_ETAPAS["biselado"],
            costo=cls.COSTOS_ETAPAS["biselado"]
        ))

        orden.agregar_etapa(EtapaOtrabajo(
            nombre="Montaje",
            duracion_horas=cls.TIEMPOS_ETAPAS["montaje"],
            costo=cls.COSTOS_ETAPAS["montaje"]
        ))

        orden.agregar_etapa(EtapaOtrabajo(
            nombre="Control de Calidad",
            duracion_horas=cls.TIEMPOS_ETAPAS["control_calidad"],
            costo=cls.COSTOS_ETAPAS["control_calidad"]
        ))

        return orden

    @classmethod
    def crear_orden_personalizada(cls, numero_orden: str, etapas: list[dict]) -> OrdenCompuesta:
        """Crea una orden personalizada"""
        orden = OrdenCompuesta(numero_orden)

        for etapa_data in etapas:
            etapa = EtapaOtrabajo(
                nombre=etapa_data["nombre"],
                duracion_horas=etapa_data.get("duracion_horas", 1.0),
                costo=etapa_data.get("costo", 0.0)
            )
            orden.agregar_etapa(etapa)

        return orden

    @classmethod
    def calcular_resumen(cls, orden: OrdenCompuesta) -> dict:
        """Calcula resumen de la orden"""
        duracion = orden.obtener_duracion_estimada()
        horas = duracion.total_seconds() / 3600

        return {
            "numero_orden": orden.numero_orden,
            "cantidad_etapas": orden.obtener_cantidad_etapas(),
            "duracion_horas": round(horas, 2),
            "costo_total": round(orden.obtener_costo(), 2),
            "fecha_creacion": orden.created_at.isoformat(),
            "descripcion": orden.obtener_descripcion()
        }
