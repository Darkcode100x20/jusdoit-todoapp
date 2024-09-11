# jusdoit-todoapp
Application web basica, usa Flask
>>>>>>> 6f749355e376385d0c8ab6434aff80a8cc14eae9

<<<<<<< HEAD
# Just-do-it-app
Just do it app es una aplicacion web basica de una lista de tareas con las siguientes funcionalidades:
1. Inicio de sesión de usuarios

2. Añadir tareas

3. Editar tareas

4. Eliminar tareas

5. Prioridad de tareas
---
CSS | [Skeleton](http://getskeleton.com/)
JS  | [jQuery](https://jquery.com/)

I've also build a quite similar app in Django:
https://github.com/rtzll/django-todolist


## Explore
    Prueba la app
### Docker
Usando `docker-compose` puedes correr la app, con los siguientes comandos de Docker:

    docker-compose build
    docker-compose up

La aplicacion correra en http://localhost:8000/

(La app se sirve usando [gunicorn](http://gunicorn.org/) el cual se usa para el despliegue en vez de correr `flask run`.)

## Estructura del proyecto # Estructura del Proyecto

Esta aplicación Flask sigue una estructura típica para una aplicación web. A continuación se presenta una visión general de los componentes principales:

## Componentes Principales

1. **todolist.py**: 
   - El archivo principal de la aplicación
   - Inicializa la aplicación Flask
   - Configura las rutas

2. **app/**: 
   - Contiene el código principal de la aplicación
   - Incluye modelos, vistas y controladores

3. **config.py**: 
   - Gestiona la configuración de la aplicación
   - Maneja la configuración de la base de datos y las variables de entorno

4. **requirements.txt**  **test-requirements.txt**: 
   - Listan las dependencias de Python para el proyecto
   - Archivos separados para dependencias de producción y de pruebas

5. **Dockerfile** **docker-compose.yml**:
   - Utilizados para containerizar la aplicación con Docker

6. **.env**: 
   - Almacena variables de entorno
   - Incluye las claves secretas o URIs de bases de datos

7. **migrations/**: 
   - Contiene scripts de migración de la base de datos
   - Utiliza Flask-Migrate para gestionar cambios en el esquema de la base de datos

8. **tests/**: 
   - Alberga pruebas unitarias 

9. **utils/**: 
   - Contiene funciones o módulos auxiliares
   - Utilizados en diferentes partes de la aplicación

## Extensions
Al crear este proyecto se usaron las siguientes extensiones.

Usage               | Flask-Extension
------------------- | -----------------------
Model & ORM         | [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/latest/)
Migration           | [Flaks-Migrate](http://flask-migrate.readthedocs.io/en/latest/)
Forms               | [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/)
Login               | [Flask-Login](https://flask-login.readthedocs.org/en/latest/)
Testing             | [Flask-Testing](https://pythonhosted.org/Flask-Testing/)
=======