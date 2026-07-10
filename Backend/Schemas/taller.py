from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from ..Models.optica import EstadoOrden

# --- Schemas para Etapas de Trabajo ---

class EtapaTrabajoBase(BaseModel):
    etapa: str
    completado: bool = False
    tecnico_id: Optional[int] = None
    notas: Optional[str] = None

class EtapaTrabajoCreate(EtapaTrabajoBase):
    pass

class EtapaTrabajoResponse(EtapaTrabajoBase):
    id: int
    orden_id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True

# --- Schemas para Histórico de Estados ---

class HistoricoEstadosResponse(BaseModel):
    id: int
    estado_anterior: Optional[EstadoOrden] = None
    estado_nuevo: EstadoOrden
    tecnico_id: Optional[int] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# --- Schemas para Órdenes de Trabajo ---

class OrdenTrabajoBase(BaseModel):
    descripcion_trabajo: Optional[str] = None
    fecha_entrega_esperada: Optional[datetime] = None

class OrdenTrabajoCreate(OrdenTrabajoBase):
    venta_id: int

class OrdenTrabajoResponse(OrdenTrabajoBase):
    id: int
    venta_id: int
    estado: EstadoOrden
    etapas: List[EtapaTrabajoResponse] = []
    historico_estados: List[HistoricoEstadosResponse] = []

    class Config:
        from_attributes = True

class CambiarEstadoOrden(BaseModel):
    estado_nuevo: str
    tecnico_id: Optional[int] = None

# --- Schema para el endpoint de demo del Composite Pattern ---

class EtapaOrdenData(BaseModel):
    nombre: str
    tiempo_estimado: int