import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import status
from httpx import AsyncClient

from Backend.index import app # Corrected import
from Backend.Schemas.empleado import EmpleadoCreate
from Backend.database.dbconnections_opt import get_db # Added import
from Backend.dependencies import get_current_active_admin_user # Added import

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_db_session():
    """Fixture to mock the database session."""
    db_session = AsyncMock()
    db_session.execute.return_value = MagicMock()
    db_session.execute.return_value.scalars.return_value.first.return_value = None
    return db_session


@pytest.fixture
def mock_admin_user():
    """Fixture to mock an admin user dependency."""
    return {"usuario": "admin", "rol": "admin"}


@pytest.fixture
async def authenticated_client(mock_db_session, mock_admin_user):
    """Fixture to create a client that bypasses authentication and database dependencies."""
    
    # Mock get_db
    app.dependency_overrides[get_db] = lambda: mock_db_session
    
    # Mock get_current_active_admin_user
    app.dependency_overrides[get_current_active_admin_user] = lambda: mock_admin_user
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Clean up overrides
    app.dependency_overrides = {}


async def test_create_user_duplicate_username(authenticated_client: AsyncClient, mock_db_session):
    """Test that creating a user with a duplicate username fails."""
    # Arrange: Mock the database to return an existing user
    mock_db_session.execute.return_value.scalars.return_value.first.return_value = {"usuario": "testuser"}
    
    user_data = {
        "dni": "12345678", "nombre": "Test", "apellido": "User",
        "usuario": "testuser", "password": "password", "rol": "paciente"
    }

    # Act
    response = await authenticated_client.post("/users/create", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "El nombre de usuario ya está registrado" in response.json()["detail"]


async def test_create_paciente_success(authenticated_client: AsyncClient):
    """Test successful creation of a patient."""
    # Arrange
    user_data = {
        "dni": "98765432", "nombre": "Nuevo", "apellido": "Paciente",
        "usuario": "newpaciente", "password": "password123",
        "rol": "paciente", "obra_social": "OSDE"
    }

    # Act
    response = await authenticated_client.post("/users/create", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json["usuario"] == "newpaciente"
    assert response_json["obra_social"] == "OSDE"
    assert "password" not in response_json


async def test_create_medico_success(authenticated_client: AsyncClient):
    """Test successful creation of a medico."""
    # Arrange
    user_data = {
        "dni": "11223344", "nombre": "Nuevo", "apellido": "Medico",
        "legajo": "MED-001", "usuario": "newmedico", "password": "password123",
        "rol": "medico", "matricula": "M12345", "especialidad": "Cardiologia"
    }

    # Act
    response = await authenticated_client.post("/users/create", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json["usuario"] == "newmedico"
    assert response_json["rol"] == "medico"
    assert response_json["legajo"] == "MED-001"
    assert "password" not in response_json


async def test_create_employee_missing_legajo(authenticated_client: AsyncClient):
    """Test that creating an employee without a legajo fails."""
    # Arrange
    user_data = {
        "dni": "44332211", "nombre": "Invalido", "apellido": "Empleado",
        "usuario": "invalidemployee", "password": "password123",
        "rol": "vendedor" # legajo is missing
    }

    # Act
    response = await authenticated_client.post("/users/create", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "requiere 'legajo'" in response.json()["detail"]


async def test_create_user_invalid_role(authenticated_client: AsyncClient):
    """Test that creating a user with an invalid role fails."""
    # Arrange
    user_data = {
        "dni": "55667788", "nombre": "Invalid", "apellido": "Role",
        "usuario": "invalidrole", "password": "password123",
        "rol": "superadmin" # Invalid role
    }
    # Act
    response = await authenticated_client.post("/users/create", json=user_data)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Rol no válido" in response.json()["detail"]
