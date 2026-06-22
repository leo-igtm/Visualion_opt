'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/service/authService';

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
            const response = await authService.login(usuario, contraseña);
            authService.guardarToken(response.access_token);
            router.push('/dashboard');
        } catch (err: any) {
            setError(err.message || 'Error al iniciar sesión');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center px-4">
            <div className="w-full max-w-md">
                <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-2xl">
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-blue-400 mb-2">
                            Visualion
                        </h1>
                        <p className="text-gray-400">Iniciar Sesión</p>
                    </div>

                    <form onSubmit={handleLogin} className="space-y-4">
                        <div>
                            <label htmlFor="usuario" className="block text-sm font-medium text-gray-300 mb-2">
                                Usuario
                            </label>
                            <input
                                id="usuario"
                                type="text"
                                placeholder="Tu usuario"
                                value={usuario}
                                onChange={(e) => setUsuario(e.target.value)}
                                required
                                disabled={loading}
                                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 transition-colors disabled:opacity-50"
                            />
                        </div>

                        <div>
                            <label htmlFor="contraseña" className="block text-sm font-medium text-gray-300 mb-2">
                                Contraseña
                            </label>
                            <input
                                id="contraseña"
                                type="password"
                                placeholder="Tu contraseña"
                                value={contraseña}
                                onChange={(e) => setContraseña(e.target.value)}
                                required
                                disabled={loading}
                                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 transition-colors disabled:opacity-50"
                            />
                        </div>

                        {error && (
                            <div className="p-4 bg-red-900/20 border border-red-700 rounded-lg">
                                <p className="text-red-400 text-sm">{error}</p>
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white font-bold py-3 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-6"
                        >
                            {loading ? 'Ingresando...' : 'Ingresar'}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <p className="text-gray-400 text-sm">
                            ¿No tienes cuenta?{' '}
                            <a href="/register" className="text-indigo-400 hover:text-indigo-300 font-medium transition-colors">
                                Registrarse aquí
                            </a>
                        </p>
                    </div>

                    <div className="mt-8 pt-6 border-t border-gray-800">
                        <p className="text-gray-500 text-xs text-center">
                            © {new Date().getFullYear()} Visualion. Todos los derechos reservados.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
