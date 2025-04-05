# Guía de API REST de CoffeeShop

Esta documentación describe los endpoints disponibles en la API REST de CoffeeShop y cómo utilizarlos.

## Información General

La API REST de CoffeeShop está implementada utilizando Django REST Framework y proporciona acceso programático a los recursos del sistema. Todos los endpoints de la API REST están disponibles bajo el prefijo `/api/`.

## Autenticación

La API proporciona varios métodos de autenticación:

### Autenticación por Token

Para acceder a los endpoints protegidos, se puede utilizar autenticación por token. Para obtener un token:

```
GET/POST /api/login/
```

**Métodos disponibles:**
- **POST**: Enviar credenciales en el cuerpo de la solicitud
- **GET**: Enviar credenciales como parámetros de consulta

**POST Request:**
```json
{
  "username": "usuario",
  "password": "contraseña"
}
```

**GET Request:**
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

### Autenticación por Sesión

También se admite la autenticación por sesión de Django para aplicaciones web que utilizan la API.

## Permisos

La API implementa varios niveles de permisos:

- **IsAdminOrReadOnly**: Permite acceso de lectura a todos los usuarios, pero solo administradores pueden crear, actualizar o eliminar recursos.
- **IsOwnerOrAdmin**: Permite a los usuarios acceder solo a sus propios recursos, mientras que los administradores pueden acceder a todos.

## Endpoints Disponibles

### Categorías

```
GET /api/categories/
```

**Descripción:** Obtiene la lista de todas las categorías de productos.

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Café",
    "description": "Diferentes tipos de café",
    "created_at": "2023-05-15T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Accesorios",
    "description": "Accesorios para preparar café",
    "created_at": "2023-05-15T10:35:00Z"
  }
]
```

```
GET /api/categories/{id}/
```

**Descripción:** Obtiene los detalles de una categoría específica.

**Respuesta:**
```json
{
  "id": 1,
  "name": "Café",
  "description": "Diferentes tipos de café",
  "created_at": "2023-05-15T10:30:00Z"
}
```

```
POST /api/categories/
```

**Requisitos:**
- Autenticación como administrador

**Datos:**
```json
{
  "name": "Postres",
  "description": "Postres para acompañar el café"
}
```

**Respuesta:**
```json
{
  "id": 3,
  "name": "Postres",
  "description": "Postres para acompañar el café",
  "created_at": "2023-06-10T14:25:00Z"
}
```

```
PUT /api/categories/{id}/
```

**Requisitos:**
- Autenticación como administrador

**Datos:**
```json
{
  "name": "Postres Gourmet",
  "description": "Postres gourmet para acompañar el café"
}
```

**Respuesta:**
```json
{
  "id": 3,
  "name": "Postres Gourmet",
  "description": "Postres gourmet para acompañar el café",
  "created_at": "2023-06-10T14:25:00Z"
}
```

```
DELETE /api/categories/{id}/
```

**Requisitos:**
- Autenticación como administrador

**Respuesta:**
- Código 204 (No Content) si se elimina correctamente

### Productos

```
GET /api/products/
```

**Descripción:** Obtiene la lista de todos los productos disponibles.

**Parámetros de consulta:**
- `q`: Término de búsqueda (opcional)
- `category_id`: Filtrar por categoría (opcional)
- `available`: Filtrar por disponibilidad (opcional, true/false)

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Café Colombiano",
    "description": "Café de origen colombiano",
    "price": "12.99",
    "category": {
      "id": 1,
      "name": "Café",
      "description": "Diferentes tipos de café",
      "created_at": "2023-05-15T10:30:00Z"
    },
    "image": "/media/products/cafe_colombiano.jpg",
    "image_url": "/media/products/cafe_colombiano.jpg",
    "stock": 50,
    "available": true,
    "created_at": "2023-05-15T11:00:00Z",
    "updated_at": "2023-05-15T11:00:00Z"
  }
]
```

```
GET /api/products/{id}/
```

**Descripción:** Obtiene los detalles de un producto específico.

**Respuesta:**
```json
{
  "id": 1,
  "name": "Café Colombiano",
  "description": "Café de origen colombiano",
  "price": "12.99",
  "category": {
    "id": 1,
    "name": "Café",
    "description": "Diferentes tipos de café",
    "created_at": "2023-05-15T10:30:00Z"
  },
  "image": "/media/products/cafe_colombiano.jpg",
  "image_url": "/media/products/cafe_colombiano.jpg",
  "stock": 50,
  "available": true,
  "created_at": "2023-05-15T11:00:00Z",
  "updated_at": "2023-05-15T11:00:00Z"
}
```

```
POST /api/products/
```

**Requisitos:**
- Autenticación como administrador

**Datos:**
```json
{
  "name": "Té Verde Matcha",
  "description": "Té verde japonés premium en polvo para ceremonias",
  "price": "18.50",
  "category_id": 4,
  "image": "http://127.0.0.1:8000/media/products/te_verde.jpg",
  "stock": 40,
  "available": true
}
```

**Notas sobre campos especiales:**
- `image`: Puede ser un archivo o una URL. Si es una URL, el sistema la procesará para guardar la referencia correcta.
- `category_id`: ID de la categoría a la que pertenece el producto

