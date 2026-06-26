import httpx
import asyncio
from typing import Any

# Base URL of the API
BASE_URL = "http://127.0.0.1:8000"

# User data for each role
# Note: Passwords must be strong enough to pass validation
# (e.g., min 8 chars, 1 uppercase, 1 digit)
users_to_create: list[dict[str, Any]] = [
    {
        "dni": "11111111",
        "nombre": "Maria",
        "apellido": "Gonzalez",
        "telefono": "1122334455",
        "email": "maria.medico@example.com",
        "usuario": "mariamedico",
        "password": "PasswordMedico1",
        "rol": "medico",
        "legajo": "MED-001",
        "matricula": "MN-11111",
        "especialidad": "Oftalmología General"
    },
    {
        "dni": "22222222",
        "nombre": "Carlos",
        "apellido": "Lopez",
        "telefono": "1133445566",
        "email": "carlos.tecnico@example.com",
        "usuario": "carlostecnico",
        "password": "PasswordTecnico1",
        "rol": "tecnico",
        "legajo": "TEC-001",
        "matricula_optico": "OT-22222"
    },
    {
        "dni": "33333333",
        "nombre": "Ana",
        "apellido": "Martinez",
        "telefono": "1144556677",
        "email": "ana.vendedor@example.com",
        "usuario": "anavendedor",
        "password": "PasswordVendedor1",
        "rol": "vendedor",
        "legajo": "VEN-001",
        "comisiones": 5.0
    },
    {
        "dni": "44444444",
        "nombre": "Juan",
        "apellido": "Rodriguez",
        "telefono": "1155667788",
        "email": "juan.empleado@example.com",
        "usuario": "juanempleado",
        "password": "PasswordEmpleado1",
        "rol": "empleado",
        "legajo": "EMP-001"
    },
    {
        "dni": "99999999",
        "nombre": "Juan",
        "apellido": "Paciente",
        "telefono": "1122334455",
        "email": "juan.paciente@example.com",
        "usuario": "juanpaciente",
        "password": "PasswordPaciente1",
        "rol": "paciente",
        "legajo": "ignored",
        "obra_social": "OSDE",
        "historial_medico": "Sin antecedentes."
    }
]

async def register_user(client: httpx.AsyncClient, user_data: dict[str, Any]):
    """Sends a POST request to register a new user."""
    print(f"--- Creando usuario: {user_data['usuario']} (Rol: {user_data['rol']}) ---")
    try:
        response: httpx.Response = await client.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)

        if 200 <= response.status_code < 300:
            print(f"✅ ¡Éxito! Usuario '{user_data['usuario']}' creado.")
            print("Respuesta:", response.json())
        else:
            print(f"❌ Error {response.status_code}: No se pudo crear el usuario '{user_data['usuario']}'.")
            try:
                print("Detalle del error:", response.json())
            except Exception:
                print("Respuesta (no es JSON):", response.text)

    except httpx.ConnectError as e:
        print(f"❌ Error de conexión: No se pudo conectar a {BASE_URL}.")
        print("Asegúrate de que el servidor de backend se esté ejecutando.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
    print("-" * 50)


async def main():
    """Main function to register all users."""
    async with httpx.AsyncClient() as client:
        for user in users_to_create:
            await register_user(client, user)

if __name__ == "__main__":
    print("Iniciando la creación de usuarios de prueba...")
    asyncio.run(main())
    print("Proceso de creación de usuarios finalizado.")
