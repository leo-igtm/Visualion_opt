from typing import List, Any
from ..Schemas.taller import EtapaOrdenData
from ..patterns.composite import Orden, EtapaSimple, Caja

class OrdenService:
    """
    Servicio para manejar la lógica de negocio de las órdenes de trabajo,
    especialmente para la demostración del patrón Composite.
    """

    @staticmethod
    def crear_orden_estandar(numero_orden: str) -> Orden:
        """Crea una estructura de orden estándar usando el patrón Composite."""
        orden = Orden(numero_orden)
        
        caja_montura = Caja("Armado de Montura")
        caja_montura.agregar(EtapaSimple("Biselado de Lentes", 30))
        caja_montura.agregar(EtapaSimple("Montaje en Armazón", 20))
        
        orden.agregar(caja_montura)
        orden.agregar(EtapaSimple("Control de Calidad Final", 15))
        
        return orden

    @staticmethod
    def crear_orden_personalizada(numero_orden: str, etapas: List[EtapaOrdenData]) -> Orden:
        """
        Crea una orden personalizada a partir de los datos de entrada.
        Aquí se soluciona el error de tipo, importando EtapaOrdenData
        desde `Backend.Schemas.taller`.
        """
        orden = Orden(numero_orden)
        for etapa_data in etapas:
            orden.agregar(EtapaSimple(etapa_data.nombre, etapa_data.tiempo_estimado))
        return orden

    @staticmethod
    def calcular_resumen(orden: Orden) -> dict[str, Any]:
        """Calcula el tiempo total y devuelve un resumen de la orden."""
        return {
            "numero_orden": orden.nombre,
            "tiempo_total_estimado": orden.obtener_tiempo(),
            "estructura": orden.mostrar()
        }