**Respuesta:**
```json
{
  "id": 10,
  "name": "Té Verde Matcha",
  "description": "Té verde japonés premium en polvo para ceremonias",
  "price": "18.50",
  "category": {
    "id": 4,
    "name": "Tés",
    "description": "Variedades de té",
    "created_at": "2023-05-15T10:32:00Z"
  },
  "image": "/media/products/te_verde.jpg",
  "image_url": "/media/products/te_verde.jpg",
  "stock": 40,
  "available": true,
  "created_at": "2023-06-10T15:00:00Z",
  "updated_at": "2023-06-10T15:00:00Z"
}
```

```
PUT /api/products/{id}/
```

**Requisitos:**
- Autenticación como administrador

**Datos:**
```json
{
  "name": "Té Verde Matcha Premium",
  "description": "Té verde japonés premium en polvo para ceremonias tradicionales",
  "price": "22.50",
  "category_id": 4,
  "image": "http://127.0.0.1:8000/media/products/te_verde_premium.jpg",
  "stock": 30,
  "available": true
}
```

**Respuesta:**
```json
{
  "id": 10,
  "name": "Té Verde Matcha Premium",
  "description": "Té verde japonés premium en polvo para ceremonias tradicionales",
  "price": "22.50",
  "category": {
    "id": 4,
    "name": "Tés",
    "description": "Variedades de té",
    "created_at": "2023-05-15T10:32:00Z"
  },
  "image": "/media/products/te_verde_premium.jpg",
  "image_url": "/media/products/te_verde_premium.jpg",
  "stock": 30,
  "available": true,
  "created_at": "2023-06-10T15:00:00Z",
  "updated_at": "2023-06-10T15:05:00Z"
}
```

```
DELETE /api/products/{id}/
```

**Requisitos:**
- Autenticación como administrador

**Respuesta:**
- Código 204 (No Content) si se elimina correctamente

### Carrito de Compras

```
GET /api/carts/my_cart/
```

**Requisitos:**
- Autenticación como cliente

**Descripción:** Obtiene el carrito actual del usuario autenticado.

**Respuesta:**
```json
{
  "id": 1,
  "user": 2,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Café Colombiano",
        "description": "Café de origen colombiano",
        "price": "12.99",
        "category": {
          "id": 1,
          "name": "Café",
          "description": "Diferentes tipos de café",
          "created_at": "2023-05-15T10:30:00Z"
        },
        "image": "/media/products/cafe_colombiano.jpg",
        "image_url": "/media/products/cafe_colombiano.jpg",
        "stock": 50,
        "available": true,
        "created_at": "2023-05-15T11:00:00Z",
        "updated_at": "2023-05-15T11:00:00Z"
      },
      "quantity": 2,
      "total_price": "25.98"
    }
  ],
  "total_price": "25.98",
  "created_at": "2023-06-10T15:30:00Z",
  "updated_at": "2023-06-10T15:35:00Z"
}
```

```
POST /api/carts/add_item/
```

**Requisitos:**
- Autenticación como cliente

**Datos:**
```json
{
  "product_id": 1,
  "quantity": 1
}
```

**Respuesta:**
El carrito actualizado con el nuevo item.

```
POST /api/carts/remove_item/
```

**Requisitos:**
- Autenticación como cliente

**Datos:**
```json
{
  "item_id": 1
}
```

**Respuesta:**
El carrito actualizado sin el item eliminado o con su cantidad reducida.

### Pedidos

```
GET /api/orders/
```

**Requisitos:**
- Autenticación como cliente (ve solo sus pedidos)
- Autenticación como administrador o empleado (ve todos los pedidos)

**Descripción:** Obtiene la lista de pedidos según el tipo de usuario.

**Respuesta:**
```json
[
  {
    "id": 1,
    "user": {
      "id": 2,
      "username": "cliente1",
      "email": "cliente1@example.com",
      "user_type": "customer",
      "phone": "123456789",
      "address": "Calle Principal 123",
      "city": "Ciudad"
    },
    "full_name": "Cliente Ejemplo",
    "email": "cliente@example.com",
    "address": "Calle Principal 123",
    "phone": "123456789",
    "total_amount": "25.98",
    "status": "pending",
    "status_display": "Pendiente",
    "notes": "",
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "Café Colombiano",
          "description": "Café de origen colombiano",
          "price": "12.99",
          "category": {
            "id": 1,
            "name": "Café",
            "description": "Diferentes tipos de café",
            "created_at": "2023-05-15T10:30:00Z"
          },
          "image": "/media/products/cafe_colombiano.jpg",
          "image_url": "/media/products/cafe_colombiano.jpg",
          "stock": 50,
          "available": true,
          "created_at": "2023-05-15T11:00:00Z",
          "updated_at": "2023-05-15T11:00:00Z"
        },
        "price": "12.99",
        "quantity": 2
      }
    ],
    "created_at": "2023-06-10T16:00:00Z",
    "updated_at": "2023-06-10T16:00:00Z"
  }
]
```

