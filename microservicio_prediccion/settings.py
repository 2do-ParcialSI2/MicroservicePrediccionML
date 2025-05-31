"""
Configuración del microservicio - Similar a settings.py de Django
"""

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

# App info
APP_NAME = "🎓 Predictor de Rendimiento Académico"
VERSION = "1.0.0"
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Server configuration
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8000))

# Paths
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "ml_models"

# Files
DATASET_FILE = "notas_dataset.csv"
MODEL_FILE = "modelo_notas.pkl"

# Full paths
DATASET_PATH = DATA_DIR / DATASET_FILE
MODEL_PATH = MODELS_DIR / MODEL_FILE

# ML Model configuration
MODEL_CONFIG = {
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42
}

# Classification thresholds
THRESHOLD_LOW = 65.0
THRESHOLD_HIGH = 85.0

# Confidence thresholds
CONFIDENCE_HIGH_THRESHOLD = 5.0
CONFIDENCE_MEDIUM_THRESHOLD = 10.0

# Feature columns
FEATURE_COLUMNS = [
    'prom_tareas_t1', 'prom_examenes_t1', 'prom_part_t1', 'asistencia_t1',
    'prom_tareas_t2', 'prom_examenes_t2', 'prom_part_t2', 'asistencia_t2'
]

# Target column
TARGET_COLUMN = 'nota_final_t3'

# Contact info
CONTACT_INFO = {
    "name": "Sistema Educativo ML",
    "email": "ml@educativo.com"
} 