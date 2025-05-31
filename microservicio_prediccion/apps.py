from django.apps import AppConfig


class MicroservicioPrediccionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'microservicio_prediccion'
    verbose_name = 'Microservicio de Predicción Académica'
    
    def ready(self):
        """Inicialización cuando la app esté lista"""
        # Aquí se puede cargar el modelo ML automáticamente si es necesario
        pass 