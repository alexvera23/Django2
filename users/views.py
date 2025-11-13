# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserSerializer, MateriaSerializer
from .models import User, Materia 
from rest_framework.permissions import AllowAny # Permite cargar las materias sin necesidad del token :)
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    """
    Vista para registrar un nuevo usuario en el sistema.
    """
    permission_classes = [AllowAny]  # Permite el acceso sin autenticación
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
    permission_classes = [AllowAny]  # Permite el acceso sin autenticación (antes necesitabas un token :/)


class AdminUserListView(generics.ListAPIView):
    """
    Vista para listar TODOS los usuarios (para que el Admin los vea).
    En un futuro, podrías cambiar IsAuthenticated por IsAdminUser
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated] # Solo usuarios logueados

class AdministradoresListView(generics.ListAPIView):
    """ Vista para listar solo usuarios con rol 'administrador' """
    queryset = User.objects.filter(rol=User.Rol.ADMINISTRADOR).order_by('last_name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class MaestrosListView(generics.ListAPIView):
    """ Vista para listar solo usuarios con rol 'maestro' """
    queryset = User.objects.filter(rol=User.Rol.MAESTRO).order_by('last_name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class AlumnosListView(generics.ListAPIView):
    """ Vista para listar solo usuarios con rol 'alumno' """
    queryset = User.objects.filter(rol=User.Rol.ALUMNO).order_by('last_name')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
