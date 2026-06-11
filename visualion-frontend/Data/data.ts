export interface Paciente {
    id: number;
    nombre: string;
    apellido: string;
    dni: string;
    telefono?: string;
    email?: string;       
    obra_social?: string;
    historial_medico?: string;
}

export interface Empleado {
    id: number;
    dni: string;
    nombre: string;
    apellido: string;
    telefono?: string;
    email?: string;
    legajo: string;
    usuario: string;
    rol: string;
    especialidad?: string;
    matricula?: string;
    matricula_optico?: string;
    comisiones?: number;
}

