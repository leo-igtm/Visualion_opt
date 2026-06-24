'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/service/authService';

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
            await authService.register(formData);
            router.push('/login?registered=true');
        } catch (err: unknown) {
            setError((err as Error).message || 'Error al registrar');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 flex items-center justify-center px-4 py-8">
            <div className="w-full max-w-lg">
                <div className="bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-2xl">
                    <div className="text-center mb-8">
                        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-blue-400 mb-2">
                            Visualion
                        </h1>
                        <p className="text-gray-400">Crear Cuenta</p>
                    </div>

                    <form onSubmit={handleRegister} className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="nombre" className="block text-sm font-medium text-gray-300 mb-1">
                                    Nombre *
                                </label>
                                <input
                                    id="nombre"
                                    type="text"
                                    name="nombre"
                                    value={formData.nombre}
                                    onChange={handleChange}
                                    required
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                />
                            </div>
                            <div>
                                <label htmlFor="apellido" className="block text-sm font-medium text-gray-300 mb-1">
                                    Apellido *
                                </label>
                                <input
                                    id="apellido"
                                    type="text"
                                    name="apellido"
                                    value={formData.apellido}
                                    onChange={handleChange}
                                    required
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="dni" className="block text-sm font-medium text-gray-300 mb-1">
                                    DNI *
                                </label>
                                <input
                                    id="dni"
                                    type="text"
                                    name="dni"
                                    value={formData.dni}
                                    onChange={handleChange}
                                    required
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                />
                            </div>
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-1">
                                    Email *
                                </label>
                                <input
                                    id="email"
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="usuario" className="block text-sm font-medium text-gray-300 mb-1">
                                    Usuario *
                                </label>
                                <input
                                    id="usuario"
                                    type="text"
                                    name="usuario"
                                    value={formData.usuario}
                                    onChange={handleChange}
                                    required
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                />
                            </div>
                            <div>
                                <label htmlFor="legajo" className="block text-sm font-medium text-gray-300 mb-1">
                                    Legajo *
                                </label>
                                <input
                                    id="legajo"
                                    type="text"
                                    name="legajo"
                                    value={formData.legajo}
                                    onChange={handleChange}
                                    required
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                />
                            </div>
                        </div>

                        <div>
                            <label htmlFor="contraseña" className="block text-sm font-medium text-gray-300 mb-1">
                                Contraseña *
                            </label>
                            <input
                                id="contraseña"
                                type="password"
                                name="contraseña"
                                value={formData.contraseña}
                                onChange={handleChange}
                                placeholder="Min 8 caracteres, mayúscula y dígito"
                                required
                                disabled={loading}
                                className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="rol" className="block text-sm font-medium text-gray-300 mb-1">
                                    Rol *
                                </label>
                                <select
                                    name="rol"
                                    value={formData.rol}
                                    onChange={handleChange}
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                >
                                    <option value="tecnico">Técnico</option>
                                    <option value="medico">Médico</option>
                                    <option value="vendedor">Vendedor</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="telefono" className="block text-sm font-medium text-gray-300 mb-1">
                                    Teléfono
                                </label>
                                <input
                                    id="telefono"
                                    type="tel"
                                    name="telefono"
                                    value={formData.telefono}
                                    onChange={handleChange}
                                    disabled={loading}
                                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 text-gray-100 rounded-lg focus:outline-none focus:border-indigo-500 text-sm"
                                />
                            </div>
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
                            {loading ? 'Registrando...' : 'Registrarse'}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <p className="text-gray-400 text-sm">
                            ¿Ya tienes cuenta?{' '}
                            <a href="/login" className="text-indigo-400 hover:text-indigo-300 font-medium transition-colors">
                                Inicia sesión aquí
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
