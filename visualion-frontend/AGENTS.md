<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

-- Proyecto: Visualion_opt — notas para agentes --

- Ubicación del frontend: `visualion-frontend/` (Next.js 16, TypeScript).
- Ubicación del backend: `Backend/` (FastAPI, SQLAlchemy, alembic).
- Endpoints principales implementados (revisar controladores): `Backend/controllers/empleado.py`, `Backend/controllers/paciente.py`.
- Conexión a base de datos: `Backend/database/dbconnections_opt.py`.
- Migraciones: `alembic/` y `alembic.ini`.

Instrucciones para agentes que generan o modifican código:

- Antes de cambiar modelos, sincroniza `alembic/` y crea una migración con `alembic revision --autogenerate`.
- Las llamadas de prueba a la API deben ejecutarse contra `http://127.0.0.1:8000` (uvicorn `Backend.index:app`).
- Mantener coherencia en rutas y nombres: el backend vivo está en `Backend/` (no en `api/`).

Resumen de cambios recientes:

- Carga de base de datos inicial implementada y ajustes en la estructura de carpetas.
- Controladores `empleado` y `paciente` añadidos/actualizados.

Si hay dudas sobre rutas o archivos, consultar primero estos ficheros antes de proponer cambios: `Backend/index.py`, `Backend/controllers/`, `Backend/database/`.
