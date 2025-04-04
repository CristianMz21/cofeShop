# Guía de API de CoffeeShop

Esta documentación describe los endpoints disponibles en la API de CoffeeShop y cómo utilizarlos.

## Información General

La API de CoffeeShop sigue los principios RESTful y utiliza el framework Django. Actualmente, la API está diseñada principalmente para uso interno de la aplicación web, pero puede ser utilizada para integraciones con otros sistemas.

## Autenticación

Para acceder a los endpoints protegidos, es necesario estar autenticado. La autenticación se realiza mediante sesiones de Django.

## Endpoints Disponibles

### Administración

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

### Carrito de Compras

#### Añadir Producto

```
POST /cart/add/<product_id>/
```

**Requisitos:**
- Autenticación como cliente

**Respuesta:**
Redirección al carrito

#### Ver Carrito

```
GET /cart/view/
```

**Requisitos:**
- Autenticación como cliente

**Respuesta:**
Página HTML con los productos en el carrito

#### Eliminar Producto

```
POST /cart/remove/<product_id>/
```

**Requisitos:**
- Autenticación como cliente

**Respuesta:**
Redirección al carrito

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
- `302 Found`: Redirección a otra página
- `400 Bad Request`: La solicitud contiene datos inválidos
- `401 Unauthorized`: Es necesario autenticarse
- `403 Forbidden`: No se tienen permisos para acceder al recurso
- `404 Not Found`: El recurso solicitado no existe
- `500 Internal Server Error`: Error interno del servidor

## Ejemplos de Uso

### Ejemplo 1: Buscar productos por término

```
GET /products/?q=café
```

Muestra todos los productos que contienen "café" en su nombre o descripción.

### Ejemplo 2: Filtrar productos por categoría

```
GET /category/1/
```

Muestra todos los productos de la categoría con ID 1 (Café).

### Ejemplo 3: Añadir un producto al carrito

```
GET /add/2/
```

Añade el producto con ID 2 (Café Etíope) al carrito del usuario autenticado.

## Consideraciones para Integración

Si deseas integrar con la API de CoffeeShop, ten en cuenta las siguientes consideraciones:

1. La API actual está diseñada principalmente para la aplicación web, por lo que devuelve HTML en lugar de JSON/XML.
2. Para integraciones más avanzadas, se recomienda implementar una API REST dedicada utilizando Django REST Framework.
3. Las rutas pueden cambiar en futuras versiones, por lo que se recomienda verificar la documentación actualizada.

## Desarrollo Futuro

En futuras versiones, se planea implementar:

1. API REST completa con respuestas en formato JSON
2. Autenticación mediante tokens
3. Endpoints adicionales para gestión de usuarios y categorías
4. Documentación interactiva con Swagger/OpenAPI