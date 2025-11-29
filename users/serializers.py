# users/serializers.py
from rest_framework import serializers
from .models import User, Materia, Evento
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
        
        # Extraer campos especiales
        password = validated_data.pop('password', None)
        materias_data = validated_data.pop('materias', None)
        
        # Actualizar campos básicos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        
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
    

class EventoSerializer(serializers.ModelSerializer):
    publico = serializers.DictField(child=serializers.BooleanField(), write_only=True)
    responsable_nombre = serializers.SerializerMethodField()
    class Meta:
        model = Evento
        fields = [
            'id', 'nombre', 'tipo', 'fecha', 'hora_inicio', 'hora_fin',
            'lugar', 'programa_educativo', 'responsable', 'descripcion', 'cupo',
            'publico', # El campo que recibe el JSON
            # Los campos reales (para cuando leamos datos)
            'publico_estudiantes', 'publico_profesores', 'publico_general'
        ]
        read_only_fields = [ 'publico_estudiantes', 'publico_profesores', 'publico_general' ]

    def get_responsable_nombre(self, obj):
        return f"{obj.responsable.first_name} {obj.responsable.last_name}"

    def create(self, validated_data):
        publico_data = validated_data.pop('publico', {})
        evento=Evento.objects.create(
            publico_estudiantes=publico_data.get('estudiantes', False),
            publico_profesores=publico_data.get('profesores', False),
            publico_general=publico_data.get('general', False),
            **validated_data
        )
        return evento