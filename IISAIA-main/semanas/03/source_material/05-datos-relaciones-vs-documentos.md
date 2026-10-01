# Datos: relaciones vs. documentos

Acordate de la to-do list de la clase pasada: vivía en una variable de JavaScript, en memoria del navegador. Refrescabas la página y todo desaparecía. Eso no era un bug: la página nunca tuvo memoria. El servidor es lo que le da memoria a la aplicación, y detrás de cada controller hay una base de datos. La pregunta no es si hace falta una; es *qué forma* tiene esa memoria.

## Por qué hace falta una base de datos

Hay tres razones para no resolver esto con un archivo de texto. La primera es la **persistencia**: los datos tienen que sobrevivir a reinicios, despliegues y sesiones que se cierran. Una base de datos guarda en disco de forma ordenada y se asegura de que lo escrito siga ahí mañana.

La segunda es eficiencia de consulta. Buscar una tarea entre diez ítems se resuelve recorriendo una lista; buscar entre diez millones, no. Las bases de datos tienen índices y planes de ejecución pensados para que filtrar, ordenar y combinar siga siendo barato a escala.

La tercera es la **integridad**. No querés que exista una tarea con `project_id = 99` si ese proyecto no existe, ni que dos escrituras simultáneas dejen los datos en un estado inconsistente. La base de datos es el lugar donde esas reglas se hacen cumplir, no un detalle del código de aplicación.

## Relational: el mundo de tablas

Una **base de datos relational**, también llamada SQL, organiza los datos en **tablas**. Cada tabla tiene **filas** (registros) y **columnas** (campos con un tipo declarado). El conjunto de tablas, columnas y tipos forma el **schema**: la forma fija que los datos están obligados a respetar.

Las tablas se conectan entre sí con **foreign keys** (claves foráneas): una columna de una tabla que apunta a la clave primaria de otra. Para una app de tareas con proyectos, dos tablas alcanzan:

```
projects
  id            int, primary key
  name          text

tasks
  id            int, primary key
  title         text
  due_date      ISO date | null
  project_id    int, foreign key → projects.id
```

`tasks.project_id` no es un número suelto: la base sabe que tiene que existir un `projects.id` con ese valor, y rechaza las inserciones que rompan esa regla. La operación que combina ambas tablas en una sola consulta se llama **JOIN**: trae cada tarea con el nombre del proyecto al que pertenece, en una misma fila de resultado. No vamos a aprender SQL acá; alcanza con saber que esa pieza existe.

## Document: el mundo de objetos anidados

Una **base de datos document**, parte de la familia NoSQL, no piensa en tablas: piensa en **documentos**. Un documento es un objeto parecido a un JSON, con campos anidados y estructura libre. Los documentos se agrupan en **colecciones**, el equivalente más cercano a una tabla, pero sin la obligación de que todos compartan el mismo schema.

El mismo dominio de proyectos y tareas, modelado document, podría verse así:

```
{
  "id": "p1",
  "name": "Tesis",
  "tasks": [
    { "id": "t1", "title": "Marco teórico", "due_date": "2026-06-01" },
    { "id": "t2", "title": "Bibliografía",  "due_date": null }
  ]
}
```

Las tareas viven adentro del proyecto. No hay foreign key, no hay JOIN: para traer un proyecto con todas sus tareas, leés el documento y listo. **MongoDB** es el ejemplo más conocido, y DynamoDB otro habitual.

El trade-off es directo: anidar es cómodo cuando siempre leés "todo de un proyecto" junto. Es pésimo cuando las tareas también necesitan vivir solas, cuando otra entidad las referencia, o cuando querés filtrarlas globalmente sin importar a qué proyecto pertenecen.

## Cómo elegir

La heurística es simple. Relational cuando hay relaciones claras entre entidades y querés integridad: facturación, inventario, gestión de cualquier dominio que se modela con entidades relacionadas. Document cuando el dato es jerárquico, de schema flexible, optimizado para acceso por documento: perfiles con muchos campos opcionales, logs, eventos.

La regla pragmática para este curso: la mayoría de las apps arrancan relational. Ir a document tiene sentido cuando el patrón de datos lo pide.

## SQLite como entry point

En esta clase usamos **SQLite**, no Postgres. La razón es práctica: cero configuración, sin servidor ni red ni usuarios. La base entera vive en un archivo en tu disco y la librería se importa como cualquier otra.

En producción real probablemente uses Postgres, pero las decisiones de modelado, las foreign keys, los tipos de columna y los JOINs son las mismas. SQLite te deja concentrarte en *qué* modelás, no en dónde corre la base.

## Vago vs. específico

```
guardá tareas y proyectos en una base
```

```
modelá dos tablas relational en SQLite:
- projects(id INTEGER PK, name TEXT NOT NULL)
- tasks(id INTEGER PK, title TEXT NOT NULL, due_date TEXT, project_id INTEGER NOT NULL, FOREIGN KEY (project_id) REFERENCES projects(id))
generá las migraciones y un seed con dos proyectos y cinco tareas distribuidas entre ellos.
```

Los dos producen código que arranca; un LLM resuelve cualquiera. La diferencia vive en los tres ejes. Determinismo: el específico fija motor, nombres, tipos y la relación, así que dos generaciones convergen en schemas casi idénticos. Iteración: si mañana querés agregar `description` a tasks, tocás una línea del contrato y regenerás esa pieza. Auditoría: leés la migración generada contra el bloque de arriba y ves de una si las foreign keys están bien declaradas o si la IA improvisó.
