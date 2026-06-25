// visualion-frontend/app/portal/clinica/page.tsx
import Link from 'next/link';

export default function ClinicaPortalPage() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <Link href="/" className="text-blue-400 hover:text-blue-300 transition-colors">
          &larr; Volver a la página principal
        </Link>
        <header className="text-center my-8">
          <h1 className="text-5xl font-extrabold text-blue-300">🏥 Portal de Clínica</h1>
          <p className="text-lg text-gray-400 mt-2">Gestiona tus citas y consulta tu información médica.</p>
        </header>
        <main>
          <div className="grid md:grid-cols-2 gap-8">
            {/* Card para agendar turnos */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-2xl font-bold mb-4">📅 Gestión de Turnos</h2>
              <p className="text-gray-400 mb-6">Agenda nuevas citas, consulta tus próximos turnos o cancela si es necesario.</p>
              <Link href="/login?redirect=/dashboard/turnos" className="bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-500 transition-all">
                Agendar Turno
              </Link>
            </div>

            {/* Card para ver historial médico */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-2xl font-bold mb-4">📜 Historial Médico</h2>
              <p className="text-gray-400 mb-6">Accede a tu historial de consultas, recetas y estudios médicos. Requiere inicio de sesión.</p>
              <Link href="/login?redirect=/dashboard/historial" className="bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-500 transition-all">
                Ver Mi Historial
              </Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
