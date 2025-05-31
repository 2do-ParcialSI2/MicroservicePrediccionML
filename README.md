# 🎓 Predictor de Rendimiento Académico

Microservicio de Machine Learning integrado en Django para predecir el rendimiento académico de estudiantes basado en datos de trimestres anteriores.

## 📋 Descripción

Este microservicio utiliza **Random Forest** para predecir la **nota del tercer trimestre** basándose en el rendimiento de los **trimestres 1 y 2**. Incluye documentación completa con **Swagger UI** y está construido con **Django REST Framework**.

## 🚀 Características

- 🤖 **Machine Learning**: Modelo Random Forest para predicción de notas
- 📚 **Swagger UI**: Documentación interactiva de la API
- 🔄 **Django REST Framework**: API REST robusta y escalable
- 💾 **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- 📊 **Métricas**: Evaluación completa del modelo ML
- 🔍 **Health Check**: Monitoreo del estado del servicio

## 📁 Estructura del Proyecto

```
PrediccionML/                           # Proyecto Django principal
├── PrediccionML/                       # Configuración Django
│   ├── settings.py                     # Configuración principal
│   ├── urls.py                         # URLs principales
│   └── wsgi.py                         # WSGI config
├── microservicio_prediccion/           # App Django para ML
│   ├── data/                          # Dataset CSV
│   │   └── notas_dataset.csv          # Datos de entrenamiento
│   ├── ml_models/                     # Modelos entrenados
│   │   └── modelo_notas.pkl           # Modelo Random Forest
│   ├── scripts/                       # Scripts de entrenamiento
│   │   └── train_model.py             # Script para entrenar modelo
│   ├── views.py                       # API Views con DRF
│   ├── models.py                      # Esquemas Pydantic
│   ├── serializers.py                 # Validadores de datos
│   ├── services.py                    # Lógica de negocio ML
│   ├── settings.py                    # Configuración del microservicio
│   └── urls.py                        # URLs del microservicio
├── manage.py                          # Comando Django
├── requirements.txt                   # Dependencias
├── db.sqlite3                        # Base de datos SQLite
└── README.md                         # Este archivo
```

## 🛠️ Instalación

### 1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd PrediccionML
```

### 2. **Crear entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Entrenar el modelo ML** (solo primera vez)
```bash
cd microservicio_prediccion
python scripts/train_model.py
cd ..
```

### 5. **Ejecutar migraciones** (opcional)
```bash
python manage.py migrate
```

### 6. **Ejecutar el servidor**
```bash
python manage.py runserver
```

## 🌐 URLs de la API

### 📚 **Documentación**
- **Swagger UI**: http://localhost:8000/docs/
- **ReDoc**: http://localhost:8000/redoc/
- **Schema JSON**: http://localhost:8000/api/schema/

### 🎯 **Endpoints principales** (Base: `/api/v1/`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v1/predecir/` | 🎯 Predecir nota del T3 |
| `GET` | `/api/v1/modelo/info/` | 📊 Información del modelo |
| `POST` | `/api/v1/modelo/entrenar/` | 🤖 Entrenar/reentrenar modelo |
| `GET` | `/api/v1/health/` | 💚 Health check del servicio |

## 📖 Ejemplos de Uso

### 🎯 **Predecir Nota del Tercer Trimestre**

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/predecir/ \
  -H "Content-Type: application/json" \
  -d '{
    "prom_tareas_t1": 85.0,
    "prom_examenes_t1": 78.0,
    "prom_part_t1": 92.0,
    "asistencia_t1": 95.0,
    "prom_tareas_t2": 87.0,
    "prom_examenes_t2": 82.0,
    "prom_part_t2": 88.0,
    "asistencia_t2": 93.0
  }'
```

**Response:**
```json
{
  "nota_estimada": 84.7,
  "clasificacion": "medio",
  "nivel_confianza": "alto",
  "confianza_valor": 3.2,
  "mensaje": "Buen rendimiento. Se estima una nota de 84.7 (rendimiento medio) con alta confianza."
}
```

### 📊 **Información del Modelo**

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/modelo/info/
```

**Response:**
```json
{
  "cargado": true,
  "n_estimators": 100,
  "max_depth": 10,
  "min_samples_split": 5,
  "min_samples_leaf": 2,
  "n_features": 8,
  "feature_names": [
    "prom_tareas_t1", "prom_examenes_t1", "prom_part_t1", "asistencia_t1",
    "prom_tareas_t2", "prom_examenes_t2", "prom_part_t2", "asistencia_t2"
  ],
  "archivo_modelo": "C:\\...\\ml_models\\modelo_notas.pkl"
}
```

