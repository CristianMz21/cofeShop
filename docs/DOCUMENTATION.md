# Documentación del Sistema CoffeeShop

## Introducción

CoffeeShop es una aplicación web desarrollada con Django para gestionar una tienda de café. Esta documentación proporciona información sobre la arquitectura del sistema, características principales, y cómo utilizar y mantener la aplicación.

## Estructura del proyecto

```
cofeshop/
├── cofeshop/           # Configuración principal del proyecto
├── shop/               # Aplicación principal
│   ├── api/            # API REST
│   ├── fixtures/       # Datos iniciales
│   ├── migrations/     # Migraciones de la base de datos
│   ├── static/         # Archivos estáticos
│   ├── templates/      # Plantillas HTML
│   ├── tests/          # Pruebas unitarias
│   ├── models.py       # Modelos de datos
│   ├── views.py        # Vistas regulares
│   ├── views_admin.py  # Vistas administrativas
│   ├── auth_views.py   # Vistas de autenticación
│   └── urls.py         # Configuración de URLs
├── media/              # Archivos cargados por usuarios
├── stactic/            # Archivos estáticos globales
├── docs/               # Documentación
├── manage.py           # Script de gestión de Django
├── test_product_api.py # Script de prueba para la API
└── .env                # Variables de entorno
```

## Modelos de datos

### Usuarios

- **User**: Extensión del modelo de usuario de Django con campos adicionales:
  - `user_type`: Tipo de usuario (customer, employee, admin)
  - `phone`: Número telefónico
  - `address`: Dirección
  - `city`: Ciudad

### Productos

- **Category**: Categorías de productos
  - `name`: Nombre de la categoría
  - `description`: Descripción
  - `created_at`: Fecha de creación

- **Product**: Productos disponibles
  - `name`: Nombre del producto
  - `description`: Descripción
  - `price`: Precio
  - `category`: Categoría (ForeignKey a Category)
  - `image`: Imagen del producto
  - `stock`: Cantidad en inventario
  - `available`: Indica si está disponible
  - `created_at`: Fecha de creación
  - `updated_at`: Fecha de actualización

### Carrito y Pedidos

- **Cart**: Carrito de compras
  - `user`: Usuario propietario
  - `created_at`: Fecha de creación
  - `updated_at`: Fecha de actualización
  
- **CartItem**: Elementos en el carrito
  - `cart`: Carrito al que pertenece
  - `product`: Producto
  - `quantity`: Cantidad

- **Order**: Pedidos realizados
  - `user`: Usuario que realizó el pedido
  - `full_name`: Nombre completo
  - `email`: Correo electrónico
  - `address`: Dirección de envío
  - `phone`: Teléfono
  - `total_amount`: Monto total
  - `status`: Estado del pedido (pending, processing, shipped, delivered, cancelled)
  - `notes`: Notas adicionales
  - `created_at`: Fecha de creación
  - `updated_at`: Fecha de actualización

- **OrderItem**: Elementos de un pedido
  - `order`: Pedido al que pertenece
  - `product`: Producto
  - `price`: Precio al momento de la compra
  - `quantity`: Cantidad

## Panel Administrativo Personalizado

El sistema incluye un panel administrativo personalizado, disponible en `/manage/`, que proporciona una interfaz adaptada a las necesidades específicas de la tienda de café.

### Acceso al Panel Administrativo

El panel administrativo es accesible solo para usuarios con tipo 'admin' o 'employee'. El endpoint de autenticación es:

```
GET/POST /manage/login/
```

**Descripción:** Página de inicio de sesión para el panel administrativo. 

**Métodos disponibles:**
- **GET**: Muestra el formulario de inicio de sesión
- **POST**: Procesa las credenciales enviadas

**Parámetros (POST):**
- `username`: Nombre de usuario
- `password`: Contraseña

**Respuesta (POST exitoso):**
Redirección a `/manage/dashboard/` si las credenciales son válidas y el usuario tiene permisos adecuados

