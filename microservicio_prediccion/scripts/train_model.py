#!/usr/bin/env python3
"""
Script para entrenar el modelo - Separado para facilitar mantenimiento
"""

import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from services import modelo_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Función principal para entrenar el modelo"""
    try:
        logger.info("🤖 Iniciando entrenamiento del modelo...")
        
        # Entrenar modelo
        resultado = modelo_service.entrenar_modelo(forzar_reentrenamiento=True)
        
        logger.info("✅ Entrenamiento completado exitosamente!")
        logger.info(f"📊 Métricas: MSE={resultado.get('mse', 'N/A'):.4f}, R²={resultado.get('r2', 'N/A'):.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en entrenamiento: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 