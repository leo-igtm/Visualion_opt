# 🔧 GUÍA DE IMPLEMENTACIÓN - Patrones Faltantes

---

## 1️⃣ CONSTANTS.PY - Eliminar Magic Numbers

### Crear archivo: `Backend/constants.py`

```python
# Backend/constants.py

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
```

### Usar en validadores

```python
# Backend/validators/optica_validators.py
from Backend.constants import PrescriptionConstants

class PrescriptionValidator:
    @staticmethod
    def validate_axis(value: int, field_name: str) -> int:
        if not (PrescriptionConstants.EJE_MIN <= value <= PrescriptionConstants.EJE_MAX):
            raise ValueError(f"{field_name} debe estar entre {PrescriptionConstants.EJE_MIN} y {PrescriptionConstants.EJE_MAX}°")
        return value
    
    # ... resto de métodos
```

---

## 2️⃣ SINGLETON PATTERN

### Crear archivo: `Backend/patterns/singleton.py`

```python
# Backend/patterns/singleton.py

"""
Singleton Pattern Implementation
Garantiza que una clase tenga solo una instancia
"""

from typing import Dict, Type, TypeVar
from threading import Lock

T = TypeVar('T')

class SingletonMeta(type):
    """
    Metaclase Singleton thread-safe
    Usa lock para evitar race conditions
    """
    _instances: Dict[Type, object] = {}
    _lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-check locking
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    Clase base para singletons
    """
    pass
```

### Aplicar a Database

```python
# Backend/database/dbconnections_opt.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from Backend.patterns.singleton import Singleton
import os

Base = declarative_base()

class DatabaseManager(Singleton):
    """
    Gestor de BD - Singleton
    Solo una instancia de conexión en toda la app
    """
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.DATABASE_URL = os.getenv(
                "DATABASE_URL",
                "postgresql+asyncpg://user:password@localhost/visualion"
            )
            self.engine = create_async_engine(
                self.DATABASE_URL,
                echo=False,
                pool_pre_ping=True
            )
            self.async_session = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            self._initialized = True
    
    async def get_db(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session
    
    async def close(self):
        await self.engine.dispose()


# Uso en FastAPI:
db_manager = DatabaseManager()

# En index.py:
@app.get("/api/data")
async def get_data(db: AsyncSession = Depends(db_manager.get_db)):
    # db es la misma instancia siempre
    pass
```

### Aplicar a Logger

```python
# Backend/logger/logger.py

import logging
from Backend.patterns.singleton import Singleton
from Backend.constants import LogConstants

class LoggerManager(Singleton):
    """
    Gestor de logs - Singleton
    """
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.logger = logging.getLogger("visualion_app")
            self.logger.setLevel(LogConstants.LOG_LEVEL)
            
            # File handler
            fh = logging.FileHandler(LogConstants.LOG_FILE)
            fh.setLevel(logging.DEBUG)
            
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(LogConstants.LOG_FORMAT)
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
            
            self._initialized = True
    
    def get_logger(self):
        return self.logger


# Uso:
logger_mgr = LoggerManager()
logger = logger_mgr.get_logger()

# En cualquier archivo:
logger.info("Turno creado")
logger.error("Error al procesar venta")
```

---

## 3️⃣ STRATEGY PATTERN

### Crear archivo: `Backend/patterns/strategy.py`

