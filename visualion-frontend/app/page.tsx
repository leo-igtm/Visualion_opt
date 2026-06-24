'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import ModuleCard from '@/componentes/ModuleCard';

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    const token = localStorage.getItem('token');
    setTimeout(() => {
      setIsAuthenticated(!!token);
      setIsLoading(false);
    }, 0);
  }, []);

  const modules = [
    {
      title: '👥 Pacientes',
      description: 'Gestiona el registro completo de pacientes, historial médico, obra social y seguimiento de atenciones.',
      icon: '👥',
      href: '/dashboard/Paciente',
      color: 'blue' as const,
    },
    {
      title: '👔 Personal',
      description: 'Administra empleados, técnicos, vendedores, médicos y sus datos de registro.',
      icon: '👔',
      href: '/dashboard/Empleados',
      color: 'indigo' as const,
    },
    {
      title: '🔧 Taller & Laboratorio',
      description: 'Control de órdenes de trabajo, etapas de producción, seguimiento y calidad de lentes.',
      icon: '🔧',
      href: '/dashboard/taller',
      color: 'green' as const,
    },
    {
      title: '💰 Ventas',
      description: 'Registro de ventas, comprobantes, detalles de productos y seguimiento de pagos.',
      icon: '💰',
      href: '/dashboard/Vendedor',
      color: 'orange' as const,
    },
    {
      title: '👨‍⚕️ Médicos',
      description: 'Gestión de médicos especialistas, matriculas y gestión de turnos médicos.',
      icon: '👨‍⚕️',
      href: '/dashboard/Usuarios',
      color: 'purple' as const,
    },
    {
      title: '🔐 Técnicos',
      description: 'Administración de técnicos ópticos, seguimiento de trabajo y producción.',
      icon: '🔐',
      href: '/dashboard/Tecnico',
      color: 'pink' as const,
    },
  ];

  if (isLoading) {
    return <div className="min-h-screen bg-gray-950 flex items-center justify-center">Cargando...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 text-gray-200">
      {/* Hero Section */}
      <header className="bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-700 text-white py-16 px-6 shadow-2xl">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-block mb-6">
            <span className="bg-white/10 backdrop-blur-md px-4 py-2 rounded-full text-sm font-medium text-blue-100 border border-white/20">
              Sistema de Gestión Integral
            </span>
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-4 leading-tight">
            Visualion
          </h1>

          <p className="text-lg md:text-xl text-blue-100 max-w-2xl mx-auto mb-8 leading-relaxed">
            Plataforma completa para la gestión de clínicas oftalmológicas y ópticas. Controla pacientes, personal, producción y ventas en un solo lugar.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {isAuthenticated ? (
              <>
                <Link
                  href="/dashboard"
                  className="inline-block bg-white text-blue-700 font-bold px-8 py-3 rounded-lg shadow-lg hover:shadow-xl hover:bg-blue-50 transition-all duration-300 transform hover:scale-105"
                >
                  ⚙️ Acceder al Dashboard
                </Link>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="inline-block bg-white text-blue-700 font-bold px-8 py-3 rounded-lg shadow-lg hover:shadow-xl hover:bg-blue-50 transition-all duration-300 transform hover:scale-105"
                >
                  🔐 Iniciar Sesión
                </Link>
                <Link
                  href="/register"
                  className="inline-block bg-white/10 backdrop-blur-md text-white font-bold px-8 py-3 rounded-lg border border-white/30 hover:bg-white/20 transition-all duration-300"
                >
                  📝 Registrarse
                </Link>
              </>
            )}
            <Link
              href="#modulos"
              className="inline-block bg-white/10 backdrop-blur-md text-white font-bold px-8 py-3 rounded-lg border border-white/30 hover:bg-white/20 transition-all duration-300"
            >
              📋 Ver Módulos
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-16">
        {/* Estadísticas Rápidas */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-100 mb-8 flex items-center gap-3">
            <span className="bg-gradient-to-r from-blue-500 to-indigo-500 h-1 w-12 rounded-full"></span>
            Estado General
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { label: 'Módulos Disponibles', value: '6', icon: '📦' },
              { label: 'Estado Sistema', value: 'Activo', icon: '✅' },
              { label: 'Roles de Usuario', value: '5', icon: '🔐' },
              { label: 'Versión', value: '1.1.0', icon: '📌' },
            ].map((stat) => (
              <div
                key={stat.label}
                className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-gray-700 transition-colors"
              >
                <div className="text-3xl mb-2">{stat.icon}</div>
                <p className="text-gray-400 text-sm mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-100">{stat.value}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Módulos Grid */}
        <section id="modulos">
          <h2 className="text-3xl font-bold text-gray-100 mb-8 flex items-center gap-3">
            <span className="bg-gradient-to-r from-green-500 to-emerald-500 h-1 w-12 rounded-full"></span>
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
        </section>

        {/* Características */}
        <section className="mt-20 bg-gray-900 border border-gray-800 rounded-2xl p-12">
          <h2 className="text-3xl font-bold text-gray-100 mb-8 flex items-center gap-3">
            <span className="bg-gradient-to-r from-purple-500 to-pink-500 h-1 w-12 rounded-full"></span>
            Características Principales
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              {
                title: 'Gestión Integral de Pacientes',
                description: 'Registro completo con historial médico, obra social y seguimiento de atenciones.',
              },
              {
                title: 'Control de Personal',
                description: 'Administra empleados, técnicos, vendedores y médicos de manera centralizada.',
              },
              {
                title: 'Taller & Laboratorio',
                description: 'Seguimiento completo de órdenes de trabajo desde recepción hasta entrega.',
              },
              {
                title: 'Sistema de Ventas',
                description: 'Control de ventas, comprobantes, detalles de productos y seguimiento de pagos.',
              },
              {
                title: 'Gestión de Turnos',
                description: 'Programación de citas médicas y seguimiento de atenciones.',
              },
              {
                title: 'Validación Oftalmológica',
                description: 'Validadores inteligentes para parámetros de dioptrías y recetas.',
              },
            ].map((feature) => (
              <div key={feature.title} className="flex gap-4">
                <div className="text-2xl mt-1">✓</div>
                <div>
                  <h3 className="font-bold text-gray-100 mb-1">{feature.title}</h3>
                  <p className="text-gray-400 text-sm">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        {!isAuthenticated && (
          <section className="mt-20 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-12 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">¿Listo para comenzar?</h2>
            <p className="text-blue-100 mb-8 max-w-xl mx-auto">
              Crea tu cuenta ahora y accede a todas las funcionalidades de Visualion para gestionar tu negocio oftalmológico.
            </p>
            <Link
              href="/register"
              className="inline-block bg-white text-indigo-600 font-bold px-10 py-4 rounded-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            >
              Crear Cuenta Gratis →
            </Link>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-8 px-6 mt-16">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-gray-100 mb-4">Visualion</h3>
              <p className="text-gray-400 text-sm">Sistema de gestión integral para ópticas y clínicas oftalmológicas.</p>
            </div>
            <div>
              <h3 className="font-bold text-gray-100 mb-4">Acceso Rápido</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>
                  <Link href={isAuthenticated ? '/dashboard' : '/login'} className="hover:text-indigo-400">
                    {isAuthenticated ? 'Dashboard' : 'Iniciar Sesión'}
                  </Link>
                </li>
                {!isAuthenticated && (
                  <li>
                    <Link href="/register" className="hover:text-indigo-400">
                      Registrarse
                    </Link>
                  </li>
                )}
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-gray-100 mb-4">Soporte</h3>
              <p className="text-gray-400 text-sm">Contacta con el equipo técnico para más información.</p>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-6 text-center text-gray-400 text-xs">
            <p>© {new Date().getFullYear()} Visualion. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
