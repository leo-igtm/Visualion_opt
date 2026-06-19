from sqlalchemy.ext.asyncio import AsyncSession
from Backend.Models.clinica import RecetaMedica
from sqlalchemy.future import select

#validacion de receta creacion de receta
class RecetaService:
    
    @staticmethod
    async def validar_receta(db: AsyncSession, receta_id: int) -> RecetaMedica:
        """Valida que la receta exista y esté asociada a un turno"""
        query = await db.execute(
            select(RecetaMedica).where(RecetaMedica.uuid == receta_id)
        )
        receta = query.scalars().first()
        if not receta:
            raise ValueError(f"Receta con ID {receta_id} no encontrada")
        if not receta.turno_id:
            raise ValueError(f"La receta con ID {receta_id} no está asociada a ningún turno")
        return receta
    
    
    @staticmethod
    async def validar_receta_para_venta(db: AsyncSession, receta_id: int) -> RecetaMedica:
        """Valida que la receta exista y esté asociada a un turno antes de crear una venta"""
        receta = await RecetaService.validar_receta(db, receta_id)
        return receta
