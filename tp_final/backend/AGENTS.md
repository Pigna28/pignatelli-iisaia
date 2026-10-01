# Backend

Los inputs estrictos están en schemas.py; los SQL parametrizados en routes.py.
Validadores Pydantic deben lanzar ValueError (TypeError no genera validación 400).
Usar BEGIN IMMEDIATE cuando se lee y luego modifica un recurso. Confirmar la
transacción antes de devolver éxito; un fallo de auditoría revierte la operación.
No convertir errores de autenticación en sesiones vacías aceptadas.
