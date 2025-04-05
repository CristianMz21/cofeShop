# CoffeeShop - Aplicación de Tienda de Café

CoffeeShop es una aplicación web desarrollada con Django que permite gestionar una tienda online de café, postres y accesorios relacionados. La aplicación incluye funcionalidades para administrar productos, categorías, usuarios, carritos de compra y pedidos.

## Características Principales

- **Sistema de usuarios**: Administradores, empleados y clientes con diferentes niveles de acceso
- **Catálogo de productos**: Organizado por categorías (Café, Postres, Accesorios)
- **Carrito de compras**: Permite a los usuarios añadir productos y gestionar cantidades
- **Proceso de checkout**: Flujo completo para finalizar compras
- **Historial de pedidos**: Los usuarios pueden ver sus pedidos anteriores
- **Panel de administración**: Interfaz para gestionar todos los aspectos de la tienda
- **API REST**: Interfaz programática completa para integración con otros sistemas

## Requisitos

- Python 3.8 o superior
- Django 5.2
- Django REST Framework
- PostgreSQL
- Otras dependencias listadas en requirements.txt

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/CristianMz21/cofeShop.git
   cd cofeShop
   ```

2. Crear y activar un entorno virtual:
   ```
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   SECRET_KEY=tu_clave_secreta
   DEBUG=True
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=cofeshop
   DB_USER=tu_usuario_db
   DB_PASSWORD=tu_contraseña_db
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. Configurar la base de datos PostgreSQL:
   - Crear una base de datos llamada `cofeshop`
   - Asegurarse de que las credenciales en el archivo `.env` son correctas

6. Aplicar migraciones:
   ```
   python manage.py migrate
   ```

7. Cargar datos iniciales:
   ```
   python manage.py loaddata shop/fixtures/users_data.json
   python manage.py loaddata shop/fixtures/initial_data.json
   ```

8. Iniciar el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

9. Acceder a la aplicación en el navegador: http://127.0.0.1:8000/

## Estructura del Proyecto

- **cofeshop/**: Configuración principal del proyecto Django
  - `settings.py`: Configuración de la aplicación
  - `urls.py`: Configuración de URLs principal

- **shop/**: Aplicación principal
  - `models.py`: Definición de modelos (User, Category, Product, Order, etc.)
  - `views.py`: Vistas para manejar las solicitudes HTTP
  - `urls.py`: Configuración de URLs de la aplicación
  - `admin.py`: Configuración del panel de administración
  - `api/`: Implementación de la API REST
    - `views.py`: Vistas de la API
    - `serializers.py`: Serializadores para convertir modelos a JSON
    - `urls.py`: Configuración de URLs de la API
  - `fixtures/`: Datos iniciales para cargar en la base de datos

## Usuarios Predefinidos

La aplicación incluye varios usuarios predefinidos para pruebas:

| Usuario    | Contraseña | Tipo        |
|------------|------------|-------------|
| admin      | admin      | Administrador |
| empleado1  | admin      | Empleado    |
| empleado2  | admin      | Empleado    |
| cliente1   | admin      | Cliente     |
| cliente2   | admin      | Cliente     |

## Endpoints Principales

### Aplicación Web

- `/`: Página principal
- `/products/`: Lista de productos
- `/category/<id>/`: Productos filtrados por categoría
- `/product/<id>/`: Detalle de un producto
- `/cart/`: Carrito de compras
- `/checkout/`: Proceso de pago
- `/orders/`: Historial de pedidos
- `/admin/`: Panel de administración Django predeterminado

### Panel Administrativo

- `/manage/login/`: Inicio de sesión para el panel administrativo personalizado
  - Accesible solo para usuarios tipo 'admin' o 'employee'
  - Redirecciona a `/manage/dashboard/` tras inicio de sesión exitoso
- `/manage/dashboard/`: Panel principal de administración
- `/manage/inventory/`: Gestión de inventario
- `/manage/orders/`: Gestión de pedidos

### API REST

Todos los endpoints de la API REST están disponibles bajo el prefijo `/api/`:

- `/api/categories/`: Gestión de categorías
- `/api/products/`: Gestión de productos
- `/api/carts/`: Gestión de carritos de compra
  - `/api/carts/my_cart/`: Obtener el carrito del usuario actual
  - `/api/carts/add_item/`: Añadir un producto al carrito
  - `/api/carts/remove_item/`: Eliminar un producto del carrito
- `/api/orders/`: Gestión de pedidos
  - `/api/orders/checkout/`: Crear un nuevo pedido
  - `/api/orders/{id}/update_status/`: Actualizar el estado de un pedido
- `/api/login/`: Autenticación y obtención de token

Para más detalles sobre la API, consulte la documentación en la carpeta `docs/`:
- [Guía de API General](docs/API_GUIDE.md)
- [Guía de API REST](docs/API_GUIDE_REST.md)

## Autenticación de API

La API proporciona autenticación mediante tokens. Para obtener un token:

```
POST /api/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

Para usar el token, incluirlo en el encabezado de las solicitudes:
```
Authorization: Token tu_token_de_autenticación
```

## Scripts de Ejemplo

El repositorio incluye scripts de ejemplo para interactuar con la API:

- `test_product_api.py`: Demuestra cómo crear un nuevo producto a través de la API

Para ejecutar el script:
```
python test_product_api.py
```

## Panel de Administración

Accede al panel de administración en http://127.0.0.1:8000/admin/ con las credenciales de administrador para gestionar:

- Usuarios
- Categorías
- Productos
- Pedidos
- Carritos de compra

Además, existe un panel administrativo personalizado disponible en http://127.0.0.1:8000/manage/, que ofrece una interfaz más adaptada a las necesidades específicas de la tienda.

## Desarrollo

### Crear un superusuario

Para crear un nuevo administrador:

```
python manage.py createsuperuser
```

### Ejecutar pruebas

```
python manage.py test shop
```

### Generar tokens de autenticación

Para generar un token para un usuario desde el shell de Django:

```python
python manage.py shell

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='usuario')
token, created = Token.objects.get_or_create(user=user)
print(f"Token: {token.key}")
```

## Documentación

Para obtener más información sobre el funcionamiento del sistema, consulte la documentación en la carpeta `docs/`:

- [Documentación General](docs/DOCUMENTATION.md)
- [Guía de Instalación](docs/INSTALLATION.md)
- [Guía de Usuario](docs/USER_GUIDE.md)
- [Guía de API](docs/API_GUIDE.md)
- [Guía de API REST](docs/API_GUIDE_REST.md)

## Licencia

Este proyecto está licenciado bajo [Licencia MIT](LICENSE).