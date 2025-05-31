"""
URLs - Configuración de rutas Django para el microservicio de predicción
"""

from django.urls import path
from . import views

app_name = 'microservicio_prediccion'

# URLs del microservicio - Accesibles desde /api/v1/
urlpatterns = [
    # 🎯 Predicción de notas académicas
    path('predecir/', views.PrediccionView.as_view(), name='predecir'),
    
    # 🤖 Gestión del modelo ML
    path('modelo/info/', views.ModeloView.as_view(), name='modelo_info'),
    path('modelo/entrenar/', views.ModeloView.as_view(), name='modelo_entrenar'),
    
    # 💚 Health check y sistema
    path('health/', views.HealthView.as_view(), name='health'),
] 