```python
# Backend/patterns/strategy.py

"""
Strategy Pattern Implementation
Define una familia de algoritmos, encapsula cada uno,
y hacen intercambiables
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from datetime import datetime

class PaymentStrategy(ABC):
    """
    Interfaz para estrategias de pago
    """
    
    @abstractmethod
    def validate(self, payment_data: dict) -> bool:
        """Valida los datos de pago"""
        pass
    
    @abstractmethod
    def process(self, amount: Decimal) -> dict:
        """Procesa el pago y retorna resultado"""
        pass
    
    @abstractmethod
    def get_fee(self, amount: Decimal) -> Decimal:
        """Calcula la tarifa o comisión"""
        pass


class CashPaymentStrategy(PaymentStrategy):
    """Pago en efectivo"""
    
    def validate(self, payment_data: dict) -> bool:
        # No requiere validación especial
        return True
    
    def process(self, amount: Decimal) -> dict:
        return {
            "status": "completed",
            "method": "cash",
            "amount": amount,
            "timestamp": datetime.now(),
            "reference": f"CASH_{datetime.now().timestamp()}"
        }
    
    def get_fee(self, amount: Decimal) -> Decimal:
        # Sin comisión en efectivo
        return Decimal("0.00")


class CreditCardPaymentStrategy(PaymentStrategy):
    """Pago con tarjeta de crédito"""
    
    def validate(self, payment_data: dict) -> bool:
        required = ["card_number", "cvv", "expiry"]
        return all(field in payment_data for field in required)
    
    def process(self, amount: Decimal) -> dict:
        # Aquí iría integración con Stripe/Mercado Pago
        return {
            "status": "pending",  # Requiere confirmación
            "method": "credit_card",
            "amount": amount,
            "timestamp": datetime.now(),
            "reference": f"CC_{datetime.now().timestamp()}"
        }
    
    def get_fee(self, amount: Decimal) -> Decimal:
        # 2.5% de comisión
        return amount * Decimal("0.025")


class TransferPaymentStrategy(PaymentStrategy):
    """Pago por transferencia bancaria"""
    
    def validate(self, payment_data: dict) -> bool:
        required = ["account_number", "bank_code"]
        return all(field in payment_data for field in required)
    
    def process(self, amount: Decimal) -> dict:
        return {
            "status": "pending",  # Requiere confirmación manual
            "method": "transfer",
            "amount": amount,
            "timestamp": datetime.now(),
            "reference": f"TRF_{datetime.now().timestamp()}"
        }
    
    def get_fee(self, amount: Decimal) -> Decimal:
        # $50 fijos
        return Decimal("50.00")


# Aplicar en Venta
# Backend/Models/optica.py - REFACTORIZADO

from Backend.patterns.strategy import PaymentStrategy

class Venta(Base):
    __tablename__ = 'ventas'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ... campos existentes
    
    @property
    def payment_strategy(self) -> PaymentStrategy:
        """Factory para obtener estrategia de pago"""
        strategies = {
            "efectivo": CashPaymentStrategy(),
            "tarjeta_credito": CreditCardPaymentStrategy(),
            "transferencia": TransferPaymentStrategy()
        }
        return strategies.get(self.estado_pago, CashPaymentStrategy())
    
    def procesar_pago(self, payment_data: dict):
        """Procesa pago usando estrategia"""
        strategy = self.payment_strategy
        
        if not strategy.validate(payment_data):
            raise ValueError("Datos de pago inválidos")
        
        fee = strategy.get_fee(self.total)
        result = strategy.process(self.total)
        
        return {
            "result": result,
            "fee": fee,
            "total_with_fee": self.total + fee
        }
```

---

## 4️⃣ OBSERVER PATTERN

### Crear archivo: `Backend/patterns/observer.py`

```python
# Backend/patterns/observer.py

"""
Observer Pattern Implementation
Define una dependencia de uno-a-muchos entre objetos
"""

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

class Observer(ABC):
    """Interfaz para observadores"""
    
    @abstractmethod
    def update(self, event: 'Event') -> None:
        """Llamado cuando ocurre un evento"""
        pass


class Event:
    """Representa un evento en el sistema"""
    
    def __init__(self, event_type: str, data: dict):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now()


class NotificationObserver(Observer):
    """Observador que envía notificaciones"""
    
    def update(self, event: Event) -> None:
        print(f"[NOTIFICATION] {event.event_type}: {event.data}")
        # Aquí iría el envío real de SMS/Email
        # from Backend.services.notification_service import notify
        # notify(event)


class LogObserver(Observer):
    """Observador que registra eventos en logs"""
    
    def update(self, event: Event) -> None:
        logger = LoggerManager().get_logger()
        logger.info(f"EVENT: {event.event_type} - Data: {event.data}")


class EventSubject:
    """Sujeto que notifica a observadores"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Suscribir observador"""
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Desuscribir observador"""
        self._observers.remove(observer)
    
    def notify(self, event: Event) -> None:
        """Notificar a todos los observadores"""
        for observer in self._observers:
            observer.update(event)
```

