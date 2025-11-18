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
    materias_info = MateriaSerializer(source='materias', many=True, read_only=True)
    materias = serializers.PrimaryKeyRelatedField(
        queryset=Materia.objects.all(), 
        many=True, 
        write_only=True,
        required=False
    )
    
    class Meta:
        model = User
        
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'password', 'rol', 'telefono', 'fecha_nacimiento', 'edad',
            'clave_admin', 'rfc', 'ocupacion', 'matricula', 'curp',
            'n_empleado', 'cubiculo', 'area_investigacion', 'materias', 'materias_info'
        ]
        
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }
        read_only_fields = ['id', 'materias_info', 'edad']

    def create(self, validated_data):
        materias_data = validated_data.pop('materias', None)
        password = validated_data.pop('password', None)
        
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        
        if materias_data:
            instance.materias.set(materias_data)
        
        return instance
    
    def update(self, instance, validated_data):
        """
        Actualiza un usuario existente.
        Si se proporciona una contraseña, la encripta antes de guardar.
        """
        # Extraer campos especiales
        password = validated_data.pop('password', None)
        materias_data = validated_data.pop('materias', None)
        
        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Si hay una nueva contraseña, encriptarla
        if password:
            instance.set_password(password)
        
        # Guardar los cambios
        instance.save()
        
        # Actualizar materias si se proporcionaron
        if materias_data is not None:
            instance.materias.set(materias_data)
        
        return instance

# Serializador personalizado para JWT que incluye el rol del usuario
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['rol'] = user.rol 
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token