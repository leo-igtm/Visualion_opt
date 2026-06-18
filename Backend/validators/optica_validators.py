class PrescriptionValidator:
    @staticmethod
    def validate_axis(value: int, field_name: str) -> int:
        if not (0 <= value <= 180):
            raise ValueError(f"{field_name} debe estar entre 0 y 180°")
        return value

    @staticmethod
    def validate_sphere(value: float, field_name: str) -> float:
        if not (-25 <= value <= 25):
            raise ValueError(f"{field_name} debe estar entre -25 y +25")
        if round(value * 4) % 1 != 0:
            raise ValueError(f"{field_name} debe ser múltiplo de 0.25")
        return value

    @staticmethod
    def validate_cylinder(value: float, field_name: str) -> float:
        if not (-8 <= value <= 0):
            raise ValueError(f"{field_name} debe estar entre -8 y 0")
        if round(value * 4) % 1 != 0:
            raise ValueError(f"{field_name} debe ser múltiplo de 0.25")
        return value

    @staticmethod
    def validate_addition(value: float, field_name: str) -> float:
        if not (0 <= value <= 4):
            raise ValueError(f"{field_name} debe estar entre 0 y +4")
        if round(value * 4) % 1 != 0:
            raise ValueError(f"{field_name} debe ser múltiplo de 0.25")
        return value

    @staticmethod
    def validate_pupilary_distance(value: float | None) -> float | None:
        if value is not None and not (54 <= value <= 74):
            raise ValueError("Distancia pupilar debe estar entre 54 y 74 mm")
        return value
