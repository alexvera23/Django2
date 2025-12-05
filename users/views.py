# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserSerializer, MateriaSerializer, EventoSerializer
from .models import Evento, User, Materia 
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse



class RegisterView(APIView):
    """
    Vista para registrar un nuevo usuario 
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MateriaListView(generics.ListCreateAPIView):
    """
    Vista para listar todas las materias o crear una nueva materia.
    """
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [AllowAny]
    authentication_classes = [] 


class AdminUserListView(generics.ListAPIView):
    
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class AdministradoresListView(generics.ListAPIView):
    """Vista para listar solo usuarios con rol 'administrador'"""
    queryset = User.objects.filter(rol=User.Rol.ADMINISTRADOR).order_by('last_name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class MaestrosListView(generics.ListAPIView):
    """Vista para listar solo usuarios con rol 'maestro'"""
    queryset = User.objects.filter(rol=User.Rol.MAESTRO).order_by('last_name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class AlumnosListView(generics.ListAPIView):
    """Vista para listar solo usuarios con rol 'alumno'"""
    queryset = User.objects.filter(rol=User.Rol.ALUMNO).order_by('last_name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
       
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
class EventoListView(generics.ListCreateAPIView):
    """
    Vista para listar todos los eventos o crear un nuevo evento.
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

class EventoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar o eliminar un evento específico.
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]    


def crear_superusuario_temporal(request):
    # Definimos las credenciales que queremos
    username = 'admin_render'
    password = 'password_segura_123'  # ¡Cámbiala después de entrar!
    email = 'admin@escuela.com'

    if not User.objects.filter(username=username).exists():
        # Creamos el superusuario usando el método helper de Django
        User.objects.create_superuser(username, email, password)
        return HttpResponse(f"¡Éxito! Superusuario creado.<br>Usuario: {username}<br>Password: {password}")
    else:
        return HttpResponse("El superusuario ya existe.")
    