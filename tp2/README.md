# TP 2 — API de carrito para tienda gamer

## Introducción

Este trabajo complementa el TP1 de la tienda gamer.

En el TP1 el carrito funcionaba directamente dentro del archivo HTML. Para este TP decidí definir una API que represente los carritos de compra y los productos agregados a cada carrito.

El objetivo del trabajo es crear el contrato de la API usando OpenAPI. No se implementa un servidor real.

## Cómo se usa

El archivo `openapi.yaml` se puede copiar y pegar en Swagger Editor:

https://editor.swagger.io

Ahí se puede visualizar la documentación de la API y revisar los endpoints definidos.

## Qué me propuse construir

Elegí trabajar con dos recursos principales:

- `Cart`, que representa un carrito de compra.
- `CartItem`, que representa un producto agregado a un carrito.

La relación entre ellos es directa: un carrito puede tener varios items y cada item pertenece a un carrito.

La API final tiene 5 operaciones distribuidas en 3 paths:

- `GET /carts`
- `POST /carts`
- `GET /carts/{cartId}/items`
- `POST /carts/{cartId}/items`
- `DELETE /carts/{cartId}/items/{itemId}`

## Decisiones que tomé

### Usar carritos e items

Elegí modelar el carrito porque es una funcionalidad que ya existía en el TP1, pero allí funcionaba solamente de manera local dentro de la página.

De esta forma, el TP2 complementa el trabajo anterior en lugar de crear una API sin relación con la tienda.

### Separar los datos de entrada y salida

Cuando se agrega un producto al carrito, el cliente solamente envía:

- `product_id`
- `quantity`

El `id` del item lo genera el servidor.

El `cart_id` tampoco se envía en el body porque el carrito ya está identificado en la URL mediante `cartId`.

### Cantidad mínima de productos

Definí que `quantity` tenga un valor mínimo de 1, porque no tendría sentido agregar un producto al carrito con cantidad 0 o negativa.

### Errores 404

Los endpoints que trabajan con un carrito específico pueden devolver `404` cuando ese carrito no existe.

También se devuelve `404` al intentar eliminar un item que no existe.

### DELETE con código 204

Cuando un item se elimina correctamente se devuelve `204`, sin contenido en la respuesta.

## Proceso

El archivo se generó utilizando tres prompts en una misma conversación.

En el primer prompt definí los recursos y los endpoints principales.

En el segundo agregué la posibilidad de eliminar un producto del carrito.

En el tercero pedí una revisión completa del archivo para corregir posibles errores, principalmente evitar repetir `cart_id` en el body y asegurar que los códigos de respuesta fueran correctos.

## Archivos

- `openapi.yaml`: contrato final de la API.
- `prompts.md`: registro de los prompts utilizados para generar y corregir el archivo.
- `README.md`: explicación general del trabajo.
