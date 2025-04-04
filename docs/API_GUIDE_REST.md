# Guía de API REST de CoffeeShop

Esta documentación describe los endpoints disponibles en la API REST de CoffeeShop y cómo utilizarlos.

## Información General

La API REST de CoffeeShop está implementada utilizando Django REST Framework y proporciona acceso programático a los recursos del sistema. Todos los endpoints de la API REST están disponibles bajo el prefijo `/api/`.

## Autenticación

Para acceder a los endpoints protegidos, es necesario estar autenticado. La API utiliza autenticación basada en sesiones de Django. En futuras versiones, se implementará autenticación mediante tokens.

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
  "stock": 50,
  "available": true,
  "created_at": "2023-05-15T11:00:00Z",
  "updated_at": "2023-05-15T11:00:00Z"
}
```

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
- Autenticación como administrador (ve todos los pedidos)

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
    "address": "Calle Principal 123, Ciudad",
    "phone": "123456789",
    "total_amount": "25.98",
    "status": "pending",
    "status_display": "Pendiente",
    "notes": null,
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
  "address": "Calle Principal 123, Ciudad",
  "phone": "123456789"
}
```

**Respuesta:**
El pedido creado con los detalles completos.

```
POST /api/orders/{id}/update_status/
```

**Requisitos:**
- Autenticación como administrador o empleado

**Datos:**
```json
{
  "status": "processing"
}
```

**Respuesta:**
El pedido actualizado con el nuevo estado.

## Códigos de Estado HTTP

La API utiliza los siguientes códigos de estado HTTP:

- `200 OK`: La solicitud se ha completado correctamente
- `201 Created`: El recurso se ha creado correctamente
- `400 Bad Request`: La solicitud contiene datos inválidos
- `401 Unauthorized`: Es necesario autenticarse
- `403 Forbidden`: No se tienen permisos para acceder al recurso
- `404 Not Found`: El recurso solicitado no existe
- `500 Internal Server Error`: Error interno del servidor

## Ejemplos de Uso

### Ejemplo 1: Buscar productos por término

```
GET /api/products/?q=café
```

Devuelve todos los productos que contienen "café" en su nombre o descripción.

### Ejemplo 2: Filtrar productos por categoría

```
GET /api/products/?category_id=1
```

Devuelve todos los productos de la categoría con ID 1 (Café).

### Ejemplo 3: Añadir un producto al carrito

```
POST /api/carts/add_item/
```

Con los siguientes datos:
```json
{
  "product_id": 2,
  "quantity": 1
}
```

Añade el producto con ID 2 (Café Etíope) al carrito del usuario autenticado.

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