**Notas de seguridad:**
- Esta ruta implementa limitación de intentos para prevenir ataques de fuerza bruta
- La sesión expira después de 30 minutos de inactividad
- Las contraseñas se transmiten de forma segura mediante HTTPS (en producción)

### Secciones del Panel Administrativo

El panel administrativo incluye las siguientes secciones principales:

- **Dashboard** (`/manage/dashboard/`): Proporciona una visión general del negocio, incluyendo:
  - Resumen de ventas
  - Pedidos recientes
  - Estado del inventario
  - Gráficos y estadísticas

- **Gestión de Inventario** (`/manage/inventory/`): Permite:
  - Ver el inventario actual
  - Añadir/reducir stock de productos
  - Recibir alertas de stock bajo
  - Registrar movimientos de inventario

- **Gestión de Pedidos** (`/manage/orders/`): Permite:
  - Ver todos los pedidos
  - Filtrar por estado
  - Actualizar el estado de los pedidos
  - Ver detalles completos de cada pedido

- **Gestión de Productos** (`/manage/products/`): Permite:
  - Crear nuevos productos
  - Editar productos existentes
  - Gestionar categorías
  - Activar/desactivar productos

- **Informes** (`/manage/reports/`): Proporciona:
  - Informes de ventas por período
  - Productos más vendidos
  - Análisis de clientes
  - Exportación a formatos CSV/Excel

### Diferencias con el Panel de Admin de Django

A diferencia del panel de administración predeterminado de Django (`/admin/`), el panel personalizado (`/manage/`):

1. Está diseñado específicamente para operaciones de la tienda de café
2. Tiene una interfaz más amigable y adaptada al flujo de trabajo del negocio
3. Incorpora estadísticas y métricas relevantes
4. Está restringido a funcionalidades específicas del negocio
5. Tiene un diseño visual coherente con la marca

## API REST

La aplicación incluye una API REST completa que permite integrar CoffeeShop con otros sistemas o desarrollar aplicaciones móviles. La API está implementada utilizando Django REST Framework.

### Documentación de la API

La documentación completa de la API está disponible en:
- [Guía de API General](API_GUIDE.md)
- [Guía de API REST](API_GUIDE_REST.md)

### Autenticación de la API

La API proporciona varios métodos de autenticación:

#### Autenticación por Token

Para acceder a los endpoints protegidos, se puede utilizar autenticación por token. Los tokens se generan por usuario y no caducan a menos que se regeneren manualmente.

Para obtener un token:

```
GET/POST /api/login/
```

**Métodos disponibles:**
- **POST**: Enviar credenciales en el cuerpo de la solicitud
  ```json
  {
    "username": "usuario",
    "password": "contraseña"
  }
  ```
- **GET**: Enviar credenciales como parámetros de consulta
  ```
  /api/login/?username=usuario&password=contraseña
  ```

**Respuesta:**
```json
{
  "token": "tu_token_de_autenticación"
}
```

**Uso del token:**
Incluir el token en el encabezado de las solicitudes:
```
Authorization: Token tu_token_de_autenticación
```

#### Autenticación por Sesión

También se admite la autenticación por sesión de Django para aplicaciones web que utilizan la API.

### Permisos de la API

La API implementa varios niveles de permisos:

- **IsAdminOrReadOnly**: Permite acceso de lectura a todos los usuarios, pero solo administradores pueden crear, actualizar o eliminar recursos.
- **IsOwnerOrAdmin**: Permite a los usuarios acceder solo a sus propios recursos, mientras que los administradores pueden acceder a todos.

### Ejemplos de uso de la API

#### Scripts de prueba

El proyecto incluye scripts de ejemplo para probar la API. Por ejemplo, el script `test_product_api.py` demuestra cómo crear un nuevo producto a través de la API:

```python
import requests
import json

# Data para el nuevo producto
product_data = {
    "name": "Té Verde Matcha",
    "description": "Té verde japonés premium en polvo para ceremonias",
    "price": "18.50",
    "category_id": 4,
    "image": "http://127.0.0.1:8000/media/products/te_verde.jpg",
    "stock": 40,
    "available": True
}

# Realizar la solicitud API para crear el producto
response = requests.post('http://127.0.0.1:8000/api/products/', 
                        json=product_data)

# Imprimir los resultados
print(f'Product Creation Status Code: {response.status_code}')
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text) 
```

