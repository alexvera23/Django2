# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserSerializer, MateriaSerializer
from .models import User, Materia 
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    """
    Vista para registrar un nuevo usuario en el sistema.
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


class AdminUserListView(generics.ListAPIView):
    """
    Vista para listar TODOS los usuarios (para que el Admin los vea).
    """
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
    """
    Vista para obtener, actualizar o eliminar un usuario específico.
    Soporta tanto PUT (actualización completa) como PATCH (actualización parcial).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        """
        Sobrescribimos update para agregar logging y mejor manejo de errores.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Maneja las solicitudes PATCH para actualizaciones parciales.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)