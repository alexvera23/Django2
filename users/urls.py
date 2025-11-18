# users/urls.py
from django.urls import path
from .views import(RegisterView, 
                   MateriaListView,
                   AdminUserListView,
                   AdministradoresListView,
                   MaestrosListView,
                   UserDetailView,
                   AlumnosListView) 


urlpatterns = [
    # La ruta 'register/' se mapeará a nuestra RegisterView
    path('register/', RegisterView.as_view(), name='register'),
    path('materias/', MateriaListView.as_view(), name='materia-list'),
    path('users/all/', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/administradores/', AdministradoresListView.as_view(), name='user-list-admins'),
    path('users/maestros/', MaestrosListView.as_view(), name='user-list-maestros'),
    path('users/alumnos/', AlumnosListView.as_view(), name='user-list-alumnos'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]