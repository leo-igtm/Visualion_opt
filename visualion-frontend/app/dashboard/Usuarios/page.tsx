'use client';

import { useEffect, useState } from 'react';
import { fetchUsuarios, eliminarUsuario } from '@/service/api';
import styles from './usuarios.module.css';

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
            <div className={styles.container}>
                <p className={styles.loading}>Cargando usuarios...</p>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <h1>Gestión de Usuarios</h1>

            {usuarios.length === 0 ? (
                <p className={styles.empty}>No hay usuarios registrados</p>
            ) : (
                <div className={styles.tableWrapper}>
                    <table className={styles.table}>
                        <thead>
                            <tr>
                                <th>DNI</th>
                                <th>Nombre</th>
                                <th>Usuario</th>
                                <th>Email</th>
                                <th>Rol</th>
                                <th>Teléfono</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {usuarios.map((usuario) => (
                                <tr key={usuario.id}>
                                    <td>{usuario.dni}</td>
                                    <td>{usuario.nombre} {usuario.apellido}</td>
                                    <td>{usuario.usuario}</td>
                                    <td>{usuario.email}</td>
                                    <td>
                                        <span className={`${styles.badge} ${styles[`badge-${usuario.rol}`]}`}>
                                            {usuario.rol}
                                        </span>
                                    </td>
                                    <td>{usuario.telefono || '-'}</td>
                                    <td>
                                        <button
                                            className={styles.deleteBtn}
                                            onClick={() => handleEliminar(usuario.id)}
                                            disabled={deleting === usuario.id}
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
