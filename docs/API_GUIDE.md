# Guía de API de CoffeeShop

Esta documentación describe los endpoints disponibles en la API de CoffeeShop y cómo utilizarlos.

## Información General

La API de CoffeeShop sigue los principios RESTful y utiliza el framework Django. Actualmente, la API está diseñada principalmente para uso interno de la aplicación web, pero puede ser utilizada para integraciones con otros sistemas.

## Autenticación

### Autenticación Web

Para acceder a los endpoints protegidos desde la aplicación web, es necesario estar autenticado. La autenticación se realiza mediante sesiones de Django.

### Autenticación de API

Para integraciones con otros sistemas, se proporciona autenticación mediante tokens. Para obtener un token:

```
GET/POST /api/login/
```

**Métodos disponibles:**
- **POST**: Enviar credenciales en el cuerpo de la solicitud
- **GET**: Enviar credenciales como parámetros de consulta

Para usar el token, incluirlo en el encabezado de las solicitudes:
```
Authorization: Token tu_token_de_autenticación
```

## API REST

La API REST está disponible bajo el prefijo `/api/`. Para más detalles sobre los endpoints REST, consulte la [Guía de API REST](API_GUIDE_REST.md).

## Endpoints Disponibles

### Administración

#### Inicio de Sesión del Panel Administrativo

```
GET/POST /manage/login/
```

**Descripción:** Página de inicio de sesión para el panel administrativo. Solo accesible para usuarios con tipo 'admin' o 'employee'.

**Métodos disponibles:**
- **GET**: Muestra el formulario de inicio de sesión
- **POST**: Procesa las credenciales enviadas

**Parámetros (POST):**
- `username`: Nombre de usuario
- `password`: Contraseña

**Respuesta (GET):**
Página HTML con el formulario de inicio de sesión

**Respuesta (POST exitoso):**
Redirección a `/manage/dashboard/` si las credenciales son válidas y el usuario tiene permisos adecuados

**Respuesta (POST fallido):**
Página de inicio de sesión con mensaje de error

**Códigos de estado:**
- `200 OK`: Formulario de inicio de sesión o error de autenticación
- `302 Found`: Redirección tras inicio de sesión exitoso
- `403 Forbidden`: Si un usuario sin permisos intenta acceder

**Notas de seguridad:**
- Esta ruta implementa limitación de intentos para prevenir ataques de fuerza bruta
- La sesión expira después de 30 minutos de inactividad
- Las contraseñas se transmiten de forma segura mediante HTTPS (en producción)

#### Gestión de Inventario

```
GET /manage/inventory/
```

**Requisitos:**
- Autenticación como administrador

**Respuesta:**
Página HTML con el estado actual del inventario

```
POST /manage/inventory/add-stock/
```

**Parámetros:**
- `product_id`: ID del producto
- `quantity`: Cantidad a añadir

**Respuesta:**
Redirección a la página de gestión de inventario con mensaje de confirmación

```
POST /manage/orders/{order_id}/inventory/
```

**Parámetros:**
- `order_id`: ID de la orden
- `action`: 'add' o 'remove'
- `product_id`: ID del producto
- `quantity`: Cantidad a modificar

**Respuesta:**
Redirección a la página de detalle de orden con mensaje de confirmación

### Usuarios

#### Registro de Usuarios

```
POST /register/
```

**Parámetros:**
- `username`: Nombre de usuario
- `email`: Correo electrónico
- `password1`: Contraseña
- `password2`: Confirmación de contraseña
- `user_type`: Tipo de usuario (customer/employee/admin)

**Respuesta:**
Redirección a la página principal tras registro exitoso

#### Inicio de Sesión

```
POST /login/
```

**Parámetros:**
- `username`: Nombre de usuario
- `password`: Contraseña

**Respuesta:**
Redirección a la página principal tras inicio de sesión exitoso o mensaje de error

### Productos

#### Listar Productos

```
GET /products/
```

**Parámetros de consulta:**
- `q`: Término de búsqueda (opcional)
- `category_id`: Filtrar por categoría (opcional)

