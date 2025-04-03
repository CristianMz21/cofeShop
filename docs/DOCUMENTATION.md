# Documentación Técnica de CoffeeShop

Este documento proporciona información técnica detallada sobre la aplicación CoffeeShop, su arquitectura, modelos de datos y funcionalidades principales.

## Arquitectura del Sistema

CoffeeShop está desarrollado utilizando el framework Django, siguiendo el patrón de arquitectura Modelo-Vista-Controlador (MVC), que en Django se implementa como Modelo-Vista-Template (MVT):

- **Modelos**: Definen la estructura de datos y la lógica de negocio
- **Vistas**: Manejan la lógica de presentación y procesamiento de solicitudes
- **Templates**: Definen cómo se presenta la información al usuario

## Modelos de Datos

### Usuario (User)

Extiende el modelo de usuario de Django para incluir información adicional:

- **Tipos de usuario**: Administrador, Empleado, Cliente
- **Campos adicionales**: Teléfono, Dirección
- **Métodos**: `is_admin()`, `is_employee()`, `is_customer()`

### Categoría (Category)

Permite organizar los productos en grupos lógicos:

- **Campos**: Nombre, Descripción, Fecha de creación

### Producto (Product)

Representa los artículos disponibles para la venta:

- **Campos**: Nombre, Descripción, Precio, Categoría, Imagen, Stock, Disponibilidad
- **Relaciones**: Pertenece a una Categoría

### Orden/Pedido (Order)

Registra las compras realizadas por los usuarios:

- **Estados**: Pendiente, En Proceso, Enviado, Entregado, Cancelado
- **Campos**: Usuario, Nombre completo, Email, Dirección, Teléfono, Monto total, Estado
- **Relaciones**: Pertenece a un Usuario, contiene múltiples OrderItem

### Detalle de Orden (OrderItem)

Representa cada producto incluido en una orden:

- **Campos**: Orden, Producto, Precio, Cantidad
- **Métodos**: `get_total_price()`

### Carrito de Compras (Cart)

Almacena temporalmente los productos que un usuario desea comprar:

- **Campos**: Usuario, Fechas de creación y actualización
- **Métodos**: `get_total_price()`

### Item del Carrito (CartItem)

Representa cada producto añadido al carrito:

- **Campos**: Carrito, Producto, Cantidad
- **Métodos**: `get_total_price()`

## Flujos Principales

### Proceso de Compra

1. **Navegación del catálogo**: El usuario navega por las categorías y productos
2. **Añadir al carrito**: El usuario añade productos a su carrito
3. **Gestión del carrito**: El usuario puede modificar cantidades o eliminar productos
4. **Checkout**: El usuario proporciona información de envío y confirma la compra
5. **Confirmación**: Se crea una orden y se vacía el carrito

### Gestión de Usuarios

- **Registro**: Los usuarios pueden crear una cuenta como cliente
- **Autenticación**: Sistema de login/logout
- **Perfiles**: Los usuarios pueden ver y editar su información personal
- **Historial**: Los usuarios pueden ver sus pedidos anteriores

## Panel de Administración

El panel de administración de Django está personalizado para gestionar todos los aspectos de la tienda:

- **Gestión de usuarios**: Crear, editar y desactivar usuarios
- **Gestión de productos**: Añadir, editar y eliminar productos y categorías
- **Gestión de pedidos**: Ver, actualizar estado y gestionar pedidos

## Configuración del Sistema

### Base de Datos

La aplicación utiliza PostgreSQL como sistema de gestión de base de datos:

- **Configuración**: Definida en `settings.py` y variables de entorno
- **Migraciones**: Gestionadas por Django ORM

### Archivos Estáticos y Media

- **Estáticos**: CSS, JavaScript y otros recursos estáticos
- **Media**: Imágenes de productos subidas por los administradores

### Variables de Entorno

La aplicación utiliza variables de entorno para configuración sensible:

- **SECRET_KEY**: Clave secreta de Django
- **DEBUG**: Modo de depuración
- **Configuración de BD**: Credenciales y parámetros de conexión

## Datos Iniciales (Fixtures)

La aplicación incluye datos iniciales para facilitar el desarrollo y pruebas:

- **users_data.json**: Usuarios predefinidos (admin, empleados, clientes)
- **initial_data.json**: Categorías y productos de ejemplo

## Seguridad

- **Autenticación**: Sistema de autenticación de Django
- **Autorización**: Permisos basados en tipo de usuario
- **CSRF Protection**: Protección contra falsificación de solicitudes entre sitios
- **Contraseñas**: Almacenadas con hash seguro (PBKDF2 SHA256)

## Extensibilidad

La aplicación está diseñada para ser fácilmente extensible:

- **Nuevos tipos de productos**: Añadiendo categorías
- **Métodos de pago**: Preparado para integrar pasarelas de pago
- **Internacionalización**: Soporte para múltiples idiomas mediante el sistema i18n de Django

## Consideraciones para Producción

- **Configuración de servidor web**: Nginx/Apache con Gunicorn/uWSGI
- **Seguridad**: Deshabilitar DEBUG, configurar ALLOWED_HOSTS
- **Base de datos**: Optimizar configuración de PostgreSQL
- **Archivos estáticos**: Configurar almacenamiento y servicio adecuados
- **Backups**: Implementar estrategia de copias de seguridad