"""
Event Service - Gestiona observadores para eventos del sistema
"""

from Backend.patterns.observer import EventSubject, NotificationObserver, LogObserver


class EventService:
    """Servicio centralizado para manejar eventos"""

    _orden_subject: EventSubject | None = None

    @classmethod
    def get_orden_subject(cls) -> EventSubject:
        """Obtiene el sujeto de eventos de órdenes (Singleton)"""
        if cls._orden_subject is None:
            cls._orden_subject = EventSubject()
            # Agregar observadores por defecto
            cls._orden_subject.attach(LogObserver())
            cls._orden_subject.attach(NotificationObserver())
        return cls._orden_subject

    @classmethod
    def reset(cls):
        """Reset para testing"""
        cls._orden_subject = None
