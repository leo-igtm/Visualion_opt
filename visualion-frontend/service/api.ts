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


export async function fetchlistarPacientes() {
    try {
        const response = await fetch(`${BaseURL}/pacientes`);  
        if (!response.ok) {
            throw new Error('Error al listar los pacientes');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al listar los pacientes:', error);
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