**Respuesta:**
Página HTML con la lista de productos que coinciden con los criterios de búsqueda.

#### Detalle de Producto

```
GET /product/{product_id}/
```

**Parámetros:**
- `product_id`: ID del producto

**Respuesta:**
Página HTML con los detalles del producto especificado.

### Carrito de Compras

#### Ver Carrito

```
GET /cart/
```

**Requisitos:**
- Usuario autenticado

**Respuesta:**
Página HTML con el contenido actual del carrito del usuario.

#### Añadir al Carrito

```
GET /add/{product_id}/
```

**Parámetros:**
- `product_id`: ID del producto a añadir

**Requisitos:**
- Usuario autenticado

**Respuesta:**
Redirección a la página del carrito con el producto añadido.

#### Eliminar del Carrito

```
GET /remove/{item_id}/
```

**Parámetros:**
- `item_id`: ID del item del carrito a eliminar

**Requisitos:**
- Usuario autenticado
- El item debe pertenecer al carrito del usuario

**Respuesta:**
Redirección a la página del carrito con el item eliminado o su cantidad reducida.

### Pedidos

#### Proceso de Checkout

```
GET /checkout/
```

**Requisitos:**
- Usuario autenticado
- Carrito no vacío

**Respuesta:**
Página HTML con el formulario de checkout.

```
POST /checkout/
```

**Datos del formulario:**
- `full_name`: Nombre completo
- `email`: Correo electrónico
- `address`: Dirección de envío
- `phone`: Número de teléfono

**Requisitos:**
- Usuario autenticado
- Carrito no vacío

**Respuesta:**
Redirección a la página de confirmación de pedido.

#### Confirmación de Pedido

```
GET /order/complete/{order_id}/
```

**Parámetros:**
- `order_id`: ID del pedido completado

**Requisitos:**
- Usuario autenticado
- El pedido debe pertenecer al usuario

**Respuesta:**
Página HTML con los detalles del pedido completado.

#### Historial de Pedidos

```
GET /orders/
```

**Requisitos:**
- Usuario autenticado

**Respuesta:**
Página HTML con la lista de pedidos del usuario.

## Códigos de Estado HTTP

La API utiliza los siguientes códigos de estado HTTP:

- `200 OK`: La solicitud se ha completado correctamente
- `201 Created`: El recurso se ha creado correctamente
- `204 No Content`: La solicitud se completó pero no hay contenido para devolver
- `302 Found`: Redirección a otra página
- `400 Bad Request`: La solicitud contiene datos inválidos
- `401 Unauthorized`: Es necesario autenticarse
- `403 Forbidden`: No se tienen permisos para acceder al recurso
- `404 Not Found`: El recurso solicitado no existe
- `500 Internal Server Error`: Error interno del servidor

## Integración con Sistemas Externos

Para integrar la tienda con sistemas externos, se recomienda utilizar la API REST. Para más detalles, consulte la [Guía de API REST](API_GUIDE_REST.md).

### Ejemplo de Autenticación con Python

```python
import requests
import json

# Credenciales de usuario
credentials = {
    "username": "admin",
    "password": "adminpassword"
}

# Solicitar token de autenticación
response = requests.post('http://127.0.0.1:8000/api/login/', 
                        json=credentials)

# Imprimir respuesta
print(f'Código de Estado: {response.status_code}')
print(json.dumps(response.json(), indent=2))

# Guardar token para uso posterior
token = response.json()['token']
print(f'Token: {token}')

# Ejemplo de uso del token en una solicitud
headers = {
    'Authorization': f'Token {token}'
}

# Solicitar lista de productos con el token
products_response = requests.get('http://127.0.0.1:8000/api/products/', 
                               headers=headers)

print(f'Código de Estado de Productos: {products_response.status_code}')
print(json.dumps(products_response.json(), indent=2))
```

## Desarrollo Futuro

En futuras versiones, se planea implementar:

1. Autenticación mediante tokens JWT para la API REST
2. Paginación para listas grandes de recursos
3. Filtros adicionales para búsquedas más específicas
4. Documentación interactiva con Swagger/OpenAPI