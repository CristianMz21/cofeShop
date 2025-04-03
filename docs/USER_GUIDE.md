# Guía de Usuario de CoffeeShop

Esta guía proporciona instrucciones detalladas sobre cómo utilizar la aplicación CoffeeShop según el tipo de usuario.

## Tipos de Usuarios

La aplicación CoffeeShop tiene tres tipos de usuarios, cada uno con diferentes niveles de acceso y funcionalidades:

1. **Administradores**: Control total del sistema
2. **Empleados**: Gestión de productos y pedidos
3. **Clientes**: Navegación, compra y seguimiento de pedidos

## Acceso al Sistema

### Iniciar Sesión

1. Accede a la página principal: http://127.0.0.1:8000/
2. Haz clic en "Iniciar Sesión" en la barra de navegación
3. Introduce tu nombre de usuario y contraseña
4. Haz clic en "Acceder"

### Cerrar Sesión

1. Haz clic en tu nombre de usuario en la barra de navegación
2. Selecciona "Cerrar Sesión"

## Guía para Clientes

### Navegación por el Catálogo

1. **Ver todos los productos**: Accede a la sección "Productos" desde el menú principal
2. **Filtrar por categoría**: Selecciona una categoría en el menú lateral
3. **Buscar productos**: Utiliza la barra de búsqueda en la parte superior

### Gestión del Carrito de Compras

1. **Añadir productos al carrito**:
   - Navega hasta el producto deseado
   - Haz clic en "Añadir al Carrito"

2. **Ver el carrito**:
   - Haz clic en el icono del carrito en la barra de navegación
   - Verás todos los productos añadidos, cantidades y precio total

3. **Modificar cantidades**:
   - En la página del carrito, puedes aumentar o disminuir la cantidad de cada producto
   - Haz clic en "+" para aumentar o "-" para disminuir

4. **Eliminar productos**:
   - Haz clic en "Eliminar" junto al producto que deseas quitar del carrito

### Proceso de Compra

1. **Iniciar checkout**:
   - En la página del carrito, haz clic en "Proceder al Pago"

2. **Completar información de envío**:
   - Rellena el formulario con tu nombre completo, dirección, teléfono y email
   - Si ya has iniciado sesión, estos campos pueden estar pre-rellenados

3. **Confirmar pedido**:
   - Revisa el resumen de tu pedido
   - Haz clic en "Confirmar Pedido"

4. **Confirmación**:
   - Recibirás una página de confirmación con los detalles de tu pedido
   - También recibirás un email con la confirmación

### Historial de Pedidos

1. **Ver pedidos anteriores**:
   - Accede a "Mi Cuenta" > "Mis Pedidos"
   - Verás una lista de todos tus pedidos ordenados por fecha

2. **Ver detalles de un pedido**:
   - Haz clic en "Ver Detalles" junto al pedido que te interese
   - Podrás ver los productos, cantidades, precios y estado del pedido

## Guía para Empleados

Los empleados tienen acceso al panel de administración con permisos limitados.

### Acceso al Panel de Administración

1. Accede a http://127.0.0.1:8000/admin/
2. Introduce tus credenciales de empleado

### Gestión de Productos

1. **Ver productos**:
   - En el panel de administración, haz clic en "Products"
   - Verás la lista de todos los productos disponibles

2. **Añadir nuevo producto**:
   - Haz clic en "Add Product"
   - Rellena el formulario con la información del producto
   - Sube una imagen del producto
   - Haz clic en "Save"

3. **Editar producto existente**:
   - Haz clic en el nombre del producto que deseas editar
   - Modifica los campos necesarios
   - Haz clic en "Save"

4. **Gestionar stock**:
   - Edita el producto y actualiza el campo "Stock"
   - Marca o desmarca "Available" según corresponda

### Gestión de Pedidos

1. **Ver pedidos**:
   - En el panel de administración, haz clic en "Orders"
   - Verás la lista de todos los pedidos

2. **Actualizar estado de un pedido**:
   - Haz clic en el número de pedido
   - Cambia el campo "Status" al estado correspondiente
   - Haz clic en "Save"

3. **Ver detalles de un pedido**:
   - Los detalles de los productos se muestran en la sección "Order Items"

## Guía para Administradores

Los administradores tienen control total sobre el sistema.

### Gestión de Usuarios

1. **Ver usuarios**:
   - En el panel de administración, haz clic en "Users"
   - Verás la lista de todos los usuarios registrados

2. **Añadir nuevo usuario**:
   - Haz clic en "Add User"
   - Rellena el formulario con la información del usuario
   - Asigna el tipo de usuario (admin, employee, customer)
   - Haz clic en "Save"

3. **Editar usuario existente**:
   - Haz clic en el nombre del usuario que deseas editar
   - Modifica los campos necesarios
   - Haz clic en "Save"

4. **Desactivar usuario**:
   - Edita el usuario y desmarca la casilla "Active"
   - Esto impide que el usuario inicie sesión sin eliminar su cuenta

### Gestión de Categorías

1. **Ver categorías**:
   - En el panel de administración, haz clic en "Categories"
   - Verás la lista de todas las categorías

2. **Añadir nueva categoría**:
   - Haz clic en "Add Category"
   - Rellena el nombre y descripción
   - Haz clic en "Save"

3. **Editar categoría existente**:
   - Haz clic en el nombre de la categoría
   - Modifica los campos necesarios
   - Haz clic en "Save"

### Informes y Estadísticas

Como administrador, puedes acceder a información detallada sobre ventas y actividad:

1. **Ver pedidos por período**:
   - Utiliza los filtros de fecha en la sección "Orders"

2. **Analizar ventas por producto**:
   - Revisa los detalles de pedidos para ver qué productos se venden más

## Solución de Problemas Comunes

### Problemas de Inicio de Sesión

- **Contraseña olvidada**: Utiliza la opción "¿Olvidaste tu contraseña?" en la página de inicio de sesión
- **Cuenta bloqueada**: Contacta con un administrador para reactivar tu cuenta

### Problemas con el Carrito

- **Productos no disponibles**: Si un producto se agota después de añadirlo al carrito, se te notificará durante el checkout
- **Carrito vacío inesperadamente**: Las sesiones pueden caducar; vuelve a añadir los productos

### Problemas con los Pedidos

- **Pedido no aparece en historial**: Asegúrate de haber completado el proceso de checkout
- **Estado de pedido incorrecto**: Contacta con atención al cliente para resolver el problema