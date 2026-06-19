from Backend.Models.taller import EstadoOrden, OrdenTrabajo


class OrdenTrabajoValidator:
    """Validator for OrdenTrabajo state machine transitions"""

    TRANSICIONES_VALIDAS = {
        EstadoOrden.RECIBIDA: [EstadoOrden.BISELADO],
        EstadoOrden.BISELADO: [EstadoOrden.MONTAJE],
        EstadoOrden.MONTAJE: [EstadoOrden.CONTROL_CALIDAD],
        EstadoOrden.CONTROL_CALIDAD: [EstadoOrden.LISTO, EstadoOrden.MONTAJE],
        EstadoOrden.LISTO: [],
    }

    @staticmethod
    def puede_transicionar(estado_actual: str, estado_nuevo: str) -> bool:
        """Check if transition is valid"""
        if estado_actual not in OrdenTrabajoValidator.TRANSICIONES_VALIDAS:
            return False
        return estado_nuevo in OrdenTrabajoValidator.TRANSICIONES_VALIDAS[estado_actual]

    @staticmethod
    def obtener_transiciones_permitidas(estado_actual: str) -> list[str]:
        """Get list of allowed next states"""
        return OrdenTrabajoValidator.TRANSICIONES_VALIDAS.get(estado_actual, [])

    @staticmethod
    def validar_transicion(orden: OrdenTrabajo, nuevo_estado: str) -> tuple[bool, str | None]:
        """Validate state transition and return (is_valid, error_message)"""
        if nuevo_estado not in EstadoOrden.all_estados():
            return False, f"Estado inválido: {nuevo_estado}"

        if orden.estado == nuevo_estado:
            return False, f"La orden ya está en estado: {orden.estado}"

        if not OrdenTrabajoValidator.puede_transicionar(orden.estado, nuevo_estado):
            transiciones_permitidas = OrdenTrabajoValidator.obtener_transiciones_permitidas(orden.estado)
            if not transiciones_permitidas:
                return False, f"No hay transiciones permitidas desde estado: {orden.estado}"
            return False, f"Transición no permitida de {orden.estado} a {nuevo_estado}. Transiciones permitidas: {', '.join(transiciones_permitidas)}"

        return True, None
