# Mapeo de Estructura Actual vs. Alcance Requerido

## Resumen Ejecutivo
El proyecto cuenta con una **estructura base sólida** pero requiere expansiones significativas para cubrir el alcance completo, especialmente en Taller, Notificaciones y patrones avanzados.

---

## 1. MÓDULO DE GESTIÓN DE PACIENTES Y TURNOS

### ✅ Implementado
- **Modelos**: `Paciente`, `Turno`, `Medico`
- **Controlador**: `paciente.py`, `clinica.py`
- **Campos**: Turnos con estado (pendiente/completado/cancelado)
- **Relaciones**: Paciente ↔ Turno ↔ Medico

### ⚠️ Incompleto / Falta
- [ ] Recordatorios automáticos de turnos (SMS/Email)
- [ ] Gestión de agendas médicas avanzada
- [ ] Confirmación de turnos por paciente
- [ ] Historial de cambios de turno

### 📝 Archivos Relevantes
- `Backend/Models/Usuarios.py` (línea 27-41: clase Paciente)
- `Backend/Models/clinica.py` (línea 5-17: clase Turno)
- `Backend/controllers/clinica.py`

---

## 2. MÓDULO CLÍNICO (OFTALMOLOGÍA)

### ✅ Implementado
- **Modelo**: `RecetaMedica` con parámetros completos
- **Campos**: Esfera, Cilindro, Eje, Adición (OD/OI), Distancia Pupilar
- **Controlador**: `clinica.py`
- **Relaciones**: Turno → RecetaMedica

### ⚠️ Incompleto / Falta
- [ ] **Validador de dioptrías** (Validator Pattern) - Falta validar:
  - Eje no mayor a 180°
  - Rangos válidos de esfera (-25 a +25)
  - Validación de cilindro (-25 a 0)
- [ ] Historia clínica completa (solo hay campos genéricos)
- [ ] Exámenes visuales adicionales (agudeza visual, presión ocular)
- [ ] Vencimiento de receta con notificación

### 📝 Archivos Relevantes
- `Backend/Models/clinica.py` (línea 20-48: clase RecetaMedica)
- `Backend/controllers/clinica.py` (línea 0-???)

---

## 3. MÓDULO COMERCIAL (ÓPTICA)

### ✅ Implementado
- **Modelos**: `Producto`, `Venta`, `DetalleVenta`, `Vendedor`
- **Campos**: SKU, Precio, Stock, Estado de Pago
- **Controlador**: `optica.py`
- **Relaciones**: Venta → DetalleVenta → Producto
- **Vínculo con receta**: Venta.receta_id (opcional)

### ⚠️ Incompleto / Falta
- [ ] **DTOs** (Data Transfer Objects) - Proteger datos internos
- [ ] Gestión de pagos avanzada (múltiples métodos)
- [ ] Facturación digital con numeración
- [ ] Control de stock en tiempo real (alertas)
- [ ] Categorización de productos (Armazones, Cristales, Insumos)

### 📝 Archivos Relevantes
- `Backend/Models/optica.py` (completo)
- `Backend/controllers/optica.py`

---

## 4. MÓDULO DE TALLER Y LABORATORIO

### ❌ FALTA IMPLEMENTAR COMPLETAMENTE
Este es el módulo más crítico y falta casi por completo.

### Requerido
- [ ] **Modelo `OrdenTrabajo`** con campos:
  - ID único, Venta FK, Estado (máquina de estados)
  - Tareas: Biselado, Montaje, Control de Calidad
  - Técnico responsable, Fechas

- [ ] **State Pattern** (Máquina de Estados)
  - Estados válidos: Recibida → Biselado → Montaje → QC → Listo
  - Restricción: No avanza si no pasa QC
  - Transiciones solo permitidas en orden

- [ ] **Trazabilidad**
  - Técnico responsable por etapa
  - Historial de cambios de estado
  - Timestamps

- [ ] **Controlador**: `taller.py`

### 📝 Estructura Propuesta
```
Backend/
├── Models/
│   └── taller.py (NEW)
│       ├── OrdenTrabajo
│       ├── EtapaTrabajo
│       └── EstadoOrden (Enum)
├── controllers/
│   └── taller.py (NEW)
└── schemas/
    └── taller.py (NEW)
```

---

## 5. MÓDULO DE NOTIFICACIONES

### ❌ FALTA IMPLEMENTAR COMPLETAMENTE

### Requerido
- [ ] **Sistema de notificaciones** con eventos:
  - Confirmación de turno (SMS/Email)
  - Aviso de retiro de producto
  - Recordatorio 24h antes de turno
  - Estado de orden en taller

- [ ] **Integraciones**:
  - Proveedor SMS (Twilio, AWS SNS)
  - Email (SendGrid, SMTP)

- [ ] **Modelo**: `Notificacion` (Log de enviadas)

### 📝 Estructura Propuesta
```
Backend/
├── services/
│   ├── notification_service.py (NEW)
│   ├── sms_provider.py (NEW)
│   └── email_provider.py (NEW)
├── Models/
│   └── notificacion.py (NEW)
└── controllers/
    └── notificaciones.py (NEW)
```

---

## 6. PATRONES DE DISEÑO REQUERIDOS

### 🔴 NO IMPLEMENTADOS

| Patrón | Módulo | Estado | Prioridad |
|--------|--------|--------|-----------|
| **Validator** | Salud/Clínica | ❌ Falta | 🔴 Alta |
| **State Pattern** | Taller | ❌ Falta | 🔴 Alta |
| **DTO** | Comercial/Inventario | ❌ Falta | 🟡 Media |
| **Repository** | General | ❌ Falta | 🟡 Media |
| **Service Layer** | General | ⚠️ Parcial | 🟡 Media |

---

## 7. ESTRUCTURA FRONTEND

### ✅ Vistas Existentes
- Dashboard general
- Paciente
- Empleados
- Técnico
- Vendedor

### ⚠️ Falta
- [ ] Módulo Taller/Laboratorio
- [ ] Módulo Notificaciones
- [ ] Componentes de Validación (Recetas)
- [ ] Seguimiento de órdenes en tiempo real

---

## 8. MATRIZ DE PRIORIDADES

| Módulo | % Completado | Prioridad | Acción |
|--------|-------------|-----------|--------|
| Pacientes y Turnos | 60% | 🟡 Media | Mejorar gestión, agregar notificaciones |
| Clínica | 70% | 🔴 Alta | Implementar Validator, completar historia clínica |
| Comercial | 75% | 🟡 Media | Agregar DTOs, facturación |
| Taller | 0% | 🔴 CRÍTICA | Implementar desde cero |
| Notificaciones | 0% | 🔴 CRÍTICA | Implementar desde cero |

---

## Recomendación
**Prioridad de Implementación:**
1. 🔴 **Validador de Recetas** (Validator Pattern) - 2-3 horas
2. 🔴 **Módulo de Taller** (State Pattern) - 4-5 horas
3. 🔴 **Notificaciones** - 3-4 horas
4. 🟡 **DTOs en Comercial** - 2 horas
5. 🟡 **Mejoras en Pacientes** - 2 horas
