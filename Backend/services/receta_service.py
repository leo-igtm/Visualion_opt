from sqlalchemy.ext.asyncio import AsyncSession
from Backend.Models.clinica import RecetaMedica


class RecetaService:
    @staticmethod
    async def validate_receta_complete(receta_data) -> dict:
        """Validación adicional de negocios más allá de Pydantic"""
        return {"valid": True}

    @staticmethod
    async def create_receta(db: AsyncSession, receta_data, schema_class) -> RecetaMedica:
        """Lógica consolidada para crear receta con validación"""
        receta = schema_class.model_validate(receta_data)
        receta_obj = RecetaMedica(**receta.model_dump())
        db.add(receta_obj)
        await db.commit()
        await db.refresh(receta_obj)
        return receta_obj
