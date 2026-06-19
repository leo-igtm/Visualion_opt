import Link from "next/link";
import ModuleCard from "@/componentes/ModuleCard";

export default function DashboardHome() {
  const modules = [
    {
      title: "👥 Pacientes",
      description: "Gestiona pacientes y registros médicos",
      icon: "👥",
      href: "/dashboard/Paciente",
      color: "blue" as const,
    },
    {
      title: "👔 Personal",
      description: "Administra empleados y roles",
      icon: "👔",
      href: "/dashboard/Empleados",
      color: "indigo" as const,
    },
    {
      title: "🔧 Taller",
      description: "Control de órdenes de trabajo",
      icon: "🔧",
      href: "/dashboard/taller",
      color: "green" as const,
    },
    {
      title: "💰 Ventas",
      description: "Gestión de ventas y pagos",
      icon: "💰",
      href: "/dashboard/Vendedor",
      color: "orange" as const,
    },
    {
      title: "👨‍⚕️ Médicos",
      description: "Administración de médicos",
      icon: "👨‍⚕️",
      href: "/dashboard/Usuarios",
      color: "purple" as const,
    },
    {
      title: "🔐 Técnicos",
      description: "Gestión de técnicos ópticos",
      icon: "🔐",
      href: "/dashboard/Tecnico",
      color: "pink" as const,
    },
  ];

  return (
    <main className="p-8 max-w-7xl mx-auto w-full">
      {/* Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-bold text-gray-100 mb-2">
          Panel de Control
        </h1>
        <p className="text-gray-400 text-lg">
          Bienvenido. Accede a cualquier módulo desde aquí.
        </p>
      </div>

      {/* Estadísticas Rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
        {[
          { label: "Total Pacientes", value: "--", icon: "👥", color: "bg-blue-600/10 border-blue-600/30" },
          { label: "Personal Activo", value: "--", icon: "👔", color: "bg-indigo-600/10 border-indigo-600/30" },
          { label: "Órdenes Pendientes", value: "--", icon: "🔧", color: "bg-green-600/10 border-green-600/30" },
          { label: "Ventas Este Mes", value: "--", icon: "💰", color: "bg-orange-600/10 border-orange-600/30" },
        ].map((stat) => (
          <div
            key={stat.label}
            className={`${stat.color} border rounded-xl p-6 backdrop-blur-sm`}
          >
            <div className="text-3xl mb-3">{stat.icon}</div>
            <p className="text-gray-400 text-sm mb-2 font-medium">{stat.label}</p>
            <p className="text-3xl font-bold text-gray-100">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Módulos Grid */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold text-gray-100 mb-6 flex items-center gap-3">
          <span className="bg-gradient-to-r from-indigo-500 to-blue-500 h-1 w-8 rounded-full"></span>
          Módulos Disponibles
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((module) => (
            <ModuleCard
              key={module.href}
              title={module.title}
              description={module.description}
              icon={module.icon}
              href={module.href}
              color={module.color}
            />
          ))}
        </div>
      </div>

      {/* Acciones Rápidas */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-100 mb-6 flex items-center gap-3">
          <span className="bg-gradient-to-r from-purple-500 to-pink-500 h-1 w-8 rounded-full"></span>
          Acciones Rápidas
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/dashboard/Paciente"
            className="bg-blue-600/10 border border-blue-600/30 rounded-lg p-4 hover:bg-blue-600/20 transition-colors"
          >
            <p className="font-semibold text-blue-300 mb-1">+ Nuevo Paciente</p>
            <p className="text-sm text-gray-400">Registra un nuevo paciente en el sistema</p>
          </Link>

          <Link
            href="/dashboard/taller"
            className="bg-green-600/10 border border-green-600/30 rounded-lg p-4 hover:bg-green-600/20 transition-colors"
          >
            <p className="font-semibold text-green-300 mb-1">+ Nueva Orden Taller</p>
            <p className="text-sm text-gray-400">Crear orden de trabajo para el laboratorio</p>
          </Link>

          <Link
            href="/dashboard/Vendedor"
            className="bg-orange-600/10 border border-orange-600/30 rounded-lg p-4 hover:bg-orange-600/20 transition-colors"
          >
            <p className="font-semibold text-orange-300 mb-1">+ Nueva Venta</p>
            <p className="text-sm text-gray-400">Registrar nueva venta de productos</p>
          </Link>

          <Link
            href="/dashboard/Empleados"
            className="bg-indigo-600/10 border border-indigo-600/30 rounded-lg p-4 hover:bg-indigo-600/20 transition-colors"
          >
            <p className="font-semibold text-indigo-300 mb-1">+ Nuevo Empleado</p>
            <p className="text-sm text-gray-400">Agregar nuevo miembro al personal</p>
          </Link>
        </div>
      </div>
    </main>
  );
}
