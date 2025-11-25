# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Materia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class User(AbstractUser):
   

   #Tenmos que definir los roles de usuario
    class Rol(models.TextChoices):
        ADMINISTRADOR = 'administrador', 'Administrador'
        MAESTRO = 'maestro', 'Maestro'
        ALUMNO = 'alumno', 'Alumno'


    rol = models.CharField(
        max_length=15,
        choices=Rol.choices,
        default=Rol.ALUMNO,
        verbose_name='Rol'
    )

   

    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)

    # Campos  de Administrador
    clave_admin = models.CharField(max_length=50, blank=True, null=True, unique=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)

    # Campos de Alumno
    matricula = models.CharField(max_length=50, blank=True, null=True, unique=True)
    curp = models.CharField(max_length=18, blank=True, null=True)

    # Campos  de Maestro
    n_empleado = models.CharField(max_length=50, blank=True, null=True, unique=True)
    cubiculo = models.CharField(max_length=50, blank=True, null=True)
    area_investigacion = models.CharField(max_length=100, blank=True, null=True)
   
    materias = models.ManyToManyField(Materia, blank=True)


    def __str__(self):
        return self.get_full_name() if self.get_full_name() else self.username