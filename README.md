# Futbolmanía

Aplicación de fútbol llamada Futbolmanía inspirada en juegos de creación de plantilla como el Comunio o el Liga fantasy.

Creado en Python usando el framework Django y con el sistema de gestión de bases de datos relacional Postgresql.

## Instalación

Esta aplicación web de Djando necesita instalar varios paquetes adicionales de Python, para ello, usaremos el siguiente comando:
```
$ pip install -r requirements.txt
```
Para construir la base de datos usaremos los siguientes comandos:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
## Panel de administración

Django nos ofrece la posibilidad de tener un panel de administración desde el cual se puede crear, consultar, actualizar y borrar registros. Para acceder a este panel de administración debemos **crear un superusuario**, lo haremos usando el siguiente código:
```
$ python manage.py createsuperuser
```

## Ejecutar la aplicación

Para arrancar el servidor usaremos el siguiente comando:
```
$ python manage.py ruserver
```
A continuación, abra en su navegador la siguiente URL: http://127.0.0.1:8000/inicioSesion para acceder a la aplicación.

Si se desea acceder al panel de administración debemos usar la URL: http://127.0.0.1:8000/admin e introducir el nombre de usuario y la contraseña que hemos creado antes.

## Uso

Esta es una aplicación es necesario estar registrado e iniciar sesión para poder navegar por ella. A la hora de registrarse es necesario unirse a una liga para poder jugar. Si no tiene ninguna liga a la que unirse puede se puede crear una nueva. Una vez se tenga un usuario y una liga, ya se podrá entrar en la aplicación.

En la pestaña de ayuda se resuelven alguna de las dudas más frecuentes sobre el funcionamiento de la aplicación.