### 🤖 **Entrenar Modelo**

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/modelo/entrenar/ \
  -H "Content-Type: application/json" \
  -d '{"forzar_reentrenamiento": false}'
```

**Response:**
```json
{
  "mensaje": "Modelo entrenado exitosamente",
  "mse": 0.5615,
  "r2": 0.9913,
  "n_estimators": 100,
  "tamano_entrenamiento": 40,
  "tamano_prueba": 10,
  "cargado": true
}
```

### 💚 **Health Check**

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/health/
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-05-31T03:00:00Z",
  "modelo": {
    "cargado": true,
    "tipo": "RandomForestRegressor"
  },
  "dataset": {
    "existe": true,
    "filas": 50
  },
  "endpoints": [
    "/api/v1/predecir/",
    "/api/v1/modelo/info/",
    "/api/v1/modelo/entrenar/",
    "/api/v1/health/"
  ]
}
```

## 🗄️ Configuración de Base de Datos

### **SQLite (Por defecto - Desarrollo)**
Ya configurado. No requiere instalación adicional.

### **PostgreSQL (Producción)**

1. **Instalar PostgreSQL**
2. **Crear base de datos**:
   ```sql
   CREATE DATABASE prediccion_ml;
   ```
3. **Configurar variables de entorno**:
   ```bash
   export DB_NAME=prediccion_ml
   export DB_USER=postgres
   export DB_PASSWORD=tu_password
   export DB_HOST=localhost
   export DB_PORT=5432
   ```
4. **Descomentar configuración PostgreSQL** en `PrediccionML/settings.py`

## 🧪 Testing

### **Usar Swagger UI**
Visita http://localhost:8000/docs/ para probar los endpoints interactivamente.

### **Usar cURL**
Usa los ejemplos de arriba para probar desde línea de comandos.

### **Integración con Django**
```python
# En tu código Django
import requests

response = requests.post('http://localhost:8000/api/v1/predecir/', json={
    "prom_tareas_t1": 85.0,
    "prom_examenes_t1": 78.0,
    "prom_part_t1": 92.0,
    "asistencia_t1": 95.0,
    "prom_tareas_t2": 87.0,
    "prom_examenes_t2": 82.0,
    "prom_part_t2": 88.0,
    "asistencia_t2": 93.0
})

prediccion = response.json()
print(f"Nota estimada: {prediccion['nota_estimada']}")
```

## 📊 Dataset

El dataset incluye 50 registros sintéticos con:

**Características (Features):**
- `prom_tareas_t1/t2`: Promedio de tareas (0-100)
- `prom_examenes_t1/t2`: Promedio de exámenes (0-100)  
- `prom_part_t1/t2`: Promedio de participación (0-100)
- `asistencia_t1/t2`: Porcentaje de asistencia (0-100)

**Target:**
- `nota_final_t3`: Nota del tercer trimestre (0-100)

## 🤖 Modelo ML

- **Algoritmo**: Random Forest Regressor
- **Hiperparámetros**:
  - `n_estimators`: 100
  - `max_depth`: 10
  - `min_samples_split`: 5
  - `min_samples_leaf`: 2
- **Métricas**: R² > 99%, MSE < 1.0

## 🔧 Configuración Avanzada

### **Variables de Entorno**
```bash
# Base de datos
DB_NAME=prediccion_ml
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Aplicación  
DEBUG=True
SECRET_KEY=tu-secret-key
```

### **Personalizar Modelo ML**
Edita `microservicio_prediccion/settings.py`:
```python
MODEL_CONFIG = {
    'n_estimators': 200,
    'max_depth': 15,
    'min_samples_split': 3,
    'min_samples_leaf': 1,
    'random_state': 42
}
```

## 🚀 Despliegue

### **Desarrollo**
```bash
python manage.py runserver 0.0.0.0:8000
```

### **Producción**
1. Configurar PostgreSQL
2. Usar Gunicorn + Nginx
3. Configurar variables de entorno
4. Ejecutar migraciones

## 📚 Documentación Técnica

- **Django**: Framework web principal
- **Django REST Framework**: API REST
- **drf-spectacular**: Documentación OpenAPI/Swagger
- **scikit-learn**: Machine Learning
- **pandas**: Manipulación de datos
- **pydantic**: Validación de esquemas

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 📞 Contacto

- **Sistema Educativo ML**
- **Email**: ml@educativo.com

---

🎓 **¡Construido para el éxito académico!** 🚀 