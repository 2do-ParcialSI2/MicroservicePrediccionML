"""
Modelos/Esquemas Pydantic - Similar a models.py de Django
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class EstudianteRequest(BaseModel):
    """Esquema para datos de entrada del estudiante"""
    
    # Primer trimestre
    prom_tareas_t1: float = Field(
        ..., 
        ge=0, le=100,
        description="Promedio de tareas del primer trimestre (0-100)"
    )
    prom_examenes_t1: float = Field(
        ..., 
        ge=0, le=100,
        description="Promedio de exámenes del primer trimestre (0-100)"
    )
    prom_part_t1: float = Field(
        ..., 
        ge=0, le=100,
        description="Promedio de participación del primer trimestre (0-100)"
    )
    asistencia_t1: float = Field(
        ..., 
        ge=0, le=100,
        description="Porcentaje de asistencia del primer trimestre (0-100)"
    )
    
    # Segundo trimestre
    prom_tareas_t2: float = Field(
        ..., 
        ge=0, le=100,
        description="Promedio de tareas del segundo trimestre (0-100)"
    )
    prom_examenes_t2: float = Field(
        ..., 
        ge=0, le=100,
        description="Promedio de exámenes del segundo trimestre (0-100)"
    )
    prom_part_t2: float = Field(
        ..., 
        ge=0, le=100,
        description="Promedio de participación del segundo trimestre (0-100)"
    )
    asistencia_t2: float = Field(
        ..., 
        ge=0, le=100,
        description="Porcentaje de asistencia del segundo trimestre (0-100)"
    )

    @validator("*", pre=True)
    def validar_numeros(cls, value):
        """Valida que todos los valores sean números válidos"""
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError("Todos los valores deben ser números válidos")


class PrediccionResponse(BaseModel):
    """Esquema para respuesta de predicción"""
    
    nota_estimada: float = Field(
        description="Nota estimada para el tercer trimestre (0-100)"
    )
    clasificacion: str = Field(
        description="Clasificación del rendimiento: 'bajo', 'medio' o 'alto'"
    )
    nivel_confianza: str = Field(
        description="Nivel de confianza: 'bajo', 'medio' o 'alto'"
    )
    confianza_valor: float = Field(
        description="Valor numérico de confianza (diferencia estándar)"
    )
    mensaje: str = Field(
        description="Mensaje descriptivo de la predicción"
    )


class ErrorResponse(BaseModel):
    """Esquema para respuesta de error"""
    
    error: str = Field(
        description="Mensaje de error"
    )
    detalle: Optional[str] = Field(
        None,
        description="Detalle específico del error"
    )
    codigo: Optional[int] = Field(
        None,
        description="Código de error"
    )


class HealthResponse(BaseModel):
    """Esquema para respuesta de health check"""
    
    status: str = Field(
        description="Estado del servicio"
    )
    timestamp: str = Field(
        description="Timestamp del check"
    )
    version: str = Field(
        description="Versión del servicio"
    )
    modelo_cargado: bool = Field(
        description="Indica si el modelo ML está cargado"
    ) 