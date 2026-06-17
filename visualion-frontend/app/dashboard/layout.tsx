import Link from "next/link";
import {ReactNode} from "react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
    return (
        <div className="min-h-screen flex bg-gray-950 text-gray-200">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-900 border-r border-gray-800 text-white p-6 shadow-xl z-10 relative">
                <h2 className="text-2xl font-extrabold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-blue-400">Visualion</h2>
                <nav className="space-y-2">
                    <Link href="/dashboard/Paciente" className="block py-3 px-4 rounded-lg hover:bg-indigo-600/20 hover:text-indigo-300 transition-all font-medium">
                        👥 Pacientes
                    </Link>
                    <Link href="/dashboard/Empleados" className="block py-3 px-4 rounded-lg hover:bg-indigo-600/20 hover:text-indigo-300 transition-all font-medium">
                        👔 Empleados
                    </Link>
                    <Link href="/dashboard" className="block py-3 px-4 rounded-lg hover:bg-indigo-600/20 hover:text-indigo-300 transition-all font-medium mt-6 border border-gray-800">
                        📊 Dashboard
                    </Link>
                </nav>
            </aside>
            <main className="flex-1 p-6 relative">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 pointer-events-none" />
                <div className="relative z-10">
                    {children}
                </div>
            </main>
        </div>
    );
}