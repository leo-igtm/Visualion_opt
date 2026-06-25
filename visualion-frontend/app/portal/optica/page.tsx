// visualion-frontend/app/portal/optica/page.tsx
import Link from 'next/link';

export default function OpticaPortalPage() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <Link href="/" className="text-green-400 hover:text-green-300 transition-colors">
          &larr; Volver a la página principal
        </Link>
        <header className="text-center my-8">
          <h1 className="text-5xl font-extrabold text-green-300">👓 Portal de Óptica</h1>
          <p className="text-lg text-gray-400 mt-2">Explora nuestros productos y sigue el estado de tus pedidos.</p>
        </header>
        <main>
          <div className="grid md:grid-cols-2 gap-8">
            {/* Card para el catálogo */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-2xl font-bold mb-4">📖 Catálogo de Productos</h2>
              <p className="text-gray-400 mb-6">Navega por nuestra amplia selección de armazones, lentes y accesorios de las mejores marcas.</p>
              <Link href="/catalogo" className="bg-green-600 text-white font-bold py-2 px-4 rounded hover:bg-green-500 transition-all">
                Explorar Catálogo
              </Link>
            </div>

            {/* Card para seguir pedido */}
            <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
              <h2 className="text-2xl font-bold mb-4">🚚 Seguimiento de Pedido</h2>
              <p className="text-gray-400 mb-6">Ingresa tu número de orden para ver en qué etapa se encuentra tu pedido de lentes.</p>
              <div className="flex gap-2">
                <input type="text" placeholder="Número de orden" className="bg-gray-700 text-white border border-gray-600 rounded px-3 py-2 w-full focus:ring-green-500 focus:border-green-500" />
                <button className="bg-green-600 text-white font-bold py-2 px-4 rounded hover:bg-green-500 transition-all">
                  Seguir
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
