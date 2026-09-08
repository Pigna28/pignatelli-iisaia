# Registro de prompts

## 1. Prompt inicial

```
Dame un prompt para estas 3 opciones en una pagina de catalogo de cosas "gamer". La idea es que sea una pagina de compra, en otro chat voy a pegar el prompt y la idea es empezar a realizar el código html en este nuevo chat

Bopton comprar que se escapa
Categorías por arbol genealogico
Botón de eliminar del carrito con confirmación rusa
```

**Que intentaba lograr**  
Generar un prompt más completo y detallado a partir de tres ideas de interfaz de usuario absurda para una página de e-commerce gamer, con la intención de reutilizarlo en otro chat para comenzar a desarrollar el HTML.

**Que deolvio**  
Un prompt de generación detallado que define una tienda gamer completa en un solo archivo HTML e incorpora las tres mecánicas: botón de compra que se escapa, categorías mediante un árbol genealógico y eliminación del carrito con una cadena exagerada de confirmaciones.

**Que hice con eso**  
Copié el prompt generado y lo utilicé como prompt inicial en un nuevo agente/chat para que desarrollara la página web.

---

## 2. Prompt de generacion (nuevo agente)

```
Quiero que desarrolles una página web completa de e-commerce de productos gamer en un único archivo HTML, incluyendo dentro del mismo archivo todo el código necesario.

La estética debe ser de una tienda gamer moderna: fondo oscuro, acentos neón, tarjetas de productos, imágenes o placeholders de productos, precios, categorías, carrito y navegación.
La página debe verse suficientemente bien pero debe incluir decisiones de interfaz deliberadamente malas y absurdas.

El objetivo no es hacer una página rota técnicamente, sino una interfaz funcional cuyo comportamiento sea intencionalmente frustrante y humorístico.

Implementá estas tres mecánicas principales:

### 1. Botón de compra que se escapa

Cada tarjeta de producto debe tener un botón “Comprar”.

Cuando el usuario acerque el cursor o intente hacer click, el botón debe moverse a otra posición dentro de la tarjeta o de una zona delimitada.

Debe ser posible atraparlo eventualmente.

Comportamiento sugerido:

- En los primeros intentos, el botón se mueve rápidamente.
- Contabilizar la cantidad de intentos fallidos.
- Después de 5 intentos, hacerlo más lento o reducir la distancia del movimiento.
- Después de aproximadamente 8 intentos, permitir finalmente hacer click.
- Al conseguirlo, agregar el producto al carrito.
- Mostrar algún mensaje humorístico como “El carrito más veloz de este lado del Suquia”

No permitir que el botón salga de la pantalla o quede inaccesible.

### 2. Categorías mediante un árbol genealógico absurdo

En vez de utilizar un menú normal de categorías, crear una sección llamada algo como:

“Familia Gamer”

Las categorías deben visualizarse como un árbol genealógico jerárquico.

Ejemplo:

Gaming
├── Hardware
│ ├── PC
│ │ ├── GPU
│ │ ├── CPU
│ │ └── RAM
│ └── Consoles
│ ├── Controllers
│ └── Accessories
├── Peripherals
│ ├── Keyboards
│ ├── Mice
│ └── Headsets
└── Gamer Essentials
├── RGB
├── Chairs
└── Questionable Energy Drinks

Visualmente quiero que parezca un verdadero árbol genealógico:

- tarjetas o nodos conectados mediante líneas;
- hijos y padres;
- ramas expandibles;
- pequeñas etiquetas absurdas como “Pariente”, “Decendiente”, “Primo segundo”.

Para seleccionar una categoría, el usuario debe navegar por el árbol y hacer click en uno de los nodos finales.

Al seleccionar una categoría, filtrar los productos visibles del catálogo.

La navegación debe ser innecesariamente compleja pero entendible.

### 3. Eliminar producto del carrito con confirmación rusa

Cuando el usuario presione “Eliminar” sobre un producto del carrito, NO eliminarlo inmediatamente.

Debe aparecer una sucesión exagerada de confirmaciones.

Ejemplo:

1. “¿Seguro que querés eliminar este producto?”
2. “¿Seguro seguro?”
3. “Este producto ya se había encariñado con vos.”
4. “Pensalo otra vez.”
5. “Última oportunidad.”
6. “¿Estás emocionalmente preparado para esto?”
7. “Bueno. Eliminando…”

El usuario debe avanzar manualmente por cada confirmación.

Podés usar un estilo con botones, pequeñas animaciones y un contador de pasos.

Agregar ocasionalmente botones engañosos como:

- “Sí”
- “Sí, lamentablemente”
- “Volver con mi producto”
- “No puedo hacerle esto”

Pero el proceso debe seguir siendo funcional.

Al completar toda la cadena de confirmaciones, eliminar finalmente el producto del carrito.

### Catálogo

Crear al menos 8 productos gamer ficticios, por ejemplo:

- Mechanical RGB Keyboard
- UltraLight Gaming Mouse
- 360 Hz Monitor
- Noise-Cancelling Gaming Headset
- RGB GPU Support Bracket
- Stream Deck
- Gamer Chair
- “Performance” RGB Mousepad

Cada producto debe tener:

- nombre;
- categoría;
- precio;
- breve descripción;
- imagen o representación visual;
- botón Comprar.

### Carrito

El carrito debe poder:

- mostrar productos agregados;
- mostrar cantidades;
- calcular subtotal;
- eliminar productos mediante la mecánica de confirmación descrita;
- mostrar cantidad total de productos en un indicador.

No es necesario implementar pagos reales.

### Diseño

Quiero una estética visual gamer relativamente sofisticada, no una página deliberadamente fea.

Usar:

- fondo negro/gris muy oscuro;
- paneles oscuros;
- bordes sutiles;
- luces RGB/neón;
- tipografía estilo tecnológica;
- animaciones suaves;
- hover effects;
- sombras;
- buen espaciado;
- diseño responsive.

La mala UX debe venir principalmente de las interacciones absurdas, no de que el sitio visualmente sea malo.

Remarco que Todo debe funcionar abriendo directamente un solo archivo
```

**Que intentaba lograr**  
Obtener una implementación funcional y autocontenida de la tienda gamer, en un único archivo HTML, manteniendo una estética cuidada pero introduciendo deliberadamente interacciones frustrantes y humorísticas.

**Que deolvio**  
Una primera versión de la página web. La implementación incluía elementos de navegación como las pestañas “Catálogo” y “Familia Gamer”, y una sección o vista de “Todo el arsenal” visible por defecto. Bastante bien para ser la primer iteración.

**Que hice con eso**  
Revisé la estructura y detecté que algunas decisiones de navegación no aportaban valor por la cantidad de contenido disponible.

---

## 3. Promp de correccion

```
Las pestañas catalogo y familia gamer quedan sin proposito porque la pagina no tiene tantos elementos. Sacalos
Todo el arsenal se muestra por defecto, ocúltalo, déjalo como algo a seleccionar y deja el árbol de familia gamer visible por default
```

**Que intentaba lograr**  
Simplificar la navegación eliminando pestañas innecesarias y hacer que el árbol de “Familia Gamer” sea el punto de entrada principal de la experiencia, en lugar de mostrar todo el catálogo automáticamente.

**Que deolvio**  
El html final y exasperantemente no funcional.
