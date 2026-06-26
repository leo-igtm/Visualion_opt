from fastapi import Depends, HTTPException, status
from Backend.Core.auth import get_current_user
from Backend.Models.Usuarios import Empleado


def get_current_active_user(current_user: Empleado = Depends(get_current_user)) -> Empleado:
    """
    Dependencia para obtener el usuario activo actual.
    En el futuro, podrías añadir una comprobación de `is_active` aquí.
    """
    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin_user(current_user: Empleado = Depends(get_current_active_user)) -> Empleado:
    """
    Dependencia que verifica si el usuario actual es un administrador.
    """
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

# Puedes crear dependencias similares para otros roles
# def get_current_active_medico_user(...)
# def get_current_active_vendedor_user(...)


# Ejemplo de cómo usarlo en un router:
# router = APIRouter(dependencies=[Depends(get_current_active_medico_user)])