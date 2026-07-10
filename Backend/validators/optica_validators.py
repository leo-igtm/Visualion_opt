from ..constants import PrescriptionConstants


class PrescriptionValidator:
    @staticmethod
    def validate_axis(value: int, field_name: str) -> int:
        if not (PrescriptionConstants.EJE_MIN <= value <= PrescriptionConstants.EJE_MAX):
            raise ValueError(f"{field_name} debe estar entre {PrescriptionConstants.EJE_MIN} y {PrescriptionConstants.EJE_MAX}°")
        return value

    @staticmethod
    def validate_sphere(value: float, field_name: str) -> float:
        if not (PrescriptionConstants.ESFERA_MIN <= value <= PrescriptionConstants.ESFERA_MAX):
            raise ValueError(f"{field_name} debe estar entre {PrescriptionConstants.ESFERA_MIN} y +{PrescriptionConstants.ESFERA_MAX}")
        if round(value * 4) % 1 != 0:
            raise ValueError(f"{field_name} debe ser múltiplo de {PrescriptionConstants.ESFERA_STEP}")
        return value

    @staticmethod
    def validate_cylinder(value: float, field_name: str) -> float:
        if not (PrescriptionConstants.CILINDRO_MIN <= value <= PrescriptionConstants.CILINDRO_MAX):
            raise ValueError(f"{field_name} debe estar entre {PrescriptionConstants.CILINDRO_MIN} y {PrescriptionConstants.CILINDRO_MAX}")
        if round(value * 4) % 1 != 0:
            raise ValueError(f"{field_name} debe ser múltiplo de {PrescriptionConstants.CILINDRO_STEP}")
        return value

    @staticmethod
    def validate_addition(value: float, field_name: str) -> float:
        if not (PrescriptionConstants.ADICION_MIN <= value <= PrescriptionConstants.ADICION_MAX):
            raise ValueError(f"{field_name} debe estar entre {PrescriptionConstants.ADICION_MIN} y +{PrescriptionConstants.ADICION_MAX}")
        if round(value * 4) % 1 != 0:
            raise ValueError(f"{field_name} debe ser múltiplo de {PrescriptionConstants.ADICION_STEP}")
        return value

    @staticmethod
    def validate_pupilary_distance(value: float | None) -> float | None:
        if value is not None and not (PrescriptionConstants.DISTANCIA_PUPILAR_MIN <= value <= PrescriptionConstants.DISTANCIA_PUPILAR_MAX):
            raise ValueError(f"Distancia pupilar debe estar entre {PrescriptionConstants.DISTANCIA_PUPILAR_MIN} y {PrescriptionConstants.DISTANCIA_PUPILAR_MAX} mm")
        return value
