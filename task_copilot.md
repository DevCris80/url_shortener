# Plan: URL Shortener - Roadmap Integral

## TL;DR
El proyecto tiene la funcionalidad core de URL shortening funcionando, pero le faltan:
1. **Autenticación & Gestión de Usuarios** (tu prioridad)
2. **Validación y Manejo de Errores**
3. **Testing y Logging**
4. **Features Avanzadas** (Analytics, Admin, etc.)

Con timeline largo, se implementarán en 4 fases independientes e iterativas.

---

## FASE 1: Autenticación y Gestión de Usuarios (Prioridad)
**Objetivo:** Usuarios puedan registrarse, loguearse y gestionar sus URLs.

### Pasos
1. Implementar hashing de contraseñas → usar `bcrypt` o `passlib`:
   - Instalar `python-jose[cryptography]` y `passlib[bcrypt]`
   - Crear función `hash_password()` y `verify_password()` en `service/`
   - Aplicar a modelo User

2. Implementar autenticación JWT:
   - Crear `create_access_token()` en `service/`
   - Establecer JWT_SECRET y JWT_ALGORITHM en `core/config.py`
   - Implementar `get_current_user()` en `routes/deps.py` (actualmente stub)

3. Implementar endpoints de usuario:
   - `POST /user/register` - crear usuario (username, email, password)
   - `POST /user/login` - retornar JWT token
   - `GET /user/me` - reemplazar "Hello World" con datos del usuario actual
   - `PUT /user/me` - actualizar perfil (email, password)
   - `DELETE /user/me` - eliminar cuenta y sus URLs

4. Asociar URLs a usuarios autenticados:
   - Modificar `POST /shortener` para capturar `user_id` del token JWT
   - Agregar filtrado en `GET /urls` para retornar solo URLs del usuario actual (o todas si admin)
   - Validar que solo el propietario pueda crear/eliminar URLs

---

## FASE 2: Validación, Errores y Logging
**Objetivo:** Código robusto, manejo de errores claro, trazabilidad.

### Pasos
1. Mejorar validación de inputs:
   - Agregar validadores Pydantic en schemas (URL válida, email válido, contraseña fuerte)
   - Validar longitud de `long_url` (máximo 2048 chars)
   - Validar uniqueness de username/email en tiempo real

2. Implementar manejo consistente de errores:
   - Crear `HTTPException` custom para errores comunes (401, 403, 404, 422)
   - Agregar exception handlers globales en `main.py`
   - Retornar mensajes de error claros en formato JSON

3. Agregar logging estructurado:
   - Configurar logging en `core/` (file + console)
   - Loguear autenticación, creación de URLs, errores
   - Opcional: usar `structlog` para logs JSON

4. Documentación de API:
   - Agregar docstrings a endpoints (FastAPI genera docs automáticamente)
   - Asegurarse que `/docs` y `/redoc` muestren toda la API

---

## FASE 3: Testing y Calidad
**Objetivo:** Confianza en el código, prevenir regresos.

### Pasos
1. Migrar a pytest (reemplazar test_api.py):
   - Instalar `pytest`, `pytest-asyncio`
   - Crear `tests/` folder con estructura: `test_auth.py`, `test_urls.py`, `test_users.py`
   - Tests para: registro, login, creación de URL, redirect, validación

2. Fixtures y test database:
   - Crear fixture de AsyncSession con DB en memoria
   - Fixture para usuario autenticado (con token)
   - Fixture para URLs precargadas

3. Coverage y CI:
   - Instalar `pytest-cov`
   - Target: 80%+ coverage en `service/` y `routes/`
   - Opcional: GitHub Actions workflow para correr tests en cada push

4. Linting y formato:
   - Instalar `black`, `ruff`, `mypy`
   - Pre-commit hooks para garantizar formato

---

## FASE 4: Features Avanzadas (Opcional)
**Objetivo:** Diferenciar el proyecto, agregar valor.

