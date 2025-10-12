# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

class RegisterView(APIView):
    """
    Vista para registrar un nuevo usuario en el sistema.
    """
    def post(self, request):
        # Tomamos los datos que llegan en la petición (el JSON del frontend)
        serializer = UserSerializer(data=request.data)

        # Validamos los datos con las reglas del serializer
        if serializer.is_valid():
            # Si son válidos, creamos el usuario (esto llama al método .create() del serializer)
            serializer.save()
            # Devolvemos una respuesta exitosa
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si los datos no son válidos, devolvemos los errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)