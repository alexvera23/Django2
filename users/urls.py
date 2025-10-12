# users/urls.py
from django.urls import path
from .views import RegisterView

urlpatterns = [
    # La ruta 'register/' se mapeará a nuestra RegisterView
    path('register/', RegisterView.as_view(), name='register'),
]