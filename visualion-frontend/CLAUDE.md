Este archivo resume la información esencial para el agente Claude al trabajar con el repositorio Visualion_opt.

Puntos clave:

- Revisa primero [visualion-frontend/AGENTS.md](AGENTS.md) para las reglas de Next.js y notas de proyecto.
- Backend principal: `Backend/` — controla la API FastAPI y la conexión a PostgreSQL.
- Archivos importantes:
	- `Backend/index.py` (arranque de la API)
	- `Backend/controllers/empleado.py` y `Backend/controllers/paciente.py` (endpoints principales)
	- `Backend/database/dbconnections_opt.py` (cadena de conexión y helpers)
	- `alembic/` (migraciones)

Cambios recientes a tener en cuenta:

- Implementación de carga inicial de BD y ajustes en la estructura de carpetas.
- Endpoints básicos para empleados y pacientes añadidos.

Indicaciones operativas para Claude:

- Si vas a proponer cambios en modelos o esquemas, sugiere también la migración Alembic correspondiente.
- Para pruebas locales, asume `http://127.0.0.1:8000` como base de la API y recuerda usar `Backend.index:app` con Uvicorn.

Si necesitas más contexto, abre los archivos listados arriba y las migraciones en `alembic/`.
