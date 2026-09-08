# E-commerce Gamer con UX intencionalmente absurda

## Introducción

Este proyecto consiste en una página web de e-commerce de productos gamer desarrollada como una experiencia funcional.

La idea principal fue explorar qué pasa cuando una interfaz visualmente cuidada incorpora interacciones que van en contra de las convenciones habituales de usabilidad, sin llegar a romper técnicamente la experiencia.

El resultado es una tienda gamer con estética oscura, detalles neón, catálogo de productos, carrito y una serie de mecánicas absurdas pensadas para incomodar al usuario de manera intencional.

## Cómo se ejecuta

El proyecto está pensado para funcionar directamente desde un único archivo HTML.

1. Descargar o clonar los archivos del proyecto.
2. Abrir el archivo `.html` principal en un navegador web.


## Qué me propuse construir

Me propuse crear una página de compra de productos gamer que tuviera una apariencia relativamente profesional, pero que utilizara patrones de interacción intencionalmente malos.

Las tres ideas principales fueron:

- Un botón **Comprar** que se escapa cuando el usuario intenta alcanzarlo.
- Un sistema de categorías representado mediante un **árbol genealógico gamer** innecesariamente complejo.
- Un sistema para eliminar productos del carrito que obliga al usuario a pasar por una **cadena exagerada de confirmaciones**.

El objetivo no era hacer una página visualmente fea ni técnicamente defectuosa, sino construir una interfaz funcional en la que la mala experiencia de usuario surgiera principalmente de las interacciones.

## Decisiones que tomé yo

Durante el desarrollo tomé algunas decisiones para orientar y simplificar la experiencia:

- Elegí una temática de e-commerce gamer.
- Definí las tres mecánicas principales de mala interfaz.
- Que todo funcionara dentro de un único archivo HTML.
- Decidí que el botón de compra no debía ser imposible de atrapar, sino volverse progresivamente más fácil después de varios intentos.
- Elegí reemplazar el menú tradicional de categorías por un árbol genealógico.
- Decidí que la eliminación de productos debía requerir múltiples confirmaciones antes de completarse.
- Después de revisar la primera versión, decidí eliminar las pestañas **Catálogo** y **Familia Gamer** porque no aportaban demasiado a una página con pocos elementos.
- También decidí ocultar inicialmente la opción **Todo el arsenal** y dejar visible por defecto el árbol de **Familia Gamer**, para que esa mecánica tuviera más protagonismo.

## Qué salió mal y cómo lo corregí

En la primera versión aparecieron algunos elementos de navegación que terminaban siendo innecesarios.

Las pestañas **Catálogo** y **Familia Gamer** agregaban una capa de navegación que no tenía demasiado sentido para la cantidad de contenido disponible. En lugar de ayudar, hacían que la estructura se sintiera más complicada de lo necesario.

Además, el catálogo completo, identificado como **Todo el arsenal**, se mostraba por defecto. Esto hacía que el árbol genealógico perdiera importancia, a pesar de ser una de las mecánicas principales del proyecto.

Para corregirlo:

- Eliminé las pestañas **Catálogo** y **Familia Gamer**.
- Dejé el árbol de **Familia Gamer** visible desde el inicio.
- Convertí **Todo el arsenal** en una opción que el usuario debe seleccionar explícitamente.

De esta manera, la navegación sigue siendo absurda de forma intencional, pero la estructura general de la página tiene más sentido.

## Prompts

Los prompts utilizados durante el proceso de diseño, generación y corrección están documentados en: [prompts](./prompts.md)
