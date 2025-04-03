# Guía de Instalación de CoffeeShop

Esta guía proporciona instrucciones detalladas para instalar y configurar el entorno de desarrollo de CoffeeShop.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python**: Versión 3.8 o superior
- **PostgreSQL**: Versión 12 o superior
- **Git**: Para clonar el repositorio

## Pasos de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/CristianMz21/cofeShop.git
cd cofeShop
```

### 2. Configurar el Entorno Virtual

#### En Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### En macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Si no existe un archivo `requirements.txt`, puedes crear uno con las siguientes dependencias mínimas:

```
Django==5.2
psycopg2-binary==2.9.5
Pillow==9.4.0
python-dotenv==1.0.0
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
SECRET_KEY=tu_clave_secreta_generada
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=cofeshop
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña_postgres
DB_HOST=localhost
DB_PORT=5432
```

Para generar una clave secreta, puedes usar el siguiente comando en Python:

```python
import secrets
print(secrets.token_urlsafe(50))
```

### 5. Configurar la Base de Datos PostgreSQL

#### Crear la Base de Datos

```bash
# Acceder a PostgreSQL
psql -U postgres

# Dentro de PostgreSQL, crear la base de datos
CREATE DATABASE cofeshop;

# Salir de PostgreSQL
\q
```

### 6. Aplicar Migraciones

```bash
python manage.py migrate
```

### 7. Cargar Datos Iniciales

```bash
python manage.py loaddata shop/fixtures/users_data.json
python manage.py loaddata shop/fixtures/initial_data.json
```

### 8. Crear un Superusuario (Opcional)

Si no quieres usar los usuarios predefinidos, puedes crear tu propio superusuario:

```bash
python manage.py createsuperuser
```

### 9. Iniciar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Ahora puedes acceder a la aplicación en tu navegador: http://127.0.0.1:8000/

El panel de administración está disponible en: http://127.0.0.1:8000/admin/

## Solución de Problemas Comunes

### Error de Conexión a la Base de Datos

Si encuentras errores al conectar con PostgreSQL:

1. Verifica que PostgreSQL esté en ejecución
2. Comprueba las credenciales en el archivo `.env`
3. Asegúrate de que la base de datos `cofeshop` exista

### Error al Cargar los Fixtures

Si hay problemas al cargar los datos iniciales:

1. Asegúrate de que las migraciones se han aplicado correctamente
2. Verifica que los archivos de fixtures existen en la ruta correcta
3. Intenta cargar cada fixture por separado para identificar el problema

### Problemas con las Imágenes

Si las imágenes de productos no se muestran:

1. Verifica que la carpeta `media` existe y tiene los permisos adecuados
2. Comprueba que la configuración de `MEDIA_URL` y `MEDIA_ROOT` en `settings.py` es correcta

## Configuración para Desarrollo

### Configurar Email para Desarrollo

Para probar funcionalidades de email en desarrollo, puedes usar la configuración de consola:

Añade esto a tu archivo `.env`:

```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Habilitar Django Debug Toolbar

Para facilitar el desarrollo, puedes instalar Django Debug Toolbar:

```bash
pip install django-debug-toolbar
```

Luego añade la configuración necesaria en `settings.py` según la documentación oficial.