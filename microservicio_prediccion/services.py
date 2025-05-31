"""
Services - Lógica de negocio para ML (similar a servicios en Django)
"""

import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Optional, Tuple, Dict, Any
import logging

from .models import EstudianteRequest, PrediccionResponse
from .serializers import EstudianteSerializer, PrediccionSerializer, DatasetSerializer
from .settings import (
    MODEL_PATH, DATASET_PATH, MODEL_CONFIG, 
    FEATURE_COLUMNS, TARGET_COLUMN
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModeloService:
    """Servicio para manejo del modelo de Machine Learning"""
    
    def __init__(self):
        self.modelo: Optional[RandomForestRegressor] = None
        self.is_loaded = False
        self.feature_names = FEATURE_COLUMNS
        
    def cargar_modelo(self) -> bool:
        """
        Carga el modelo desde archivo
        
        Returns:
            bool: True si se cargó exitosamente
        """
        try:
            if MODEL_PATH.exists():
                with open(MODEL_PATH, 'rb') as f:
                    self.modelo = pickle.load(f)
                self.is_loaded = True
                logger.info(f"Modelo cargado desde {MODEL_PATH}")
                return True
            else:
                logger.warning(f"Archivo de modelo no encontrado: {MODEL_PATH}")
                return False
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            self.is_loaded = False
            return False
    
    def guardar_modelo(self) -> bool:
        """
        Guarda el modelo en archivo
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            # Crear directorio si no existe
            MODEL_PATH.parent.mkdir(exist_ok=True)
            
            with open(MODEL_PATH, 'wb') as f:
                pickle.dump(self.modelo, f)
            logger.info(f"Modelo guardado en {MODEL_PATH}")
            return True
        except Exception as e:
            logger.error(f"Error guardando modelo: {e}")
            return False
    
    def entrenar_modelo(self, forzar_reentrenamiento: bool = False) -> Dict[str, Any]:
        """
        Entrena el modelo con el dataset
        
        Args:
            forzar_reentrenamiento: Si True, reentrena aunque ya exista modelo
            
        Returns:
            Dict: Métricas del entrenamiento
        """
        # Si ya existe modelo y no se fuerza reentrenamiento
        if MODEL_PATH.exists() and not forzar_reentrenamiento:
            if self.cargar_modelo():
                return {"mensaje": "Modelo ya existe y fue cargado", "cargado": True}
        
        try:
            # Cargar y preparar datos
            df = pd.read_csv(DATASET_PATH)
            DatasetSerializer.validar_columnas(df)
            df = DatasetSerializer.limpiar_datos(df)
            
            # Preparar características y objetivo
            X = df[FEATURE_COLUMNS]
            y = df[TARGET_COLUMN]
            
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Crear y entrenar modelo
            self.modelo = RandomForestRegressor(**MODEL_CONFIG)
            self.modelo.fit(X_train, y_train)
            
            # Evaluar modelo
            y_pred = self.modelo.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Guardar modelo
            self.guardar_modelo()
            self.is_loaded = True
            
            metricas = {
                "mensaje": "Modelo entrenado exitosamente",
                "mse": float(mse),
                "r2": float(r2),
                "n_estimators": MODEL_CONFIG["n_estimators"],
                "tamano_entrenamiento": len(X_train),
                "tamano_prueba": len(X_test),
                "cargado": True
            }
            
            logger.info(f"Modelo entrenado - MSE: {mse:.4f}, R²: {r2:.4f}")
            return metricas
            
        except Exception as e:
            logger.error(f"Error entrenando modelo: {e}")
            raise ValueError(f"Error en entrenamiento: {str(e)}")
    
    def predecir(self, estudiante: EstudianteRequest) -> PrediccionResponse:
        """
        Realiza predicción para un estudiante
        
        Args:
            estudiante: Datos del estudiante
            
        Returns:
            PrediccionResponse: Predicción completa
            
        Raises:
            ValueError: Si el modelo no está cargado o hay error en predicción
        """
        if not self.is_loaded or self.modelo is None:
            # Intentar cargar modelo
            if not self.cargar_modelo():
                raise ValueError("Modelo no disponible. Debe entrenar primero.")
        
        try:
            # Convertir datos a array
            features = EstudianteSerializer.to_features_array(estudiante)
            
            # Realizar predicción
            prediccion = self.modelo.predict(features)[0]
            
            # Calcular confianza usando desviación estándar de los estimadores
            predicciones_arboles = [
                arbol.predict(features)[0] 
                for arbol in self.modelo.estimators_
            ]
            std_prediccion = np.std(predicciones_arboles)
            
            # Crear respuesta
            response = PrediccionSerializer.create_response(
                nota=float(prediccion),
                diferencia_std=float(std_prediccion)
            )
            
            logger.info(f"Predicción realizada: {prediccion:.2f} ± {std_prediccion:.2f}")
            return response
            
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            raise ValueError(f"Error realizando predicción: {str(e)}")
    
    def obtener_info_modelo(self) -> Dict[str, Any]:
        """
        Obtiene información del modelo actual
        
        Returns:
            Dict: Información del modelo
        """
        if not self.is_loaded or self.modelo is None:
            return {
                "cargado": False,
                "mensaje": "Modelo no cargado"
            }
        
        try:
            return {
                "cargado": True,
                "n_estimators": self.modelo.n_estimators,
                "max_depth": self.modelo.max_depth,
                "min_samples_split": self.modelo.min_samples_split,
                "min_samples_leaf": self.modelo.min_samples_leaf,
                "n_features": self.modelo.n_features_in_,
                "feature_names": self.feature_names,
                "archivo_modelo": str(MODEL_PATH)
            }
        except Exception as e:
            logger.error(f"Error obteniendo info del modelo: {e}")
            return {
                "cargado": False,
                "error": str(e)
            }


class DatasetService:
    """Servicio para manejo del dataset"""
    
    @staticmethod
    def verificar_dataset() -> Dict[str, Any]:
        """
        Verifica el estado del dataset
        
        Returns:
            Dict: Información del dataset
        """
        try:
            if not DATASET_PATH.exists():
                return {
                    "existe": False,
                    "mensaje": f"Dataset no encontrado en {DATASET_PATH}"
                }
            
            df = pd.read_csv(DATASET_PATH)
            DatasetSerializer.validar_columnas(df)
            df_clean = DatasetSerializer.limpiar_datos(df)
            
            return {
                "existe": True,
                "filas_total": len(df),
                "filas_validas": len(df_clean),
                "columnas": list(df.columns),
                "columnas_requeridas": FEATURE_COLUMNS + [TARGET_COLUMN],
                "archivo": str(DATASET_PATH)
            }
            
        except Exception as e:
            return {
                "existe": False,
                "error": str(e)
            }


# Instancia global del servicio
modelo_service = ModeloService() 