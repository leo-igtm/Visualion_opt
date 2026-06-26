from __future__ import annotations
from typing import TYPE_CHECKING
from Backend.Models.optica import EstadoOrden

if TYPE_CHECKING:
    from Backend.Models.optica import OrdenTrabajo

class OrdenTrabajoValidator:
    """
    Clase estática para validar la lógica de negocio de las Órdenes de Trabajo.
    """

    # Define la máquina de estados para las transiciones válidas.
    TRANSICIONES_VALIDAS: dict[EstadoOrden, list[EstadoOrden]] = {
        EstadoOrden.RECIBIDA: [EstadoOrden.EN_PROCESO, EstadoOrden.CANCELADA],
        EstadoOrden.EN_PROCESO: [EstadoOrden.LISTA_PARA_ENTREGA, EstadoOrden.CANCELADA],
        EstadoOrden.LISTA_PARA_ENTREGA: [EstadoOrden.ENTREGADA, EstadoOrden.CANCELADA],
        EstadoOrden.ENTREGADA: [],  # Estado final
        EstadoOrden.CANCELADA: [], # Estado final
    }

    @staticmethod
    def validar_transicion(orden: "OrdenTrabajo", nuevo_estado: EstadoOrden) -> tuple[bool, str | None]:
        """Valida si la transición de un estado a otro es permitida."""
        estado_actual = orden.estado
        if nuevo_estado in OrdenTrabajoValidator.TRANSICIONES_VALIDAS.get(estado_actual, []):
            return True, None
        
        estados_permitidos = [e.value for e in OrdenTrabajoValidator.TRANSICIONES_VALIDAS.get(estado_actual, [])]
        mensaje = f"Transición de estado no válida de '{estado_actual.value}' a '{nuevo_estado.value}'. Estados permitidos: {estados_permitidos or 'ninguno'}."
        return False, mensaje