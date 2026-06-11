import Link from "next/link";
import {ReactNode} from "react";

/*Usar fondo oscuro */ 
export default function DashboardLayout({ children }: { children: ReactNode }) {
    return (
        <div className="min-h-screen flex bg-gray-100">
            {/* Sidebar */}
            <aside className="w-64 bg-gray-800 text-white p-6">
                <h2 className="text-2xl font-bold mb-6">Visualion</h2>
                <nav className="space-y-4">
                    <Link href="/dashboard/Paciente" className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors">
                        Pacientes
                    </Link>
                    <Link href="/dashboard/Empleados" className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors">
                        Empleados
                    </Link>
                    <Link href="/dashboard" className="block py-2 px-4 rounded hover:bg-gray-700 transition-colors">
                        Dashboard
                    </Link>
                </nav>
            </aside>
            <main className="flex-1 p-6">
                {children}
            </main>
        </div>
    );
}