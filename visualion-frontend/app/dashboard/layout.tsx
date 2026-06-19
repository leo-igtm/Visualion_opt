import Link from "next/link";
import { ReactNode } from "react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
    return (
        <div className="min-h-screen flex bg-gray-950 text-gray-200">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-900 border-r border-gray-800 text-white p-6 shadow-xl z-10 relative overflow-y-auto">
                <div className="mb-8">
                    <Link href="/">
                        <h2 className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-blue-400 hover:from-indigo-300 hover:to-blue-300 transition-all cursor-pointer">
                            Visualion
                        </h2>
                    </Link>
                </div>

                <nav className="space-y-1">
                    {/* Inicio */}
                    <div className="mb-6">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-4 mb-3">
                            Inicio
                        </p>
                        <Link
                            href="/dashboard"
                            className="block py-3 px-4 rounded-lg hover:bg-indigo-600/20 hover:text-indigo-300 transition-all font-medium"
                        >
                            📊 Dashboard
                        </Link>
                    </div>

                    {/* Gestión de Usuarios */}
                    <div className="mb-6">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-4 mb-3">
                            Gestión de Usuarios
                        </p>
                        <Link
                            href="/dashboard/Paciente"
                            className="block py-3 px-4 rounded-lg hover:bg-blue-600/20 hover:text-blue-300 transition-all font-medium"
                        >
                            👥 Pacientes
                        </Link>
                        <Link
                            href="/dashboard/Empleados"
                            className="block py-3 px-4 rounded-lg hover:bg-indigo-600/20 hover:text-indigo-300 transition-all font-medium"
                        >
                            👔 Empleados
                        </Link>
                        <Link
                            href="/dashboard/Usuarios"
                            className="block py-3 px-4 rounded-lg hover:bg-purple-600/20 hover:text-purple-300 transition-all font-medium"
                        >
                            👨‍⚕️ Médicos
                        </Link>
                        <Link
                            href="/dashboard/Tecnico"
                            className="block py-3 px-4 rounded-lg hover:bg-pink-600/20 hover:text-pink-300 transition-all font-medium"
                        >
                            🔐 Técnicos
                        </Link>
                    </div>

                    {/* Operaciones */}
                    <div className="mb-6">
                        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-4 mb-3">
                            Operaciones
                        </p>
                        <Link
                            href="/dashboard/taller"
                            className="block py-3 px-4 rounded-lg hover:bg-green-600/20 hover:text-green-300 transition-all font-medium"
                        >
                            🔧 Taller & Laboratorio
                        </Link>
                        <Link
                            href="/dashboard/Vendedor"
                            className="block py-3 px-4 rounded-lg hover:bg-orange-600/20 hover:text-orange-300 transition-all font-medium"
                        >
                            💰 Ventas
                        </Link>
                    </div>

                    {/* Más */}
                    <div className="border-t border-gray-800 pt-6 mt-6">
                        <button
                            onClick={() => {
                                if (typeof window !== 'undefined') {
                                    localStorage.removeItem('token');
                                    window.location.href = '/login';
                                }
                            }}
                            className="w-full block py-3 px-4 rounded-lg hover:bg-red-600/20 hover:text-red-300 transition-all font-medium text-left"
                        >
                            🚪 Cerrar Sesión
                        </button>
                    </div>
                </nav>
            </aside>

            <main className="flex-1 p-6 relative overflow-auto">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 pointer-events-none" />
                <div className="relative z-10">
                    {children}
                </div>
            </main>
        </div>
    );
}