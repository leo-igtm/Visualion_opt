"""
Constantes globales para el proyecto Visualion_Opt
Centraliza magic numbers y valores hardcoded
"""

# ============== VALIDACIÓN DE RECETAS ==============
class PrescriptionConstants:
    # Validación de Esfera (OD/OI)
    ESFERA_MIN = -25.0
    ESFERA_MAX = 25.0
    ESFERA_STEP = 0.25  # Incremento mínimo

    # Validación de Cilindro (OD/OI)
    CILINDRO_MIN = -8.0
    CILINDRO_MAX = 0.0
    CILINDRO_STEP = 0.25

    # Validación de Eje (OD/OI)
    EJE_MIN = 0
    EJE_MAX = 180

    # Validación de Adición
    ADICION_MIN = 0.0
    ADICION_MAX = 4.0
    ADICION_STEP = 0.25

    # Distancia Pupilar (mm)
    DISTANCIA_PUPILAR_MIN = 54.0
    DISTANCIA_PUPILAR_MAX = 74.0


# ============== AUTENTICACIÓN ==============
class AuthConstants:
    # Bcrypt límite en bytes
    BCRYPT_MAX_PASSWORD_BYTES = 72

    # Token JWT
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    JWT_REFRESH_EXPIRATION_DAYS = 7

    # Validación de contraseña
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_DIGITS = True
    PASSWORD_REQUIRE_SPECIAL = False


# ============== TALLER ==============
class TallerConstants:
    # Estados válidos
    ESTADOS_ORDEN = [
        "recibida",
        "biselado",
        "montaje",
        "control_calidad",
        "listo"
    ]

    # Tiempos estimados (en horas)
    TIEMPO_BISELADO = 2
    TIEMPO_MONTAJE = 1.5
    TIEMPO_QC = 0.5


# ============== COMERCIAL ==============
class ComercialConstants:
    # Estados de pago
    ESTADO_PAGO_PENDIENTE = "pendiente"
    ESTADO_PAGO_PAGADO = "pagado"
    ESTADO_PAGO_FALLIDO = "fallido"

    # Métodos de pago
    METODOS_PAGO = [
        "efectivo",
        "tarjeta_credito",
        "tarjeta_debito",
        "transferencia",
        "cheque"
    ]

    # Stock
    STOCK_MINIMO_ALERTA = 10


# ============== NOTIFICACIONES ==============
class NotificationConstants:
    # Tipos de notificación
    TIPO_CONFIRMACION_TURNO = "confirmacion_turno"
    TIPO_RECORDATORIO_TURNO = "recordatorio_turno"
    TIPO_ESTADO_ORDEN = "estado_orden"
    TIPO_AVISO_RETIRO = "aviso_retiro"

    # Canales
    CANAL_SMS = "sms"
    CANAL_EMAIL = "email"
    CANAL_PUSH = "push"

    # Recordatorio 24h antes (en horas)
    RECORDATORIO_HORAS_ANTES = 24


# ============== SEGURIDAD ==============
class SecurityConstants:
    # Rate limiting
    RATE_LIMIT_REQUESTS = 100  # requests
    RATE_LIMIT_PERIOD = 3600   # segundos (1 hora)

    # Max intentos de login
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_TIME_MINUTES = 15


# ============== PAGINACIÓN ==============
class PaginationConstants:
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100


# ============== LOGS ==============
class LogConstants:
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = "logs/app.log"
