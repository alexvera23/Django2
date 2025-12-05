Sistema de Gestion Academica (SGA) - Backend

Este repositorio contiene el codigo fuente del Backend para el Sistema de Gestion Academica. Esta desarrollado utilizando Python y Django REST Framework, proporcionando una API RESTful robusta para gestionar la autenticacion de usuarios, la administracion de perfiles academicos (alumnos, profesores, administradores), la gestion de materias y la coordinacion de eventos academicos.

Tecnologias Utilizadas

Lenguaje: Python 3.x

Framework Web: Django

API REST: Django REST Framework (DRF)

Base de Datos: SQLite (Configuracion por defecto para desarrollo)

Autenticacion: Token-based authentication (DRF)

CORS: Django CORS Headers

Estructura del Proyecto

El proyecto sigue la arquitectura estandar de Django con una aplicacion principal llamada users que centraliza la logica de negocio.

myproject/: Directorio de configuracion principal (settings, urls, wsgi).

users/: Aplicacion principal.

models.py: Definicion de modelos de datos (User, Alumno, Profesor, Materia, Evento).

views.py: ViewSets y controladores de la API.

serializers.py: Serializadores para transformar objetos de modelo a JSON y validacion de datos.

urls.py: Rutas especificas de la API para la aplicacion de usuarios.

manage.py: Script de utilidad para tareas administrativas de Django.

Funcionalidades de la API

1. Gestion de Usuarios

La API permite el registro, edicion, eliminacion y consulta de tres tipos de usuarios, gestionados a traves de un modelo de usuario personalizado:

Administradores: Acceso total al sistema.

Profesores: Gestionan materias y eventos relacionados. Incluyen campos como ID de trabajador.

Alumnos: Se asocian a materias. Incluyen campos como Matricula.

2. Eventos Academicos

Endpoints dedicados para el ciclo de vida de un evento (CRUD):

Creacion de eventos con fecha, hora y tipo.

Listado de eventos para su visualizacion en el frontend.

3. Materias

Gestion del catalogo de materias disponibles para su asignacion a profesores y alumnos.

4. Seguridad

Implementacion de permisos para restringir el acceso a ciertos endpoints basado en el estado de autenticacion del usuario.

Validacion de datos de entrada a traves de Serializers.

Guia de Instalacion y Ejecucion

Sigue estos pasos para levantar el servidor de desarrollo en tu entorno local.

Prerrequisitos

Python instalado en el sistema.

pip (gestor de paquetes de Python).

Pasos

Clonar el repositorio o navegar a la carpeta del backend

Crear un entorno virtual
Es recomendable aislar las dependencias del proyecto.

Windows:

python -m venv venv
venv\Scripts\activate



macOS/Linux:

python3 -m venv venv
source venv/bin/activate



Instalar dependencias

pip install -r requirements.txt



Aplicar migraciones
Configura la base de datos inicial.

python manage.py makemigrations
python manage.py migrate



Crear un Superusuario (Opcional)
Para acceder al panel de administracion de Django.

python manage.py createsuperuser

Ejecutar el servidor

python manage.py runserver



El servidor estara disponible en http://127.0.0.1:8000/.

