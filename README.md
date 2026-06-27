# Visualion_Opt

Plataforma integral que unifica la atención oftalmológica clínica con la gestión comercial de una óptica. Su objetivo principal es eliminar los errores de transcripción manual, optimizar el inventario y mejorar la experiencia del paciente mediante la trazabilidad total.

Este proyecto fue desarrollado como parte del Trabajo Práctico de la materia Diseño de Sistemas.

## Características Principales

El sistema se divide en los siguientes módulos operativos:

*   **Gestión de Pacientes y Turnos:** Registro de datos personales, gestión de agendas médicas y recordatorios automáticos de citas.
*   **Módulo Clínico (Oftalmología):** Digitalización de la historia clínica, registro de exámenes visuales y emisión de recetas ópticas digitales.
*   **Módulo Comercial (Óptica):** Proceso de venta vinculado a recetas, gestión de pagos, facturación y control de stock en tiempo real.
*   **Módulo de Taller y Laboratorio:** Recepción de órdenes de trabajo automatizadas, seguimiento de estados de producción y trazabilidad del técnico responsable.
*   **Autenticación y Roles:** Sistema de registro y login con roles (Administrador, Médico, Vendedor, Técnico) para un acceso seguro y restringido a las funcionalidades.

## Tecnologías Utilizadas

*   **Backend:**
    *   Python 3.11+
    *   FastAPI
    *   SQLAlchemy 2 (ORM Asíncrono)
    *   Alembic (Migraciones de Base de Datos)
    *   Uvicorn (Servidor ASGI)
*   **Frontend:**
    *   Next.js 16+
    *   React 19
    *   TypeScript
*   **Base de Datos:**
    *   PostgreSQL

## Repositorio en GitHub

Puedes encontrar el código fuente completo en el siguiente repositorio (recuerda reemplazar `tu-usuario/visualion_opt` con tu enlace real):

https://github.com/tu-usuario/visualion_opt

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

*   Node.js (versión 20 o superior)
*   Python (versión 3.11 o superior)
*   PostgreSQL

## Instalación y Ejecución Local

Sigue estos pasos para configurar el proyecto en tu entorno de desarrollo.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/visualion_opt.git
cd visualion_opt
```

### 2. Configuración del Backend

El backend se encuentra en la carpeta `Backend/`.

**a. Crear y activar un entorno virtual:**

```bash
# Desde la raíz del proyecto
python -m venv venv
# En Windows
.\venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

**b. Instalar dependencias de Python:**

```bash
pip install -r requirements.txt
```

**c. Configurar la base de datos:**

1.  Asegúrate de que tu servicio de PostgreSQL esté en ejecución.
2.  Crea una base de datos. Por ejemplo, `visualion_opt`.
3.  La configuración de la conexión se encuentra en `Backend/database/dbconnections_opt.py` y `alembic.ini`. Asegúrate de que las credenciales (usuario, contraseña, host, puerto y nombre de la base de datos) sean correctas en ambos archivos.

**d. Aplicar las migraciones:**

Alembic gestiona el esquema de la base de datos. Para crear todas las tablas, ejecuta:

```bash
# Asegúrate de estar en la raíz del proyecto
alembic upgrade head
```

**e. Ejecutar el servidor del backend:**

```bash
uvicorn Backend.index:app --reload --host 127.0.0.1 --port 8000
```

La API estará disponible en `http://127.0.0.1:8000/docs` para ver la documentación interactiva de Swagger.

### 3. Configuración del Frontend

El frontend se encuentra en la carpeta `visualion-frontend/`.

**a. Navegar al directorio del frontend e instalar dependencias:**

```bash
cd visualion-frontend
npm install
```

**b. Ejecutar el servidor de desarrollo:**

```bash
npm run dev
```

Abre http://localhost:3000 en tu navegador para ver la aplicación.

## Usuarios de Prueba

Para facilitar las pruebas de las funcionalidades de cada rol, puedes crear los siguientes usuarios. La contraseña sugerida para todos es `password123`.

**Nota:** Estos usuarios deben ser creados a través del endpoint de registro (`POST /auth/register`) o desde la interfaz de la aplicación si está disponible.

### Empleados (con acceso al sistema)

| Rol | Usuario | Contraseña | Datos Adicionales (ejemplo para el registro) |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `password123` | `{"rol": "admin", "legajo": "ADM-001"}` |
| **Empleado** | `empleado.user` | `password123` | `{"rol": "empleado", "legajo": "EMP-001"}` |
| **Médico** | `medico.user` | `password123` | `{"rol": "medico", "legajo": "MED-001", "matricula": "MN-12345", "especialidad": "Oftalmología"}` |
| **Vendedor** | `vendedor.user` | `password123` | `{"rol": "vendedor", "legajo": "VEN-001"}` |
| **Técnico** | `tecnico.user` | `password123` | `{"rol": "tecnico", "legajo": "TEC-001", "matricula_optico": "MOT-6789"}` |

#### Ejemplo de Creación con cURL

Puedes usar una herramienta como cURL para crear un usuario. Aquí un ejemplo para el **Médico**:

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "dni": "11222333",
  "nombre": "Doctor",
  "apellido": "House",
  "telefono": "555-0101",
  "email": "medico@visualion.com",
  "usuario": "medico.user",
  "contraseña": "password123",
  "legajo": "MED-001",
  "rol": "medico",
  "matricula": "MN-12345",
  "especialidad": "Oftalmología General"
}'
```

### Pacientes (gestionados en el sistema)

Los pacientes no tienen credenciales de acceso. Su información es gestionada por los empleados a través de los módulos correspondientes (ej. "Gestión de Pacientes"). Puedes crear un paciente nuevo una vez que hayas iniciado sesión con un rol con permisos (como Administrador o Médico).

## Estructura del Proyecto

```
.
├── Backend/              # Lógica del backend (FastAPI)
│   ├── controllers/      # Endpoints de la API (routers)
│   ├── database/         # Conexión a la BD
│   ├── Models/           # Modelos de SQLAlchemy (tablas)
│   ├── Schemas/          # Esquemas de Pydantic (validación de datos)
│   ├── services/         # Lógica de negocio
│   └── index.py          # Punto de entrada de la aplicación FastAPI
├── visualion-frontend/   # Aplicación frontend (Next.js)
│   ├── app/              # Páginas y componentes de React
│   └── ...
├── alembic/              # Scripts de migración de Alembic
├── alembic.ini           # Configuración de Alembic
└── requirements.txt      # Dependencias de Python
```