### Aplicar en Cambios de Estado

```python
# Backend/controllers/taller.py - REFACTORIZADO

from Backend.patterns.observer import Event, EventSubject, NotificationObserver, LogObserver

# Crear sujeto global
orden_subject = EventSubject()
orden_subject.attach(NotificationObserver())
orden_subject.attach(LogObserver())

@router.put("/ordenes/{orden_id}/estado")
async def cambiar_estado_orden(orden_id: int, datos: schemas.CambiarEstadoOrden, db: AsyncSession = Depends(get_db)):
    """Cambiar estado y notificar a observadores"""
    
    # ... código existente ...
    
    # Crear evento
    event = Event(
        event_type="orden_estado_cambio",
        data={
            "orden_id": orden_id,
            "estado_anterior": db_orden.estado,
            "estado_nuevo": datos.estado_nuevo,
            "tecnico_id": datos.tecnico_id
        }
    )
    
    # Notificar a todos los observadores
    orden_subject.notify(event)
    
    return db_orden
```

---

## 5️⃣ COMPOSITE PATTERN

### Crear archivo: `Backend/patterns/composite.py`

```python
# Backend/patterns/composite.py

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
        return f"Etapa: {self.nombre}"


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
        return f"Orden {self.numero_orden}:\n" + "\n".join(etapas_desc)


# Uso:
orden = OrdenCompuesta("ORD-2026-001")
orden.agregar_etapa(EtapaOtrabajo("Biselado", 2.0, 150.00))
orden.agregar_etapa(EtapaOtrabajo("Montaje", 1.5, 100.00))
orden.agregar_etapa(EtapaOtrabajo("QC", 0.5, 50.00))

print(f"Duración total: {orden.obtener_duracion_estimada()}")
print(f"Costo total: ${orden.obtener_costo()}")
```

---

## 6️⃣ OAUTH2 - GOOGLE + GITHUB

### Crear: `Backend/services/oauth_service.py`

```python
# Backend/services/oauth_service.py

"""
OAuth2 Service para autenticación con servicios externos
"""

import os
import httpx
from typing import Optional, Dict

class GoogleOAuthService:
    """Google OAuth2 Service"""
    
    CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/google/callback")
    
    @staticmethod
    def get_auth_url() -> str:
        """Retorna URL para autenticar"""
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={GoogleOAuthService.CLIENT_ID}&"
            f"redirect_uri={GoogleOAuthService.REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile"
        )
    
    @staticmethod
    async def verify_token(code: str) -> Optional[Dict]:
        """Verifica código y obtiene info del usuario"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": GoogleOAuthService.CLIENT_ID,
                    "client_secret": GoogleOAuthService.CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": GoogleOAuthService.REDIRECT_URI
                }
            )
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            
            # Obtener info del usuario
            id_token = data.get("id_token")
            
            return {
                "email": data.get("email"),
                "name": data.get("name"),
                "picture": data.get("picture"),
                "provider": "google"
            }


class GitHubOAuthService:
    """GitHub OAuth2 Service"""
    
    CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:3000/auth/github/callback")
    
    @staticmethod
    def get_auth_url() -> str:
        """Retorna URL para autenticar"""
        return (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={GitHubOAuthService.CLIENT_ID}&"
            f"redirect_uri={GitHubOAuthService.REDIRECT_URI}&"
            f"scope=user:email"
        )
    
    @staticmethod
    async def verify_token(code: str) -> Optional[Dict]:
        """Verifica código y obtiene info del usuario"""
        async with httpx.AsyncClient() as client:
            # Obtener access token
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": GitHubOAuthService.CLIENT_ID,
                    "client_secret": GitHubOAuthService.CLIENT_SECRET,
                    "code": code,
                },
                headers={"Accept": "application/json"}
            )
            
            if response.status_code != 200:
                return None
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            
            # Obtener info del usuario
            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_response.status_code != 200:
                return None
            
            user_data = user_response.json()
            
            return {
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "avatar_url": user_data.get("avatar_url"),
                "provider": "github"
            }
```