Para ejecutar este script:

```bash
python test_product_api.py
```

**Nota**: Este script de ejemplo está configurado para ejecutarse sin autenticación. En un entorno de producción, es necesario modificarlo para incluir el token de autenticación como se muestra a continuación.

##### Autenticación en scripts

Para usar endpoints protegidos, es necesario primero obtener un token. Modifique sus scripts para incluir la autenticación:

```python
# Obtener token
auth_response = requests.post('http://127.0.0.1:8000/api/login/', 
                             json={"username": "admin", "password": "adminpassword"})
token = auth_response.json()['token']

# Usar token en solicitudes
headers = {'Authorization': f'Token {token}'}
response = requests.post('http://127.0.0.1:8000/api/products/', 
                        json=product_data,
                        headers=headers)
```

#### Creación de scripts personalizados

Puede crear sus propios scripts para interactuar con la API. Por ejemplo, para crear un script que obtenga la lista de todos los productos:

```python
import requests
import json

# Obtener token (si es necesario para su entorno)
auth_response = requests.post('http://127.0.0.1:8000/api/login/', 
                             json={"username": "admin", "password": "adminpassword"})
token = auth_response.json()['token']
headers = {'Authorization': f'Token {token}'}

# Obtener lista de productos
response = requests.get('http://127.0.0.1:8000/api/products/', headers=headers)

# Imprimir resultados
print(f'Status Code: {response.status_code}')
print(json.dumps(response.json(), indent=2))
```

## Flujo de trabajo del sistema

### Flujo de compra para clientes

1. El cliente navega por los productos y categorías
2. Añade productos al carrito de compras
3. Procede al checkout y proporciona información de envío
4. Completa el pedido
5. Puede ver el historial de sus pedidos

### Flujo de administración

1. Los administradores y empleados pueden ver todos los pedidos
2. Pueden actualizar el estado de los pedidos
3. Pueden gestionar el inventario de productos
4. Los administradores pueden crear/editar/eliminar productos y categorías

## Personalización del sistema

El sistema puede personalizarse de varias maneras:

### Temas visuales

El diseño visual se basa en Bootstrap 5 y puede personalizarse editando los archivos CSS en el directorio `static/css/`.

### Configuración del sistema

Las principales opciones de configuración se encuentran en:
- `cofeshop/settings.py`: Configuración general de Django
- `.env`: Variables de entorno sensibles (no incluir en control de versiones)

## Mantenimiento y operaciones

### Respaldo de base de datos

Para crear un respaldo de la base de datos:

```bash
python manage.py dumpdata > backup.json
```

Para restaurar:

```bash
python manage.py loaddata backup.json
```

### Actualización del sistema

Para actualizar el sistema:

1. Obtener los últimos cambios del repositorio
2. Actualizar dependencias: `pip install -r requirements.txt`
3. Aplicar migraciones: `python manage.py migrate`
4. Reiniciar el servidor

## Preguntas frecuentes

### ¿Cómo agregar un nuevo administrador?

Puede crear un nuevo administrador desde la línea de comandos:

```bash
python manage.py createsuperuser
```

O registrar un usuario normal y luego cambiar su tipo a "admin" desde el panel de administración.

### ¿Cómo cambiar la configuración de correo?

Las configuraciones de correo electrónico se encuentran en `cofeshop/settings.py`. Modifique las variables EMAIL_* según sus necesidades.

### ¿Cómo regenerar un token de autenticación?

Si necesita invalidar un token existente y generar uno nuevo:

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='usuario')
Token.objects.filter(user=user).delete()
new_token = Token.objects.create(user=user)
print(f"Nuevo token: {new_token.key}")
```

También puede hacerlo desde el shell de Django:

```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='usuario')
Token.objects.filter(user=user).delete()
new_token = Token.objects.create(user=user)
print(f"Nuevo token: {new_token.key}")
```
