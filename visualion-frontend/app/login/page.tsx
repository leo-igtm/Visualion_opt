'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { login } from '@/service/api';
import styles from './login.module.css';

export default function LoginPage() {
    const [usuario, setUsuario] = useState('');
    const [contraseña, setContraseña] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await login(usuario, contraseña);
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.message || 'Error al iniciar sesión');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.formBox}>
                <h1>Visualion - Iniciar Sesión</h1>
                <form onSubmit={handleLogin}>
                    <div className={styles.formGroup}>
                        <label htmlFor="usuario">Usuario</label>
                        <input
                            id="usuario"
                            type="text"
                            placeholder="Tu usuario"
                            value={usuario}
                            onChange={(e) => setUsuario(e.target.value)}
                            required
                            disabled={loading}
                        />
                    </div>

                    <div className={styles.formGroup}>
                        <label htmlFor="contraseña">Contraseña</label>
                        <input
                            id="contraseña"
                            type="password"
                            placeholder="Tu contraseña"
                            value={contraseña}
                            onChange={(e) => setContraseña(e.target.value)}
                            required
                            disabled={loading}
                        />
                    </div>

                    {error && <p className={styles.error}>{error}</p>}

                    <button type="submit" disabled={loading} className={styles.button}>
                        {loading ? 'Ingresando...' : 'Ingresar'}
                    </button>
                </form>

                <p className={styles.link}>
                    ¿No tienes cuenta? <a href="/register">Registrarse aquí</a>
                </p>
            </div>
        </div>
    );
}
