"use client";

import { useState } from 'react';
import { Paciente } from './listar_paciente';
import { pacientesService } from '@/service/pacientesService';

interface TablaPacientesProps {
  initialData: Paciente[];
}

export default function TablaPacientes({ initialData }: TablaPacientesProps) {
  const [pacientes, setPacientes] = useState<Paciente[]>(initialData);
  const [busqueda, setBusqueda] = useState('');
  const [modalAbierto, setModalAbierto] = useState(false);
  const [pacienteEditando, setPacienteEditando] = useState<Paciente | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState({
    dni: '',
    nombre: '',
    apellido: '',
    telefono: '',
    email: '',
    obra_social: '',
    historial_medico: '',
  });

  const handleBuscar = async () => {
    if (!busqueda) {
      const data = await pacientesService.listar();
      setPacientes(data);
      return;
    }
    try {
      const paciente = await pacientesService.obtenerPorDni(busqueda);
      setPacientes(paciente ? [paciente] : []);
    } catch (e: any) {
      setError('Error al buscar paciente');
    }
  };

  const abrirModalNuevo = () => {
    setPacienteEditando(null);
    setFormData({
      dni: '',
      nombre: '',
      apellido: '',
      telefono: '',
      email: '',
      obra_social: '',
      historial_medico: '',
    });
    setError(null);
    setModalAbierto(true);
  };

  const abrirModalEditar = (paciente: Paciente) => {
    setPacienteEditando(paciente);
    setFormData({
      dni: paciente.dni,
      nombre: paciente.nombre,
      apellido: paciente.apellido,
      telefono: paciente.telefono || '',
      email: paciente.email || '',
      obra_social: paciente.obra_social || '',
      historial_medico: paciente.historial_medico || '',
    });
    setError(null);
    setModalAbierto(true);
  };

  const handleEliminar = async (dni: string) => {
    if (confirm('¿Está seguro de eliminar este paciente?')) {
      try {
        await pacientesService.eliminar(dni);
        const data = await pacientesService.listar();
        setPacientes(data);
      } catch (e: any) {
        setError(e.message || 'Error al eliminar');
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      if (pacienteEditando) {
        await pacientesService.actualizar(pacienteEditando.id, formData);
      } else {
        await pacientesService.crear(formData);
      }
      setModalAbierto(false);
      const data = await pacientesService.listar();
      setPacientes(data);
    } catch (e: any) {
      setError(e.message || 'Error al guardar');
    }
  };

  return (
    <div className="space-y-4">
      {/* Search and Action Bar */}
      <div className="flex justify-between items-center bg-gray-900 p-4 rounded-lg shadow-sm border border-gray-800">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Buscar por DNI..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-md text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            onClick={handleBuscar}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 rounded-md transition-colors"
          >
            Buscar
          </button>
        </div>
        <button
          onClick={abrirModalNuevo}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-md shadow-sm transition-colors"
        >
          + Nuevo Paciente
        </button>
      </div>

      {error && <div className="p-3 bg-red-900/50 border border-red-500 text-red-200 rounded-md">{error}</div>}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-gray-900 border border-gray-800 rounded-lg overflow-hidden shadow-sm">
          <thead className="bg-gray-800 text-gray-400 uppercase text-xs font-semibold tracking-wider">
            <tr>
              <th className="py-3 px-4 text-left">DNI</th>
              <th className="py-3 px-4 text-left">Nombre</th>
              <th className="py-3 px-4 text-left">Obra Social</th>
              <th className="py-3 px-4 text-left">Teléfono</th>
              <th className="py-3 px-4 text-center">Acciones</th>
            </tr>
          </thead>
          <tbody className="text-gray-300 text-sm divide-y divide-gray-800">
            {pacientes.length === 0 ? (
              <tr>
                <td colSpan={5} className="py-8 text-center text-gray-500">
                  No se encontraron pacientes
                </td>
              </tr>
            ) : (
              pacientes.map((p) => (
                <tr key={p.id} className="hover:bg-gray-800/50 transition-colors">
                  <td className="py-3 px-4 font-medium">{p.dni}</td>
                  <td className="py-3 px-4">{p.nombre} {p.apellido}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-indigo-900/30 text-indigo-300 rounded-full text-xs border border-indigo-800/50">
                      {p.obra_social || 'Ninguna'}
                    </span>
                  </td>
                  <td className="py-3 px-4">{p.telefono || '-'}</td>
                  <td className="py-3 px-4 flex justify-center gap-2">
                    <button
                      onClick={() => abrirModalEditar(p)}
                      className="p-1.5 bg-gray-800 hover:bg-indigo-600 text-gray-300 hover:text-white rounded transition-colors"
                      title="Editar"
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => handleEliminar(p.dni)}
                      className="p-1.5 bg-gray-800 hover:bg-red-600 text-gray-300 hover:text-white rounded transition-colors"
                      title="Eliminar"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {modalAbierto && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
            <div className="p-6 border-b border-gray-800 flex justify-between items-center">
              <h3 className="text-xl font-bold text-gray-100">
                {pacienteEditando ? 'Editar Paciente' : 'Nuevo Paciente'}
              </h3>
              <button 
                onClick={() => setModalAbierto(false)}
                className="text-gray-400 hover:text-gray-100 transition-colors"
              >
                ✕
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Nombre *</label>
                  <input
                    required
                    type="text"
                    value={formData.nombre}
                    onChange={(e) => setFormData({...formData, nombre: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Apellido *</label>
                  <input
                    required
                    type="text"
                    value={formData.apellido}
                    onChange={(e) => setFormData({...formData, apellido: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">DNI *</label>
                <input
                  required
                  type="text"
                  value={formData.dni}
                  onChange={(e) => setFormData({...formData, dni: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Teléfono</label>
                  <input
                    type="text"
                    value={formData.telefono}
                    onChange={(e) => setFormData({...formData, telefono: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Email</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Obra Social</label>
                <input
                  type="text"
                  value={formData.obra_social}
                  onChange={(e) => setFormData({...formData, obra_social: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-400 mb-1">Historial Médico</label>
                <textarea
                  rows={3}
                  value={formData.historial_medico}
                  onChange={(e) => setFormData({...formData, historial_medico: e.target.value})}
                  className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                />
              </div>

              <div className="pt-4 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setModalAbierto(false)}
                  className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-md transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-md shadow-sm transition-colors"
                >
                  {pacienteEditando ? 'Guardar Cambios' : 'Crear Paciente'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
