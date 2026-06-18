const BaseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';


export async function fetchObtenerEmpleados() {
    try {
        const response = await fetch(`${BaseURL}/empleados`);
        if (!response.ok) {
            throw new Error('Error al obtener los empleados');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al obtener los empleados:', error);
        throw error;
    }

}


export async function fetchObtenerPaciente() {
    try {
        const response = await fetch(`${BaseURL}/pacientes`);
        if (!response.ok) {
            throw new Error('Error al obtener los pacientes');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al obtener los pacientes:', error);
        throw error;
    }
}
export async function crearPaciente(paciente: any) {
    try {
        const response = await fetch(`${BaseURL}/pacientes/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(paciente),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error al crear el paciente');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al crear el paciente:', error);
        throw error;
    }
}

export async function actualizarPaciente(id: number, paciente: any) {
    try {
        const response = await fetch(`${BaseURL}/pacientes/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(paciente),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error al actualizar el paciente');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al actualizar el paciente:', error);
        throw error;
    }
}

export async function eliminarPaciente(dni: string) {
    try {
        const response = await fetch(`${BaseURL}/pacientes/${dni}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error al eliminar el paciente');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al eliminar el paciente:', error);
        throw error;
    }
}

export async function buscarPacientePorDni(dni: string) {
    try {
        const response = await fetch(`${BaseURL}/pacientes/dni/${dni}`);
        if (!response.ok) {
            if (response.status === 404) return null;
            throw new Error('Error al buscar el paciente');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al buscar el paciente:', error);
        throw error;
    }
}

export async function fetchlistarEmpleados() {
    try {
        const response = await fetch(`${BaseURL}/empleados`);
        if (!response.ok) {
            throw new Error('Error al listar los empleados');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al listar los empleados:', error);
        throw error;
    }
}

// Funciones de autenticación y gestión de usuarios
export async function login(usuario: string, contraseña: string) {
    try {
        const response = await fetch(`${BaseURL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario, contraseña }),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Credenciales inválidas');
        }
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        return data;
    } catch (error) {
        console.error('Error en login:', error);
        throw error;
    }
}

export async function register(userData: any) {
    try {
        const response = await fetch(`${BaseURL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error al registrar');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en registro:', error);
        throw error;
    }
}

export async function fetchUsuarios() {
    try {
        const response = await fetch(`${BaseURL}/auth/usuarios`);
        if (!response.ok) throw new Error('Error al listar usuarios');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

export async function obtenerUsuario(id: number) {
    try {
        const response = await fetch(`${BaseURL}/auth/usuarios/${id}`);
        if (!response.ok) throw new Error('Error al obtener usuario');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

export async function actualizarUsuario(id: number, userData: any) {
    try {
        const response = await fetch(`${BaseURL}/auth/usuarios/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error al actualizar usuario');
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

export async function eliminarUsuario(id: number) {
    try {
        const response = await fetch(`${BaseURL}/auth/usuarios/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error al eliminar usuario');
        }
        return { success: true };
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

export function logout() {
    localStorage.removeItem('token');
}