```
GET /api/orders/{id}/
```

**Requisitos:**
- Autenticación como cliente (solo su pedido)
- Autenticación como administrador o empleado (cualquier pedido)

**Descripción:** Obtiene los detalles de un pedido específico.

**Respuesta:**
Misma estructura que en el ejemplo anterior, pero para un pedido específico.

```
POST /api/orders/checkout/
```

**Requisitos:**
- Autenticación como cliente
- Carrito no vacío

**Datos:**
```json
{
  "full_name": "Cliente Ejemplo",
  "email": "cliente@example.com",
  "address": "Calle Principal 123",
  "phone": "123456789"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "cliente1",
    "email": "cliente1@example.com",
    "user_type": "customer",
    "phone": "123456789",
    "address": "Calle Principal 123",
    "city": "Ciudad"
  },
  "full_name": "Cliente Ejemplo",
  "email": "cliente@example.com",
  "address": "Calle Principal 123",
  "phone": "123456789",
  "total_amount": "25.98",
  "status": "pending",
  "status_display": "Pendiente",
  "notes": "",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Café Colombiano",
        "description": "Café de origen colombiano",
        "price": "12.99",
        "category": {
          "id": 1,
          "name": "Café",
          "description": "Diferentes tipos de café",
          "created_at": "2023-05-15T10:30:00Z"
        },
        "image": "/media/products/cafe_colombiano.jpg",
        "image_url": "/media/products/cafe_colombiano.jpg",
        "stock": 50,
        "available": true,
        "created_at": "2023-05-15T11:00:00Z",
        "updated_at": "2023-05-15T11:00:00Z"
      },
      "price": "12.99",
      "quantity": 2
    }
  ],
  "created_at": "2023-06-10T16:00:00Z",
  "updated_at": "2023-06-10T16:00:00Z"
}
```

```
POST /api/orders/{id}/update_status/
```

**Requisitos:**
- Autenticación como administrador o empleado

**Datos:**
```json
{
  "status": "processing",
  "notes": "Pedido en preparación"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "cliente1",
    "email": "cliente1@example.com",
    "user_type": "customer",
    "phone": "123456789",
    "address": "Calle Principal 123",
    "city": "Ciudad"
  },
  "full_name": "Cliente Ejemplo",
  "email": "cliente@example.com",
  "address": "Calle Principal 123",
  "phone": "123456789",
  "total_amount": "25.98",
  "status": "processing",
  "status_display": "En Proceso",
  "notes": "Pedido en preparación",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Café Colombiano",
        "description": "Café de origen colombiano",
        "price": "12.99",
        "category": {
          "id": 1,
          "name": "Café",
          "description": "Diferentes tipos de café",
          "created_at": "2023-05-15T10:30:00Z"
        },
        "image": "/media/products/cafe_colombiano.jpg",
        "image_url": "/media/products/cafe_colombiano.jpg",
        "stock": 50,
        "available": true,
        "created_at": "2023-05-15T11:00:00Z",
        "updated_at": "2023-05-15T11:00:00Z"
      },
      "price": "12.99",
      "quantity": 2
    }
  ],
  "created_at": "2023-06-10T16:00:00Z",
  "updated_at": "2023-06-10T16:10:00Z"
}
```

## Códigos de Estado HTTP

La API utiliza los siguientes códigos de estado HTTP:

- `200 OK`: La solicitud se ha completado correctamente
- `201 Created`: El recurso se ha creado correctamente
- `204 No Content`: La solicitud se completó pero no hay contenido para devolver
- `400 Bad Request`: La solicitud contiene datos inválidos
- `401 Unauthorized`: Es necesario autenticarse
- `403 Forbidden`: No se tienen permisos para acceder al recurso
- `404 Not Found`: El recurso solicitado no existe
- `500 Internal Server Error`: Error interno del servidor

## Ejemplos de Uso

### Crear un producto usando scripts

Este es un ejemplo de cómo crear un producto usando Python y la biblioteca requests:

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
print(f'Código de Estado de Creación del Producto: {response.status_code}')
try:
    print(json.dumps(response.json(), indent=2))
except:
    print(response.text) 
```

### Obtener un token de autenticación

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

# Solicitar lista de pedidos con el token
orders_response = requests.get('http://127.0.0.1:8000/api/orders/', 
                              headers=headers)

print(f'Código de Estado de Pedidos: {orders_response.status_code}')
print(json.dumps(orders_response.json(), indent=2))
```

## Consideraciones para Integración

Si deseas integrar con la API REST de CoffeeShop, ten en cuenta las siguientes consideraciones:

1. La API devuelve respuestas en formato JSON.
2. Todos los endpoints están disponibles bajo el prefijo `/api/`.
3. Para acceder a endpoints protegidos, es necesario estar autenticado.
4. Las rutas pueden cambiar en futuras versiones, por lo que se recomienda verificar la documentación actualizada.

## Desarrollo Futuro

En futuras versiones, se planea implementar:

1. Autenticación mediante tokens JWT
2. Paginación para listas grandes de recursos
3. Filtros adicionales para búsquedas más específicas
4. Documentación interactiva con Swagger/OpenAPI