# Visualion_Opt - Sistema de Gestión para Ópticas

Este es el proyecto final para la materia Diseño de Sistemas. Visualion_Opt es una plataforma integral que unifica la atención oftalmológica clínica con la gestión comercial de una óptica.

## Tecnologías Utilizadas

*   **Frontend**: Next.js, React, TypeScript
*   **Backend**: FastAPI (Python), SQLAlchemy
*   **Base de Datos**: PostgreSQL

---

## Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu sistema:

*   [Node.js](https://nodejs.org/) (versión 20 o superior)
*   [Python](https://www.python.org/) (versión 3.11 o superior)
*   [PostgreSQL](https://www.postgresql.org/download/) (un servidor local o remoto)

---

## ⚙️ Guía de Instalación

Sigue estos pasos en orden para configurar y ejecutar el proyecto.

### 1. Configuración de la Base de Datos

Primero, necesitas restaurar la base de datos usando el archivo `visualion_opt.sql` incluido.

1.  Abre una terminal y crea una nueva base de datos en PostgreSQL:
    ```sql
    CREATE DATABASE visualion_opt;
    ```

2.  Restaura los datos desde el archivo `.sql` con el siguiente comando. Reemplaza `<tu_usuario>` con tu usuario de PostgreSQL.
    ```bash
    pg_restore -U <tu_usuario> -d visualion_opt -v "visualion_opt.sql"
    ```
    Se te pedirá la contraseña de tu usuario de PostgreSQL.

### 2. Configuración del Backend

El backend es una API construida con FastAPI.

1.  Navega a la carpeta del backend:
    ```bash
    cd Backend
    ```

2.  Crea y activa un entorno virtual para Python:
    ```bash
    # Crear entorno virtual
    python -m venv venv

    # Activar en Windows
    .\venv\Scripts\activate

    # Activar en macOS/Linux
    source venv/bin/activate
    ```

3.  Instala las dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Importante**: Configura las credenciales de la base de datos en el archivo `Backend/database/dbconnections_opt.py` para que coincidan con tu configuración local de PostgreSQL.

5.  Inicia el servidor del backend:
    ```bash
    uvicorn index:app --reload --host 127.0.0.1 --port 8000
    ```
    La API estará disponible en `http://127.0.0.1:8000`. Puedes ver la documentación interactiva en `http://127.0.0.1:8000/docs`.

### 3. Configuración del Frontend

El frontend está construido con Next.js.

1.  Abre una **nueva terminal** y navega a la carpeta del frontend:
    ```bash
    cd visualion-frontend
    ```

2.  Instala las dependencias de Node.js:
    ```bash
    npm install
    ```

3.  Inicia el servidor de desarrollo del frontend:
    ```bash
    npm run dev
    ```
    La aplicación web estará disponible en `http://localhost:3000`.

---

## ✅ ¡Listo!

Con el backend y el frontend en ejecución, ya puedes interactuar con la aplicación desde tu navegador.