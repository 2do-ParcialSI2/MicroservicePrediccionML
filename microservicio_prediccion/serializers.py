"""
Serializers - Validación y transformación de datos (similar a Django serializers)
"""

import numpy as np
from typing import Dict, Any, List
from .models import EstudianteRequest, PrediccionResponse
from .settings import FEATURE_COLUMNS, THRESHOLD_LOW, THRESHOLD_HIGH, TARGET_COLUMN


class EstudianteSerializer:
    """Serializer para datos del estudiante"""
    
    @staticmethod
    def validar_entrada(data: Dict[str, Any]) -> EstudianteRequest:
        """
        Valida los datos de entrada del estudiante
        
        Args:
            data: Diccionario con los datos del estudiante
            
        Returns:
            EstudianteRequest: Objeto validado
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        try:
            return EstudianteRequest(**data)
        except Exception as e:
            raise ValueError(f"Datos inválidos: {str(e)}")
    
    @staticmethod
    def to_features_array(estudiante: EstudianteRequest) -> np.ndarray:
        """
        Convierte los datos del estudiante a array para el modelo
        
        Args:
            estudiante: Datos validados del estudiante
            
        Returns:
            np.ndarray: Array con las características en el orden correcto
        """
        features = [
            estudiante.prom_tareas_t1,
            estudiante.prom_examenes_t1,
            estudiante.prom_part_t1,
            estudiante.asistencia_t1,
            estudiante.prom_tareas_t2,
            estudiante.prom_examenes_t2,
            estudiante.prom_part_t2,
            estudiante.asistencia_t2
        ]
        return np.array(features).reshape(1, -1)
    
    @staticmethod
    def get_feature_names() -> List[str]:
        """Retorna los nombres de las características"""
        return FEATURE_COLUMNS.copy()


class PrediccionSerializer:
    """Serializer para respuestas de predicción"""
    
    @staticmethod
    def clasificar_nota(nota: float) -> str:
        """
        Clasifica la nota en categorías
        
        Args:
            nota: Nota numérica (0-100)
            
        Returns:
            str: Clasificación ('bajo', 'medio', 'alto')
        """
        if nota < THRESHOLD_LOW:
            return "bajo"
        elif nota < THRESHOLD_HIGH:
            return "medio"
        else:
            return "alto"
    
    @staticmethod
    def evaluar_confianza(diferencia_std: float) -> str:
        """
        Evalúa el nivel de confianza basado en la diferencia estándar
        
        Args:
            diferencia_std: Diferencia estándar de la predicción
            
        Returns:
            str: Nivel de confianza ('alto', 'medio', 'bajo')
        """
        from .settings import CONFIDENCE_HIGH_THRESHOLD, CONFIDENCE_MEDIUM_THRESHOLD
        
        if diferencia_std <= CONFIDENCE_HIGH_THRESHOLD:
            return "alto"
        elif diferencia_std <= CONFIDENCE_MEDIUM_THRESHOLD:
            return "medio"
        else:
            return "bajo"
    
    @staticmethod
    def generar_mensaje(nota: float, clasificacion: str, confianza: str) -> str:
        """
        Genera mensaje descriptivo de la predicción
        
        Args:
            nota: Nota estimada
            clasificacion: Clasificación del rendimiento
            confianza: Nivel de confianza
            
        Returns:
            str: Mensaje descriptivo
        """
        mensajes_base = {
            "alto": f"Excelente trabajo! Se estima una nota de {nota:.1f} (rendimiento alto)",
            "medio": f"Buen rendimiento. Se estima una nota de {nota:.1f} (rendimiento medio)",
            "bajo": f"Hay oportunidades de mejora. Se estima una nota de {nota:.1f} (rendimiento bajo)"
        }
        
        confianza_texto = {
            "alto": "con alta confianza",
            "medio": "con confianza moderada", 
            "bajo": "con baja confianza"
        }
        
        mensaje_base = mensajes_base.get(clasificacion, f"Se estima una nota de {nota:.1f}")
        nivel_confianza = confianza_texto.get(confianza, "")
        
        return f"{mensaje_base} {nivel_confianza}."
    
    @staticmethod
    def create_response(
        nota: float, 
        diferencia_std: float
    ) -> PrediccionResponse:
        """
        Crea la respuesta completa de predicción
        
        Args:
            nota: Nota estimada
            diferencia_std: Diferencia estándar
            
        Returns:
            PrediccionResponse: Respuesta completa
        """
        clasificacion = PrediccionSerializer.clasificar_nota(nota)
        nivel_confianza = PrediccionSerializer.evaluar_confianza(diferencia_std)
        mensaje = PrediccionSerializer.generar_mensaje(nota, clasificacion, nivel_confianza)
        
        return PrediccionResponse(
            nota_estimada=round(nota, 2),
            clasificacion=clasificacion,
            nivel_confianza=nivel_confianza,
            confianza_valor=round(diferencia_std, 2),
            mensaje=mensaje
        )


class DatasetSerializer:
    """Serializer para manejo del dataset"""
    
    @staticmethod
    def validar_columnas(df) -> bool:
        """
        Valida que el dataset tenga las columnas necesarias
        
        Args:
            df: DataFrame a validar
            
        Returns:
            bool: True si es válido
            
        Raises:
            ValueError: Si faltan columnas
        """
        from .settings import TARGET_COLUMN
        
        required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
        missing_columns = set(required_columns) - set(df.columns)
        
        if missing_columns:
            raise ValueError(f"Faltan columnas en el dataset: {missing_columns}")
        
        return True
    
    @staticmethod
    def limpiar_datos(df):
        """
        Limpia y prepara los datos del dataset
        
        Args:
            df: DataFrame a limpiar
            
        Returns:
            DataFrame: Datos limpios
        """
        # Eliminar filas con valores nulos
        df_clean = df.dropna()
        
        # Validar rangos de valores
        for col in FEATURE_COLUMNS + [TARGET_COLUMN]:
            if col in df_clean.columns:
                df_clean = df_clean[
                    (df_clean[col] >= 0) & (df_clean[col] <= 100)
                ]
        
        return df_clean 