# El estilo: cómo se ve cada sustantivo

Si el HTML son los sustantivos, el CSS responde a la pregunta "¿cómo se ven?". No vamos a aprender CSS entero. Vamos a aprender las cuatro perillas que importa nombrar cuando hablás con una IA.

## Cuatro primitivas suficientes

El **CSS** es enorme: cientos de propiedades, módulos enteros que llenan libros. Para dirigir una IA no necesitás ese inventario. Necesitás cuatro primitivas: la caja, el **layout**, la tipografía y color, y las variables. Con eso alcanzás para describir el 90% de las decisiones visuales del curso. El resto se delega.

## Primitiva 1 — El modelo de caja

Todo elemento HTML es una caja. No "casi todo": todo. Y cada caja tiene cuatro capas concéntricas, como una cebolla. De adentro hacia afuera:

1. **content**: el contenido en sí (texto, imagen).
2. **padding**: el espacio interno entre el contenido y el borde de la caja.
3. **border**: el borde de la caja.
4. **margin**: el espacio externo que separa esta caja de las que la rodean.

Esto es el **modelo de caja** (box model), y es la base de todo el CSS. Importa por una razón muy concreta: la diferencia entre una página que "está apretada" y una que "respira" se decide en padding y margin. Si no tenés esos dos nombres, no podés pedir el cambio. Vas a decir cosas como "dale más aire" y la IA va a tirar al azar.

Con vocabulario, el prompt es exacto:

> *"Agregá 16px de padding interno al `<button>`."*

Una sola línea, cero ambigüedad.

## Primitiva 2 — Layout: flexbox y grid

La pregunta principal del CSS no es de qué color son las cosas. Es *cómo se acomodan las cajas entre sí*: dado un contenedor con tres hijos, ¿van en fila, en columna, en cuadrícula, centrados, con qué separación? En 2026 hay dos respuestas dominantes, y son las dos que tenés que saber nombrar.

### Flexbox: una dimensión

**Flexbox** sirve cuando querés acomodar elementos en una sola dirección: fila o columna. Le decís al contenedor `display: flex` y se vuelve un **flex container**; cada hijo es un **flex item**. Las cuatro perillas que importa conocer:

- `flex-direction`: fila o columna.
- **`justify-content`**: cómo se distribuyen en el eje principal.
- **`align-items`**: cómo se alinean en el eje cruzado.
- **`gap`**: la separación entre items.

Caso típico: una nav-bar, una toolbar, un grupo de botones, una tarjeta con avatar al lado del nombre.

### Grid: dos dimensiones

**Grid** sirve cuando el layout es un tablero: filas y columnas a la vez. Le decís al contenedor `display: grid` y se vuelve un **grid container**. La perilla central es `grid-template-columns`, donde declarás cuántas columnas hay y de qué ancho. El `gap` también funciona acá.

Caso típico: una galería de tarjetas, un dashboard, una landing con bloques en cuadrícula, un panel de productos.

Punto clave: cuando le pedís layout a un LLM, nombrar *flex* o *grid* hace que el código salga bien al primer intento. Si describís "quiero que estén una al lado de la otra", la IA improvisa con `inline-block` o floats antiguos, y vas a iterar tres veces para llegar al resultado que un término técnico te daba directo.

## Primitiva 3 — Tipografía y color

Dos perillas dominan la sensación general de un sitio: la **tipografía** y la paleta. Para tipografía, la decisión cabe en dos opciones: una sola sans-serif para todo, o una pareja heading + body (serif para títulos, sans para texto). La propiedad que la define es **`font-family`**.

Para color, alcanza con una **paleta** minimalista: un fondo, un color de texto, un acento, y opcionalmente un segundo acento de contraste. Cuatro tonos.

Por qué importa: si pedís "que se vea moderno", el LLM inventa lo que se le ocurra y te devuelve una página genérica. Si pedís "tipografía sans, fondo `#0f172a`, texto `#e2e8f0`, acento `#6366f1`", obtenés exactamente eso. La diferencia entre dirigir y rezar.

## Primitiva 4 — Variables CSS: la perilla del LLM

Las **variables CSS** (también llamadas custom properties) se declaran así, generalmente en `:root`:

```css
:root {
  --color-primary: #6366f1;
  --color-bg: #0f172a;
  --space-md: 16px;
}
```

Y se usan así: `background: var(--color-primary)`.

Importan por una razón específica de este curso: una variable es un punto de entrada. Es una etiqueta que el LLM puede modificar más tarde sin tener que reescribir todo el archivo. Cuando pedís *"cambiá el acento a verde"*, si el código usa variables, el cambio es una sola línea. Si no, la IA tiene que buscar veinte ocurrencias de `#6366f1` y reemplazarlas a mano, con riesgo de romper algo.

Lo vas a ver en vivo: la sección §2 Estilo de `demo.html` tiene un theme switcher que cambia toda la paleta tocando exactamente una variable. Ese es el patrón que querés que tu código tenga siempre.

## Cómo le pedís estilo a un LLM

Mirá el contraste entre dos prompts.

Vago:

> *"Hacelo más lindo."*

Específico:

> *"Cambiá el `<main>` a un grid de 3 columnas con gap de 24px. El `<button>` primario: fondo `var(--color-primary)`, padding 12px 20px, border-radius 8px, color de texto blanco."*

El segundo no es más largo en intención, es más *preciso*. Nombra layout (grid, columnas, gap), modelo de caja (padding, border-radius), y variables. La IA no inventa porque no tiene que.

Estilo es donde más se nota la diferencia entre dirigir y dejar improvisar. El próximo archivo trae la tercera capa: el comportamiento.