### Endpoints OAuth2

```python
# Backend/controllers/auth.py - AGREGAR ENDPOINTS

from Backend.services.oauth_service import GoogleOAuthService, GitHubOAuthService

@router.get("/oauth/google/url")
async def get_google_auth_url():
    """Retorna URL para autenticar con Google"""
    return {"url": GoogleOAuthService.get_auth_url()}


@router.post("/oauth/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Callback después de autenticación con Google"""
    
    user_info = await GoogleOAuthService.verify_token(code)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Google authentication failed")
    
    # Crear o obtener usuario
    query = select(Empleado).where(Empleado.email == user_info["email"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        # Crear nuevo usuario con Google
        user = Empleado(
            dni="GOOGLE_" + user_info["email"],
            nombre=user_info.get("name", ""),
            email=user_info["email"],
            usuario=user_info["email"],
            contraseña="OAUTH_GOOGLE",
            rol="empleado",
            legajo="OAUTH_" + str(datetime.now().timestamp())
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    # Generar JWT
    token = AuthService.create_jwt_token(user.id, user.usuario)
    
    return {"access_token": token, "user": {"id": user.id, "email": user.email}}


@router.get("/oauth/github/url")
async def get_github_auth_url():
    """Retorna URL para autenticar con GitHub"""
    return {"url": GitHubOAuthService.get_auth_url()}


@router.post("/oauth/github/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    """Callback después de autenticación con GitHub"""
    
    user_info = await GitHubOAuthService.verify_token(code)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="GitHub authentication failed")
    
    # Crear o obtener usuario
    query = select(Empleado).where(Empleado.email == user_info["email"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        user = Empleado(
            dni="GITHUB_" + str(user_info.get("name", "")),
            nombre=user_info.get("name", ""),
            email=user_info["email"],
            usuario=user_info.get("name", user_info["email"]),
            contraseña="OAUTH_GITHUB",
            rol="empleado",
            legajo="OAUTH_" + str(datetime.now().timestamp())
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    token = AuthService.create_jwt_token(user.id, user.usuario)
    
    return {"access_token": token, "user": {"id": user.id, "email": user.email}}
```

### Variables de Entorno

```bash
# .env - AGREGAR

# OAuth2 - Google
GOOGLE_CLIENT_ID=xxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxxx
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback

# OAuth2 - GitHub
GITHUB_CLIENT_ID=xxxx
GITHUB_CLIENT_SECRET=xxxx
GITHUB_REDIRECT_URI=http://localhost:3000/auth/github/callback
```

---

## 📋 PRÓXIMOS PASOS

1. Crear `Backend/constants.py` (2h)
2. Crear `Backend/patterns/singleton.py` (2h)
3. Crear `Backend/patterns/strategy.py` (3h)
4. Crear `Backend/patterns/observer.py` (3h)
5. Crear `Backend/patterns/composite.py` (4h)
6. Crear OAuth2 services (4h)
7. Testing (2h)

**Total**: ~20 horas de implementación

---

**Guía de Implementación: 2026-06-20**  
**Estado**: Listo para codificar
