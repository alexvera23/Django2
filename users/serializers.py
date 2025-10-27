# users/serializers.py
from rest_framework import serializers
from .models import User, Materia
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Serializador para el modelo Materia
class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id', 'nombre']

class UserSerializer(serializers.ModelSerializer):
    materias = serializers.PrimaryKeyRelatedField(
        queryset=Materia.objects.all(), 
        many=True, 
        write_only=True,
        required=False # Hacemos que no sea estrictamente requerido para admins y alumnos
    )
    class Meta:
        model = User
        # Campos que se enviarán/recibirán. La contraseña no se debe devolver.
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'password', 'rol', 'telefono', 'fecha_nacimiento', 'edad',
            'clave_admin', 'rfc', 'ocupacion', 'matricula', 'curp',
            'n_empleado', 'cubiculo', 'area_investigacion', 'materias'
        ]
        # Configuración extra para campos específicos
        extra_kwargs = {
            'password': {'write_only': True} # 'write_only' significa que solo se usa para crear/actualizar, no para mostrar
        }

    def create(self, validated_data):
        materias_data = validated_data.pop('materias', None)
        """
        Este método se llama cuando se crea un nuevo usuario.
        Encripta la contraseña antes de guardarla.
        """
        # Extrae la contraseña del diccionario de datos validados
        password = validated_data.pop('password', None)

        # Crea una instancia del usuario con el resto de los datos
        instance = self.Meta.model(**validated_data)

        # Si se proporcionó una contraseña, la encripta
        if password is not None:
            instance.set_password(password) # ¡Esto encripta la contraseña!

        # Guarda el nuevo usuario en la base de datos
        instance.save()
        if materias_data:
            instance.materias.set(materias_data)

        return instance
    

# Serializador personalizado para JWT que incluye el rol del usuario
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Llama al método original para obtener el token base
        token = super().get_token(user)

        # --- Añade tus campos personalizados al "payload" del token ---
        # Estos datos estarán encriptados dentro del token
        token['username'] = user.username
        token['rol'] = user.rol 
        # Puedes añadir más campos si lo necesitas, como 'first_name'

        return token