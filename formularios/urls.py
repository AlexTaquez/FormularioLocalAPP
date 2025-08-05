# filepath: formularios/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.seleccionar_formulario, name='seleccionar_formulario'),
    path('formulario/<int:formulario_id>/', views.responder_formulario, name='responder_formulario'),
    path('guardar_respuesta/', views.guardar_respuesta, name='guardar_respuesta'),
    path('resultados/', views.resultados_formularios, name='resultados_formularios'),
]