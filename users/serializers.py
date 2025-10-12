# users/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Campos que se enviarán/recibirán. La contraseña no se debe devolver.
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'password', 'rol', 'telefono', 'fecha_nacimiento', 'edad',
            'clave_admin', 'rfc', 'ocupacion', 'matricula', 'curp',
            'n_empleado', 'cubiculo', 'area_investigacion'
        ]
        # Configuración extra para campos específicos
        extra_kwargs = {
            'password': {'write_only': True} # 'write_only' significa que solo se usa para crear/actualizar, no para mostrar
        }

    def create(self, validated_data):
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
        return instance