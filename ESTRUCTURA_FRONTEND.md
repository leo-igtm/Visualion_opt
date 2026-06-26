# 📱 Estructura de Frontend - Guía de Navegación

## Flujo de Navegación

### 1. **Página Principal** (`/`)
- **Ubicación**: `app/page.tsx`
- **Propósito**: Landing page / Hub de bienvenida
- **Contenido**:
  - Hero section con descripción de Visualion
  - Grid de 6 módulos principales
  - Estadísticas del sistema
  - Características principales
  - Footer con accesos rápidos

### 2. **Dashboard** (`/dashboard`)
- **Ubicación**: `app/dashboard/page.tsx`
- **Propósito**: Panel de control centralizado
- **Layout**: Incluye sidebar con navegación
- **Contenido**:
  - Estadísticas rápidas (Pacientes, Personal, Órdenes, Ventas)
  - Grid con acceso a todos los módulos
  - Acciones rápidas

### 3. **Módulos Disponibles**

#### **Gestión de Usuarios**
- 👥 **Pacientes** (`/dashboard/Paciente`) - Registro y seguimiento de pacientes
- 👔 **Empleados** (`/dashboard/Empleados`) - Administración de personal
- 👨‍⚕️ **Médicos** (`/dashboard/Usuarios`) - Gestión de médicos
- 🔐 **Técnicos** (`/dashboard/Tecnico`) - Administración de técnicos ópticos

#### **Operaciones**
- 🔧 **Taller & Laboratorio** (`/dashboard/taller`) - Órdenes de trabajo
- 💰 **Ventas** (`/dashboard/Vendedor`) - Gestión de ventas

---

## Componentes Principales

### ModuleCard.tsx
**Propósito**: Componente reutilizable para mostrar módulos
**Props**:
- `title`: Título del módulo
- `description`: Descripción corta
- `icon`: Emoji o icono
- `href`: Ruta del módulo
- `color`: Tema de color (blue, indigo, green, orange, purple, pink)

**Uso**:
```tsx
<ModuleCard
  title="👥 Pacientes"
  description="Gestiona el registro de pacientes..."
  icon="👥"
  href="/dashboard/Paciente"
  color="blue"
/>
```

---

## Sidebar de Dashboard

**Ubicación**: `app/dashboard/layout.tsx`

**Secciones**:
1. **Inicio**
   - 📊 Dashboard

2. **Gestión de Usuarios**
   - 👥 Pacientes
   - 👔 Empleados
   - 👨‍⚕️ Médicos
   - 🔐 Técnicos

3. **Operaciones**
   - 🔧 Taller & Laboratorio
   - 💰 Ventas

4. **Más**
   - 🚪 Cerrar Sesión

---

## Estructura de Carpetas

```
visualion-frontend/
├── app/
│   ├── page.tsx                    (Página principal - Landing)
│   ├── layout.tsx                  (Layout root)
│   ├── login/
│   ├── register/
│   └── dashboard/
│       ├── page.tsx                (Dashboard home)
│       ├── layout.tsx              (Sidebar)
│       ├── Paciente/
│       ├── Empleados/
│       ├── Usuarios/
│       ├── Tecnico/
│       ├── Vendedor/
│       └── taller/
│
├── componentes/
│   ├── ModuleCard.tsx              (Tarjeta de módulo)
│   ├── ListaOrdenesTrabajo.tsx
│   ├── DetallesOrdenTrabajo.tsx
│   ├── EstadoOrdenBadge.tsx
│   └── [otros componentes]
│
├── service/
│   ├── api.ts                      (API base)
│   └── tallerService.ts            (Servicios específicos)
│
├── types/
│   └── taller.ts
│
└── utils/
    └── tallerValidations.ts
```

---

## Flujo de Usuario

### Usuario No Autenticado
```
/ (Landing) → /login → /register → (Autenticado)
```

### Usuario Autenticado
```
/ (Landing) → /dashboard (Home Panel)
    ↓
    ├─ /dashboard/Paciente
    ├─ /dashboard/Empleados
    ├─ /dashboard/Usuarios
    ├─ /dashboard/Tecnico
    ├─ /dashboard/Vendedor
    └─ /dashboard/taller → /dashboard/taller/[id]
```

---

## Cambios Realizados

### ✅ Nueva Página Principal
- Mejorada con hero section
- Grid de 6 módulos
- Estadísticas y características
- Footer con información

### ✅ Dashboard Centralizado
- Hub de control unificado
- Acceso rápido a todos los módulos
- Estadísticas relevantes
- Acciones frecuentes

### ✅ Sidebar Mejorado
- Navegación clara por secciones
- Acceso a todos los módulos
- Opción de cerrar sesión

### ✅ Componente ModuleCard
- Reutilizable en landing y dashboard
- Diseño consistente
- Temas de color por módulo

---

## Notas Importantes

1. **Consistencia Visual**: Todos los módulos usan el mismo diseño y paleta de colores
2. **Responsive**: Diseño adaptable a mobile, tablet y desktop
3. **Accesibilidad**: Links claros y navegación intuitiva
4. **Performance**: Uso de Suspense para componentes async
5. **Type Safety**: Componentes totalmente tipados con TypeScript

---

## Próximos Pasos (Opcionales)

1. Renombrar componentes antiguos a PascalCase
2. Consolidar servicios API en estructura modular
3. Agregar análitica y dashboards personalizados
4. Implementar autenticación en rutas protegidas
5. Agregar notificaciones y confirmaciones
