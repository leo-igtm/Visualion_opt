# 📚 Guía de Servicios, Autenticación y Error Handling

## 1. Servicios Consolidados

### Estructura Modular
```
service/
├── api.ts                    # API base con métodos genéricos
├── authService.ts            # Autenticación y gestión de usuarios
├── pacientesService.ts       # Gestión de pacientes
├── empleadosService.ts       # Gestión de empleados
└── tallerService.ts          # Gestión de órdenes de trabajo
```

### Uso de Servicios

#### API Base
```typescript
import { API, APIError } from "@/service/api";

// GET
const datos = await API.GET<User[]>("/usuarios");

// POST
const nuevo = await API.POST<User>("/usuarios", { nombre: "Juan" });

// PUT
const actualizado = await API.PUT<User>("/usuarios/1", { nombre: "Pedro" });

// DELETE
await API.DELETE("/usuarios/1");
```

#### Servicio de Pacientes
```typescript
import { pacientesService } from "@/service/pacientesService";

// Listar todos
const pacientes = await pacientesService.listar();

// Obtener por ID
const paciente = await pacientesService.obtenerPorId(1);

// Crear
const nuevo = await pacientesService.crear({
  dni: "12345678",
  nombre: "Juan",
  apellido: "Pérez",
});

// Actualizar
const actualizado = await pacientesService.actualizar(1, {
  nombre: "Juan Carlos",
});

// Eliminar
await pacientesService.eliminar("12345678");
```

#### Servicio de Autenticación
```typescript
import { authService } from "@/service/authService";

// Login
const response = await authService.login("usuario", "contraseña");
authService.guardarToken(response.access_token);

// Register
const user = await authService.register({
  usuario: "nuevo",
  contraseña: "segura",
  nombre: "Juan",
  apellido: "Pérez",
  dni: "12345678",
  rol: "tecnico",
});

// Logout
authService.logout();

// Verificar autenticación
const isAuth = authService.estaAutenticado();
```

---

## 2. Autenticación en Rutas Protegidas

### Middleware (`middleware.ts`)
- Valida token en cookies
- Redirige a `/login` si no hay autenticación
- Redirige a `/dashboard` si intenta acceder a login siendo autenticado
- Rutas públicas: `/`, `/login`, `/register`

### Hook useAuth
```typescript
"use client";

import { useAuth } from "@/hooks/useAuth";

export default function ProtectedComponent() {
  const { isAuthenticated, isLoading, error, logout } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error} />;
  if (!isAuthenticated) return null;

  return (
    <div>
      <button onClick={logout}>Cerrar Sesión</button>
    </div>
  );
}
```

### Setup en Login
```typescript
// 1. Guardar token en localStorage
authService.guardarToken(response.access_token);

// 2. Guardar token en cookie (para middleware)
document.cookie = `token=${response.access_token}; path=/; max-age=86400`;

// 3. Redirigir a dashboard
router.push("/dashboard");
```

---

## 3. Loading States

### Componente LoadingSpinner
```typescript
import { LoadingSpinner } from "@/componentes/Loading";

<LoadingSpinner message="Cargando datos..." />
```

### Componente LoadingSkeleton
```typescript
import { LoadingSkeleton } from "@/componentes/Loading";

<LoadingSkeleton rows={3} />
```

### Hook useAsyncData
```typescript
"use client";

import { useAsyncData } from "@/hooks/useAsyncData";
import { pacientesService } from "@/service/pacientesService";

export default function PacientesList() {
  const { data: pacientes, loading, error, retry } = useAsyncData(
    () => pacientesService.listar(),
    {
      onError: (err) => console.error("Error:", err.detail),
      onSuccess: (data) => console.log("Datos cargados:", data),
    }
  );

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorAlert message={error.detail} retry={retry} />;

  return (
    <div>
      {pacientes?.map((p) => (
        <div key={p.id}>{p.nombre}</div>
      ))}
    </div>
  );
}
```

---

## 4. Error Handling

### Clases de Error
```typescript
import { APIError } from "@/service/api";

try {
  const data = await pacientesService.obtenerPorDni("12345678");
} catch (error) {
  if (error instanceof APIError) {
    console.log("Status:", error.status);
    console.log("Mensaje:", error.detail);
  }
}
```

### Componentes de Error

#### ErrorAlert
```typescript
import { ErrorAlert } from "@/componentes/Error";

<ErrorAlert
  title="Error"
  message="No se pudo cargar los datos"
  retry={() => fetchData()}
  backLink="/dashboard"
/>
```

#### ErrorBoundary
```typescript
"use client";

import { ErrorBoundary } from "@/componentes/Error";

export default function PageWithBoundary() {
  return (
    <ErrorBoundary
      error={new Error("Algo falló")}
      reset={() => window.location.reload()}
    />
  );
}
```

#### WarningAlert
```typescript
import { WarningAlert } from "@/componentes/Error";

const [showWarning, setShowWarning] = useState(true);

<WarningAlert
  message="Esta acción no se puede deshacer"
  onDismiss={() => setShowWarning(false)}
/>
```

#### SuccessAlert
```typescript
import { SuccessAlert } from "@/componentes/Error";

<SuccessAlert
  message="Paciente guardado exitosamente"
  onDismiss={() => setShowSuccess(false)}
/>
```

---

## 5. Ejemplo Completo

```typescript
"use client";

import { useEffect, useState } from "react";
import { pacientesService, Paciente } from "@/service/pacientesService";
import { APIError } from "@/service/api";
import { LoadingSpinner, LoadingSkeleton } from "@/componentes/Loading";
import { ErrorAlert, SuccessAlert } from "@/componentes/Error";

export default function PacientesPage() {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<APIError | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchPacientes();
  }, []);

  const fetchPacientes = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await pacientesService.listar();
      setPacientes(data);
      setSuccess("Pacientes cargados correctamente");
    } catch (err) {
      if (err instanceof APIError) {
        setError(err);
      } else {
        setError(new APIError(500, "Error desconocido"));
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Cargando pacientes..." />;

  return (
    <div className="space-y-4">
      {error && (
        <ErrorAlert
          title="Error al cargar"
          message={error.detail}
          retry={fetchPacientes}
        />
      )}

      {success && (
        <SuccessAlert
          message={success}
          onDismiss={() => setSuccess(null)}
        />
      )}

      <div className="grid gap-4">
        {pacientes.map((p) => (
          <div key={p.id} className="p-4 bg-gray-900 rounded-lg">
            {p.nombre} {p.apellido}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 6. Notas Importantes

✅ **Hacer**:
- Usar servicios específicos por módulo
- Manejar `APIError` para errores de API
- Mostrar `LoadingSpinner` mientras se cargan datos
- Mostrar `ErrorAlert` cuando falle una solicitud
- Usar `useAuth` en rutas protegidas

❌ **No hacer**:
- Usar `fetch` directamente (usar servicios)
- Usar `any` en tipos (usar tipos específicos)
- Ignorar errores de API
- Mantener estados sin sincronizar
- Hardcodear URLs (usar servicios)

---

## 7. Checklist de Implementación

- ✅ Servicios consolidados y modularizados
- ✅ Middleware de autenticación
- ✅ Hook useAuth para rutas protegidas
- ✅ Hook useAsyncData para manejo de datos
- ✅ Componentes de Loading
- ✅ Componentes de Error
- ✅ Ejemplo en ListaOrdenesTrabajo
- ✅ Actualización de página de login
