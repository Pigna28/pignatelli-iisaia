# Registro de prompts — TP 2

Los tres prompts se hicieron en una misma conversación. El archivo `openapi.yaml` se fue completando y corrigiendo en cada paso.
Para el primer prompt se adjuntaron los archivos del TP1

---

## 1. Prompt inicial

```text
Necesito hacer un archivo `openapi.yaml` para complementar la tienda gamer que hice en el TP1.

Quiero que la API maneje carritos de compra y los productos que tiene cada carrito.

Los datos principales serían:

Cart:
- id
- created_at

CartItem:
- id
- product_id
- quantity
- cart_id

Quiero estos endpoints:

- GET /carts para ver los carritos
- POST /carts para crear un carrito
- GET /carts/{cartId}/items para ver los productos de un carrito
- POST /carts/{cartId}/items para agregar un producto al carrito

Si el carrito no existe, usar error 404.

Al agregar un producto, el usuario solo debería mandar product_id y quantity. El id y cart_id los define el servidor.

Usá OpenAPI 3.1 y devolveme solamente el contenido del `openapi.yaml`.
```

### Qué intentaba lograr

Crear la estructura principal de la API y relacionarla con el carrito que ya existía en el TP1.

También quería diferenciar los datos que manda el usuario de los datos que genera el servidor.

---

## 2. Agregar eliminación de productos

```text
Ahora agregá un endpoint para eliminar un producto del carrito:

DELETE /carts/{cartId}/items/{itemId}

Si se elimina correctamente, debe devolver 204.

Si el carrito o el item no existen, debe devolver 404.

No cambies lo que ya estaba hecho.

Devolveme el `openapi.yaml` completo.
```

### Qué intentaba lograr

Agregar la operación que faltaba para poder eliminar productos del carrito.

Elegí que la eliminación correcta devuelva `204` porque no necesito devolver ningún contenido después de borrar el item.

---

## 3. Revisión final

```text
Revisá el `openapi.yaml` completo y corregí cualquier problema.

Quiero que:

- al agregar un producto solo se envíen product_id y quantity;
- cart_id no esté en el body porque ya se sabe por la URL;
- quantity sea como mínimo 1;
- los ids los genere el servidor;
- los errores 404 estén donde correspondan;
- DELETE devuelva 204;
- no agregues endpoints nuevos.

El archivo final debe tener estos tres paths:

- /carts
- /carts/{cartId}/items
- /carts/{cartId}/items/{itemId}

Devolveme solamente el `openapi.yaml` final, listo para usar en Swagger Editor.
```

### Qué intentaba lograr

Hacer una revisión final del contrato antes de entregarlo.

La corrección más importante fue asegurar que `cart_id` no se enviara en el body cuando se agrega un producto, porque el carrito ya está identificado mediante `cartId` en la URL.

También revisé que `quantity` no pueda ser menor que 1 y que los códigos `404` y `204` estén usados correctamente.

---

## Resultado

El resultado final es una API de carrito con 5 operaciones repartidas en 3 paths:

```text
/carts
/carts/{cartId}/items
/carts/{cartId}/items/{itemId}
```

El archivo final se encuentra en `openapi.yaml`.
