# Visualion

Proyecto full stack compuesto por un frontend en Next.js y un backend en FastAPI con SQLAlchemy y PostgreSQL.

## Qué se realizó

El repositorio quedó organizado en dos capas principales:

- Frontend base con Next.js 16, React 19 y TypeScript.
- API inicial con FastAPI para exponer el servicio principal.
- Conexión a base de datos PostgreSQL mediante SQLAlchemy asíncrono.
- Estructura preparada para migraciones con Alembic.
- Modelos y esquemas base para empleados, médicos y técnicos.

En el estado actual, la interfaz todavía conserva la plantilla inicial de Next.js y el backend está en una fase de base estructural, listo para seguir agregando CRUDs, validaciones y endpoints de negocio.

## Estructura principal

- `app/`: frontend Next.js.
- `api/`: backend FastAPI, modelos, esquemas, controladores y conexión a base de datos.
- `alembic/` y `alembic.ini`: migraciones de base de datos.
- `public/`: recursos estáticos del frontend.

## Tecnologías usadas

- Next.js 16
- React 19
- TypeScript
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL

## Requisitos previos

- Node.js 20 o superior.
- Python 3.11 o superior.
- PostgreSQL ejecutándose localmente.
- Un entorno virtual de Python para el backend.

## Cómo ejecutar en local

### 1. Frontend

Instala dependencias y levanta el servidor de desarrollo:

```bash
npm install
npm run dev
```

Luego abre http://localhost:3000.

### 2. Backend

Instala las dependencias de Python que figuran en `requirements.txt` y ejecuta la API desde la raíz del proyecto:

```bash
python -m pip install -r requirements.txt
python -m uvicorn api.index:app --reload --host 127.0.0.1 --port 8000
```

Si prefieres iniciar el archivo directamente, `api/index.py` también incluye un arranque con Uvicorn.

### 3. Base de datos

La conexión actual apunta a PostgreSQL en `localhost:5432` con la base `visualion_opt`.

Antes de usar la API, verifica estas credenciales en:

- `api/index.py`
- `api/database/dbconnections_opt.py`
- `alembic.ini`

Si cambias usuario, contraseña, host o nombre de base, actualiza esos tres lugares para que la API y las migraciones apunten al mismo destino.

## Migraciones

Alembic está preparado para administrar la estructura de la base. Cuando agregues o cambies modelos, genera y aplica migraciones desde la raíz del proyecto.

Recomendación general:

```bash
alembic revision --autogenerate -m "descripcion_del_cambio"
alembic upgrade head
```

## Consejos útiles para trabajar el proyecto

- Usa PostgreSQL local antes de intentar desplegar, así puedes validar la conexión y las migraciones sin depender de producción.
- Mantén sincronizada la URL de base de datos entre la API, Alembic y cualquier entorno local.
- Levanta primero la API y después el frontend si vas a probar consumo de datos.
- Si vas a crecer el backend, separa controladores, servicios, esquemas y modelos por dominio para evitar que `api/index.py` concentre demasiada lógica.
- Antes de publicar, prueba al menos la ruta raíz de FastAPI y la carga inicial del frontend.

## Despliegue recomendado

### Frontend

La forma más simple es desplegar el frontend en Vercel o en cualquier hosting compatible con Next.js.

### Backend

Para producción, conviene ejecutar FastAPI detrás de un servidor ASGI como Uvicorn o Gunicorn con Uvicorn workers, y exponerlo mediante un proxy inverso como Nginx.

### Base de datos

PostgreSQL debe estar en un servicio independiente. Si usas Laragon como apoyo local, úsalo para el entorno de desarrollo, pero no como reemplazo de una base de datos gestionada para producción.

## Flujo práctico de despliegue local con Laragon

1. Inicia PostgreSQL y verifica que esté escuchando en el puerto 5432.
2. Ajusta la cadena `DATABASE_URL` con tus credenciales reales.
3. Aplica migraciones con Alembic.
4. Ejecuta la API con Uvicorn.
5. Ejecuta el frontend con `npm run dev`.

## Estado actual del proyecto

- Frontend: base funcional, pendiente de personalización de pantallas y consumo real de API.
- Backend: estructura inicial lista para crecer con endpoints de negocio.
- Base de datos: configurada para PostgreSQL y migraciones.
- Despliegue: orientado a entorno local primero y luego a hosting externo.

## Próximos pasos sugeridos

- Implementar endpoints CRUD para empleados y pacientes.
- Conectar el frontend con la API.
- Normalizar la configuración de variables de entorno.
- Completar las migraciones iniciales de Alembic.
