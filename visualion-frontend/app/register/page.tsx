'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { register } from '@/service/api';
import styles from './register.module.css';

export default function RegisterPage() {
    const [formData, setFormData] = useState({
        nombre: '',
        apellido: '',
        dni: '',
        email: '',
        usuario: '',
        contraseña: '',
        rol: 'tecnico',
        legajo: '',
        telefono: '',
        especialidad: '',
        matricula: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (formData.contraseña.length < 8) {
            setError('Contraseña debe tener mín 8 caracteres');
            return;
        }

        if (!/[A-Z]/.test(formData.contraseña)) {
            setError('Contraseña debe incluir mayúsculas');
            return;
        }

        if (!/\d/.test(formData.contraseña)) {
            setError('Contraseña debe incluir dígitos');
            return;
        }

        setLoading(true);
        try {
            await register(formData);
            router.push('/login?registered=true');
        } catch (err: any) {
            setError(err.message || 'Error al registrar');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    return (
        <div className={styles.container}>
            <div className={styles.formBox}>
                <h1>Visualion - Registrarse</h1>
                <form onSubmit={handleRegister}>
                    <div className={styles.row}>
                        <div className={styles.formGroup}>
                            <label htmlFor="nombre">Nombre *</label>
                            <input
                                id="nombre"
                                type="text"
                                name="nombre"
                                value={formData.nombre}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                        </div>
                        <div className={styles.formGroup}>
                            <label htmlFor="apellido">Apellido *</label>
                            <input
                                id="apellido"
                                type="text"
                                name="apellido"
                                value={formData.apellido}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                        </div>
                    </div>

                    <div className={styles.row}>
                        <div className={styles.formGroup}>
                            <label htmlFor="dni">DNI *</label>
                            <input
                                id="dni"
                                type="text"
                                name="dni"
                                value={formData.dni}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                        </div>
                        <div className={styles.formGroup}>
                            <label htmlFor="email">Email *</label>
                            <input
                                id="email"
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                        </div>
                    </div>

                    <div className={styles.row}>
                        <div className={styles.formGroup}>
                            <label htmlFor="usuario">Usuario *</label>
                            <input
                                id="usuario"
                                type="text"
                                name="usuario"
                                value={formData.usuario}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                        </div>
                        <div className={styles.formGroup}>
                            <label htmlFor="contraseña">Contraseña *</label>
                            <input
                                id="contraseña"
                                type="password"
                                name="contraseña"
                                value={formData.contraseña}
                                onChange={handleChange}
                                placeholder="Min 8 caracteres, mayúscula y dígito"
                                required
                                disabled={loading}
                            />
                        </div>
                    </div>

                    <div className={styles.row}>
                        <div className={styles.formGroup}>
                            <label htmlFor="legajo">Legajo *</label>
                            <input
                                id="legajo"
                                type="text"
                                name="legajo"
                                value={formData.legajo}
                                onChange={handleChange}
                                required
                                disabled={loading}
                            />
                        </div>
                        <div className={styles.formGroup}>
                            <label htmlFor="rol">Rol *</label>
                            <select name="rol" value={formData.rol} onChange={handleChange} disabled={loading}>
                                <option value="tecnico">Técnico</option>
                                <option value="medico">Médico</option>
                                <option value="vendedor">Vendedor</option>
                            </select>
                        </div>
                    </div>

                    <div className={styles.row}>
                        <div className={styles.formGroup}>
                            <label htmlFor="telefono">Teléfono</label>
                            <input
                                id="telefono"
                                type="tel"
                                name="telefono"
                                value={formData.telefono}
                                onChange={handleChange}
                                disabled={loading}
                            />
                        </div>
                        {formData.rol === 'medico' && (
                            <div className={styles.formGroup}>
                                <label htmlFor="especialidad">Especialidad</label>
                                <input
                                    id="especialidad"
                                    type="text"
                                    name="especialidad"
                                    value={formData.especialidad}
                                    onChange={handleChange}
                                    disabled={loading}
                                />
                            </div>
                        )}
                    </div>

                    {error && <p className={styles.error}>{error}</p>}

                    <button type="submit" disabled={loading} className={styles.button}>
                        {loading ? 'Registrando...' : 'Registrarse'}
                    </button>
                </form>

                <p className={styles.link}>
                    ¿Ya tienes cuenta? <a href="/login">Inicia sesión aquí</a>
                </p>
            </div>
        </div>
    );
}
