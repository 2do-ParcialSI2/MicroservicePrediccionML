"""
Views - API Views usando Django REST Framework
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import logging

from .services import modelo_service, DatasetService
from .serializers import EstudianteSerializer, PrediccionSerializer
from .models import EstudianteRequest

logger = logging.getLogger(__name__)


class PrediccionView(APIView):
    """
    API View para predicción de notas académicas
    """
    
    @extend_schema(
        operation_id='predecir_nota',
        summary='🎯 Predecir Nota del Tercer Trimestre',
        description="""
        **Predice la nota del tercer trimestre** basándose en el rendimiento de los primeros dos trimestres.
        
        Utiliza un modelo de Random Forest entrenado con datos históricos para estimar el rendimiento futuro.
        """,
        tags=['Predicción'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'prom_tareas_t1': {'type': 'number', 'description': 'Promedio tareas T1 (0-100)'},
                    'prom_examenes_t1': {'type': 'number', 'description': 'Promedio exámenes T1 (0-100)'},
                    'prom_part_t1': {'type': 'number', 'description': 'Promedio participación T1 (0-100)'},
                    'asistencia_t1': {'type': 'number', 'description': 'Asistencia T1 (0-100)'},
                    'prom_tareas_t2': {'type': 'number', 'description': 'Promedio tareas T2 (0-100)'},
                    'prom_examenes_t2': {'type': 'number', 'description': 'Promedio exámenes T2 (0-100)'},
                    'prom_part_t2': {'type': 'number', 'description': 'Promedio participación T2 (0-100)'},
                    'asistencia_t2': {'type': 'number', 'description': 'Asistencia T2 (0-100)'},
                },
                'required': ['prom_tareas_t1', 'prom_examenes_t1', 'prom_part_t1', 'asistencia_t1', 
                           'prom_tareas_t2', 'prom_examenes_t2', 'prom_part_t2', 'asistencia_t2']
            }
        },
        examples=[
            OpenApiExample(
                'Estudiante Ejemplo',
                value={
                    "prom_tareas_t1": 85.0,
                    "prom_examenes_t1": 78.0,
                    "prom_part_t1": 92.0,
                    "asistencia_t1": 95.0,
                    "prom_tareas_t2": 87.0,
                    "prom_examenes_t2": 82.0,
                    "prom_part_t2": 88.0,
                    "asistencia_t2": 93.0
                }
            )
        ]
    )
    def post(self, request):
        """Predice la nota del 3er trimestre basada en T1 y T2"""
        try:
            # Validar datos de entrada
            estudiante = EstudianteSerializer.validar_entrada(request.data)
            
            # Realizar predicción
            prediccion = modelo_service.predecir(estudiante)
            
            # Serializar respuesta
            response_data = {
                "nota_estimada": prediccion.nota_estimada,
                "clasificacion": prediccion.clasificacion,
                "nivel_confianza": prediccion.nivel_confianza,
                "confianza_valor": prediccion.confianza_valor,
                "mensaje": prediccion.mensaje
            }
            
            logger.info(f"Predicción exitosa: {prediccion.nota_estimada}")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            logger.error(f"Error de validación: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error interno: {e}")
            return Response(
                {"error": "Error interno del servidor"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModeloView(APIView):
    """
    API View para gestión del modelo ML
    """
    
    @extend_schema(
        operation_id='obtener_info_modelo',
        summary='📊 Información del Modelo',
        description='Obtiene información detallada del modelo de Machine Learning actual.',
        tags=['Modelo ML']
    )
    def get(self, request):
        """Obtiene información del modelo actual"""
        try:
            info = modelo_service.obtener_info_modelo()
            return Response(info, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error obteniendo info del modelo: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @extend_schema(
        operation_id='entrenar_modelo',
        summary='🤖 Entrenar Modelo',
        description='Entrena o reentrena el modelo de Machine Learning con el dataset disponible.',
        tags=['Modelo ML'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'forzar_reentrenamiento': {
                        'type': 'boolean', 
                        'description': 'Si es true, reentrena aunque ya exista un modelo',
                        'default': False
                    }
                }
            }
        }
    )
    def post(self, request):
        """Entrena o reentrena el modelo"""
        try:
            forzar = request.data.get('forzar_reentrenamiento', False)
            metricas = modelo_service.entrenar_modelo(forzar_reentrenamiento=forzar)
            return Response(metricas, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error entrenando modelo: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthView(APIView):
    """
    API View para verificar el estado del servicio
    """
    
    @extend_schema(
        operation_id='health_check',
        summary='💚 Health Check',
        description='Verifica el estado general del microservicio, modelo ML y dataset.',
        tags=['Sistema']
    )
    def get(self, request):
        """Verifica el estado del servicio"""
        try:
            # Verificar modelo
            modelo_info = modelo_service.obtener_info_modelo()
            
            # Verificar dataset
            dataset_info = DatasetService.verificar_dataset()
            
            health_status = {
                "status": "healthy",
                "timestamp": "2025-05-31T03:00:00Z",
                "modelo": {
                    "cargado": modelo_info.get("cargado", False),
                    "tipo": "RandomForestRegressor"
                },
                "dataset": {
                    "existe": dataset_info.get("existe", False),
                    "filas": dataset_info.get("filas_validas", 0)
                },
                "endpoints": [
                    "/api/v1/predecir/",
                    "/api/v1/modelo/info/",
                    "/api/v1/modelo/entrenar/",
                    "/api/v1/health/"
                ]
            }
            
            return Response(health_status, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return Response(
                {
                    "status": "unhealthy",
                    "error": str(e)
                }, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            ) 