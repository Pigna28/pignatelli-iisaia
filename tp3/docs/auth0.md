# Configurar Auth0

## Preparación del tenant

Siguiendo la arquitectura del TP de referencia, crear una aplicación **Regular
Web Application**. Obtener dominio del tenant, Client ID y Client Secret.
Activar la conexión social Google (`google-oauth2`) para esa aplicación.

Registrar estas URLs exactas para desarrollo:

- Allowed Callback URLs: `http://127.0.0.1:8000/callback`
- Allowed Logout URLs: `http://127.0.0.1:8000/logged-out`

Si cambia el puerto, actualizar ambas URLs y `BASE_URL`. No intercambiar
`localhost` con `127.0.0.1`: son orígenes diferentes. En producción usar el dominio
HTTPS público. No es necesario configurar un frontend SPA ni guardar tokens en
localStorage, porque el código OAuth se procesa en el servidor.

## Archivo local

```powershell
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copiar el valor generado en `SESSION_SECRET`. No enviar ese secreto al repositorio.

```dotenv
AUTH_MODE=auth0
APP_ENV=development
BASE_URL=http://127.0.0.1:8000
DATABASE_PATH=data/lab.db
SESSION_SECRET=valor-aleatorio-largo-generado-localmente
AUTH0_DOMAIN=tu-tenant.auth0.com
AUTH0_CLIENT_ID=tu-client-id
AUTH0_CLIENT_SECRET=tu-client-secret
WRITE_SUBJECTS=google-oauth2|identificador-del-operador
```

`AUTH0_DOMAIN` es solo el hostname. `WRITE_SUBJECTS` contiene los identificadores
`sub` exactos, separados por coma, no emails ni nombres. Se pueden obtener en el
dashboard de usuarios de Auth0 o en `/session` después de iniciar sesión.
Si queda vacío, todas las cuentas tienen lectura. No existe autoasignación de
operador al primer usuario. Reiniciar el servidor al modificar `.env`.

## Flujo y controles

- `/login` delega en Authlib la redirección y el estado OAuth.
- `/callback` intercambia el código y usa la identidad validada por Authlib/OIDC.
  Un error, ausencia de identidad o firma inválida rechaza el login.
- Cookie `lab_session`: firmada, HttpOnly, SameSite=Lax, máximo 8 horas; Secure
  cuando `BASE_URL` usa HTTPS. No contiene access_token ni client_secret.
- POST/DELETE requieren token CSRF ligado a la sesión, y las escrituras del
  laboratorio requieren el subject autorizado.
- `/logout` se invoca con POST y CSRF. Borra la cookie y entrega al navegador
  la URL de logout Auth0. `/logged-out` es público para evitar reingreso automático.

Una cookie firmada no constituye una sesión revocable en servidor. Una copia
robada podría seguir válida hasta vencer; rotar SESSION_SECRET invalida todas.
Para revocación individual implementar sesiones almacenadas en servidor.
Los permisos sí se evalúan contra la configuración del proceso en cada request.

## Verificación manual del tenant (pendiente)

1. Abrir `/` sin sesión: debe llevar a Auth0 y Google.
2. Ingresar como lector: listar chips; POST y auditoría deben responder 403.
3. Configurar un operador y reiniciar; verificar alta y baja con esa cuenta.
4. Cancelar login: no debe crearse sesión autenticada.
5. Salir: debe terminar en `/logged-out`, sin login automático.
6. En HTTPS verificar cookie Secure, callback exacto y redirección de salida.

Los tests automatizados simulan el cliente OAuth en su frontera. Prueban cómo
responde la aplicación a éxito/fallo, pero no sustituyen este recorrido real por
Auth0/Google ni una auditoría independiente del proveedor de identidad.
