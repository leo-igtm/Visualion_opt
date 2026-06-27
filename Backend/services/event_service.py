from ..patterns.observer import Subject

class EventService:
    """
    Servicio Singleton para gestionar los 'sujetos' de eventos en la aplicación.
    """
    _orden_subject = Subject()

    @staticmethod
    def get_orden_subject() -> Subject:
        return EventService._orden_subject