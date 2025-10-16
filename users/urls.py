# users/urls.py
from django.urls import path
from .views import RegisterView, MateriaListView


urlpatterns = [
    # La ruta 'register/' se mapeará a nuestra RegisterView
    path('register/', RegisterView.as_view(), name='register'),
    path('materias/', MateriaListView.as_view(), name='materia-list'),
]