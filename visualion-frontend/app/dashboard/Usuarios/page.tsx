'use client';

import { useEffect, useState } from 'react';
import { fetchUsuarios, eliminarUsuario } from '@/service/api';

export default function UsuariosPage() {
    const [usuarios, setUsuarios] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [deleting, setDeleting] = useState<number | null>(null);

    useEffect(() => {
        cargarUsuarios();
    }, []);

    const cargarUsuarios = async () => {
        try {
            setLoading(true);
            const data = await fetchUsuarios();
            setUsuarios(data);
        } catch (error) {
            console.error('Error al cargar usuarios:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleEliminar = async (id: number) => {
        if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
            try {
                setDeleting(id);
                await eliminarUsuario(id);
                cargarUsuarios();
            } catch (error) {
                console.error('Error:', error);
                alert('Error al eliminar usuario');
            } finally {
                setDeleting(null);
            }
        }
    };

    if (loading) {
        return (
            <div className="p-6">
                <p className="text-gray-400">Cargando usuarios...</p>
            </div>
        );
    }

    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold text-gray-100 mb-6">Gestión de Usuarios</h1>

            {usuarios.length === 0 ? (
                <p className="text-gray-400">No hay usuarios registrados</p>
            ) : (
                <div className="overflow-x-auto border border-gray-800 rounded-lg">
                    <table className="w-full">
                        <thead className="bg-gray-900 border-b border-gray-800">
                            <tr>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">DNI</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Nombre</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Usuario</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Email</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Rol</th>
                                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-800">
                            {usuarios.map((usuario) => (
                                <tr key={usuario.id} className="hover:bg-gray-800/50">
                                    <td className="px-6 py-4 text-sm text-gray-300">{usuario.dni}</td>
                                    <td className="px-6 py-4 text-sm text-gray-300">
                                        {usuario.nombre} {usuario.apellido}
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-300">{usuario.usuario}</td>
                                    <td className="px-6 py-4 text-sm text-gray-300">{usuario.email}</td>
                                    <td className="px-6 py-4 text-sm">
                                        <span className="px-3 py-1 bg-indigo-900/30 text-indigo-300 rounded-full text-xs font-medium">
                                            {usuario.rol}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-sm">
                                        <button
                                            onClick={() => handleEliminar(usuario.id)}
                                            disabled={deleting === usuario.id}
                                            className="px-3 py-1 bg-red-900/30 text-red-400 hover:bg-red-900/50 rounded text-sm transition-colors disabled:opacity-50"
                                        >
                                            {deleting === usuario.id ? 'Eliminando...' : 'Eliminar'}
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