### Opción A: Analytics & Insights
1. Dashboard de estadísticas (GET `/urls/{id}/stats`):
   - Clicks por día, ubicación geográfica (opcional: GeoIP)
   - Top URLs, tasa de conversión (si hay conversion tracking)

2. Exportar datos (GET `/export`):
   - CSV con todas las URLs del usuario

### Opción B: Dominios Custom
1. Permitir usuarios crear URLs con dominio custom:
   - `https://myshortdomain.com/abc123` en lugar de `domain.com/abc123`
   - Agregar tabla `CustomDomain` con FK a User

### Opción C: Admin & Moderación
1. Crear panel admin:
   - `GET /admin/users` - listar usuarios, estadísticas
   - `DELETE /admin/urls/{id}` - eliminar URLs reportadas
   - Role-based access (user vs admin)

### Opción D: Integración Social
1. Compartir estadísticas en redes:
   - Botones de compartir en dashboard
   - Integración con Discord/Slack webhooks (opcional)

---

## Archivos Críticos a Modificar

### Core
- `core/config.py` — Agregar JWT_SECRET, JWT_ALGORITHM, password config
- `core/exceptions.py` — CREAR para excepciones custom

### Routes (Implementación Principal)
- `routes/user.py` — Reemplazar almost entirely: register, login, me, update, delete
- `routes/shortener.py` — Agregar `user_id` a creación, filtrar por usuario

### Services (Lógica de Negocio)
- `service/auth.py` — CREAR: hash_password, verify_password, create_token, decode_token
- `service/shorten.py` — Ya están los métodos principales, pero asegurar que use user_id

### Database (Schema)
- `db/model_url.py` — Ya tiene estructura, pero asegurar relación con User

### Tests
- `tests/test_auth.py` — CREAR
- `tests/test_urls.py` — CREAR
- `tests/test_users.py` — CREAR
- `tests/conftest.py` — CREAR (fixtures)

---

## Verificación

### Después de FASE 1 (Auth):
- [ ] Usuario puede registrarse y recibe JWT
- [ ] Usuario puede loguearse con email/password
- [ ] GET `/user/me` retorna datos correctos
- [ ] POST `/shortener` requiere autenticación
- [ ] GET `/urls` muestra solo URLs del usuario autenticado
- [ ] Token inválido retorna 401

### Después de FASE 2 (Validación):
- [ ] Email inválido rechazado en registro
- [ ] Contraseña débil rechazado (reqs ajustables)
- [ ] URL > 2048 chars rechazada
- [ ] Todos los errores retornan formato JSON consistente
- [ ] Logs aparecen en consola/archivo

### Después de FASE 3 (Tests):
- [ ] `pytest` de todos los tests:
  - `test_auth.py`: 5+ tests
  - `test_urls.py`: 5+ tests
  - `test_users.py`: 3+ tests
- [ ] Coverage >= 80%
- [ ] `black --check`, `ruff check` pasan

### Después de FASE 4 (Features):
- [ ] Elegir al menos 1 opción y validar su feature específico

---

## Decisiones & Scope

- **Autenticación:** JWT (simple, standard) vs. OAuth (más complejo, mejor UX)
  → Recomendación: JWT por ahora, OAuth después si lo necesitas

- **Base de datos:** Mantener SQLite (desarrollo fácil) con opción de migrar a PostgreSQL
  → En `db/session.py` cambiar `sqlite+aiosqlite` a `postgresql+asyncpg`

- **Contraseñas:** Mínimo 8 chars, 1 mayúscula, 1 número, 1 especial (ajustable)

- **Email validation:** Implementar simple regex o usar `email-validator` package

- **CORS:** Agregar en `main.py` si planeas frontend web separado

- **Rate limiting:** Opcional ahora, recomendado antes de producción

---

## Next Steps

1. Revisa este plan
2. Confirma si FASE 1 es tu próximo paso
3. Cuando estés listo, te guío paso a paso con código específico
4. Cada fase toma ~2-4 semanas si trabajas 5-10 horas/semana