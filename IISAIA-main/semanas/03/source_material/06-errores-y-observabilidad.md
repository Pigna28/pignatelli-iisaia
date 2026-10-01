# Errores y observabilidad

La IA generó un endpoint, lo pegaste al navegador y la respuesta es "500 Internal Server Error". Frente a esa pantalla hay dos reacciones posibles. Una es copiar "no funciona" en el chat y rezar. La otra es abrir la terminal donde corre el servidor, encontrar la línea que falló y mandarle *eso* a la IA junto con el código del handler.

Las dos tardan parecido. La diferencia entre la que funciona y la que no es vocabulario: saber qué mirar y qué pedazo de evidencia pegar.

## Los errores tienen dueño

El código de error te dice de qué lado está el problema. Los códigos **4xx** significan "vos, cliente, te equivocaste": pediste un recurso que no existe (404), mandaste un body inválido (400 o 422), o no estás autorizado (401, 403, diferidos a semana 7). Los **5xx** significan "yo, servidor, me caí": el código tiene un bug, la base de datos no responde, la IA olvidó manejar un caso.

El movimiento diagnóstico es leer el primer dígito antes de tocar nada. Si es 4, mirá el request que mandaste. Si es 5, mirá el código del servidor. Empezar por el lado equivocado es la forma más rápida de perder media hora.

## Logs: lo que el servidor te susurra

Un **log** es una línea que el servidor escribe cada vez que algo pasa: cada request que entra, cada error, cada respuesta. En local los logs viven en la terminal donde corre el servidor; en producción se mandan a un sistema de agregación que los junta de muchas máquinas. Cuando algo falla, el log tiene la verdad: qué entró, qué pasó adentro, qué se rompió.

Una sesión de logs típica para un request fallido se ve así:

```
2026-05-07 14:32:11  INFO   POST /projects/4/tasks  body={"title":"Bibliografía"}
2026-05-07 14:32:11  ERROR  IntegrityError: NOT NULL constraint failed: tasks.project_id
2026-05-07 14:32:11  INFO   500 Internal Server Error  duration=12ms
```

Tres líneas, tres cosas distintas. La primera dice qué request entró: method, path, body. La segunda, qué se rompió y por qué: una columna `project_id` que llegó vacía cuando la base la exige. La tercera, con qué código respondió el servidor y cuánto tardó. Las tres juntas son el relato completo del incidente.

## El stack trace: el camino al bug

Cuando el servidor revienta suele aparecer un **stack trace**: la cadena de llamadas a funciones que llevó al error, desde la más externa hasta la más interna. No se lee linealmente de arriba a abajo. La línea que importa suele ser la primera que menciona código tuyo, no del framework.

```
Traceback (most recent call last):
  File "uvicorn/server.py", line 245, in handle
  File "fastapi/routing.py", line 218, in app
  File "app/routes/tasks.py", line 14, in create_task
    db.execute("INSERT INTO tasks (title) VALUES (?)", (body.title,))
  File "sqlite3.py", line 312, in execute
sqlite3.IntegrityError: NOT NULL constraint failed: tasks.project_id
```

Las dos primeras líneas son framework: ahí no vas a encontrar nada que arreglar. La que importa es `app/routes/tasks.py:14`, porque ahí se ve que el `INSERT` no incluye `project_id`. La última línea es el síntoma; la cuarta es la causa. El patrón se repite siempre: el síntoma grita al final, la causa vive en la primera línea de código que escribiste vos (o que la IA escribió por vos).

## Cómo le contás esto a la IA

Con el código de error, la línea de log relevante y la línea del stack trace que apunta a tu archivo, ya tenés todo lo que necesitás para pedir ayuda bien. El prompt malo se ve así:

```
no funciona, dame fix
```

El prompt bueno se ve así:

```
POST /projects/4/tasks devuelve 500.
Log relevante:
  IntegrityError: NOT NULL constraint failed: tasks.project_id
  en app/routes/tasks.py:14
Handler actual:
  [pegás acá el código]
¿Por qué falla y cómo se arregla sin romper la creación de tareas en otros proyectos?
```

La diferencia no es de cortesía. Le estás pasando a la IA la misma evidencia que necesitaría una persona: method, path, código devuelto, línea exacta del error, archivo y handler. Sin esa evidencia el modelo adivina; con ella, razona.

## Observabilidad: la palabra paraguas

**Observabilidad** es el conjunto de prácticas que hacen que un sistema te cuente qué está haciendo: logs, métricas y traces son las tres patas comunes. En esta clase nos quedamos con logs porque es lo que vas a ver en tu terminal cuando corras el servidor con Claude Code, pero el concepto es más amplio y vas a cruzarte con él apenas pongas una app en producción.

## Vago vs. específico

```
este endpoint no anda, arreglalo
```

```
el endpoint POST /tasks devuelve 500. El log adjunto muestra:
  IntegrityError: NOT NULL constraint failed: tasks.project_id
mando body { "title": "X" }. ¿Es un bug del schema (falta default), de la validación (debería rechazar el body) o falta una columna? Quiero entender la causa antes del parche.
```

Los dos pueden producir un parche que arranca; un LLM resuelve cualquiera. La diferencia vive en los tres ejes de siempre. Determinismo: el específico fija path, código, mensaje de error y body, así que dos generaciones convergen en diagnósticos parecidos en lugar de inventar tres bugs distintos. Iteración: si el primer diagnóstico no convence, pedís descartar una de las tres hipótesis sin reescribir el contexto. Auditoría: leés la respuesta contra la evidencia pegada y verificás si la causa propuesta explica realmente el log o ignora la línea que importa.
