# CoffeeShop - Aplicación de Tienda de Café

CoffeeShop es una aplicación web desarrollada con Django que permite gestionar una tienda online de café, postres y accesorios relacionados. La aplicación incluye funcionalidades para administrar productos, categorías, usuarios, carritos de compra y pedidos.

## Características Principales

- **Sistema de usuarios**: Administradores, empleados y clientes con diferentes niveles de acceso
- **Catálogo de productos**: Organizado por categorías (Café, Postres, Accesorios)
- **Carrito de compras**: Permite a los usuarios añadir productos y gestionar cantidades
- **Proceso de checkout**: Flujo completo para finalizar compras
- **Historial de pedidos**: Los usuarios pueden ver sus pedidos anteriores
- **Panel de administración**: Interfaz para gestionar todos los aspectos de la tienda

## Requisitos

- Python 3.8 o superior
- Django 5.2
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

- `/`: Página principal
- `/products/`: Lista de productos
- `/category/<id>/`: Productos filtrados por categoría
- `/product/<id>/`: Detalle de un producto
- `/cart/`: Carrito de compras
- `/checkout/`: Proceso de pago
- `/orders/`: Historial de pedidos
- `/admin/`: Panel de administración

## Panel de Administración

Accede al panel de administración en http://127.0.0.1:8000/admin/ con las credenciales de administrador para gestionar:

- Usuarios
- Categorías
- Productos
- Pedidos
- Carritos de compra

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

## Licencia

Este proyecto está licenciado bajo [Licencia MIT](LICENSE).