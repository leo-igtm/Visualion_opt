# 🔗 Guía de Integración Backend-Frontend

## Backend: Estructura de Usuarios

### Modelo de Herencia (SQLAlchemy Polymorph)
```
Persona (tabla: personas)
├── dni, nombre, apellido, telefono, email
└── tipo_persona (discriminador)
    ├── Paciente (tabla: pacientes)
    │   └── obra_social, historial_medico
    │
    └── Empleado (tabla: empleados)
        ├── legajo, usuario, contraseña, rol
        └── Hereda en:
            ├── Medico (tabla: medicos)
            │   └── matricula, especialidad
            ├── Tecnico (tabla: tecnicos)
            │   └── matricula_optico
            └── Vendedor (tabla: vendedores)
                └── comisiones
```

### Endpoints de Autenticación
```
POST   /auth/login       → Autentica usuario
POST   /auth/register    → Registra nuevo empleado
GET    /auth/usuarios    → Lista todos los empleados
GET    /auth/usuarios/{id}   → Obtiene empleado por ID
PUT    /auth/usuarios/{id}   → Actualiza empleado
DELETE /auth/usuarios/{id}   → Elimina empleado
```

### Respuestas del Backend

#### Login
```json
{
  "access_token": "token_1_usuario",
  "token_type": "bearer"
}
```

#### Register / Get Usuario
```json
{
  "id": 1,
  "dni": "12345678",
  "nombre": "Juan",
  "apellido": "Pérez",
  "telefono": "1122334455",
  "email": "juan@example.com",
  "legajo": "TEC-001",
  "usuario": "liotect",
  "rol": "tecnico"
}
```

---

## Frontend: Servicios de Autenticación

### authService.ts
```typescript
import { authService } from "@/service/authService";

// Login
const response = await authService.login("usuario", "contraseña");
authService.guardarToken(response.access_token);

// Register
const empleado = await authService.register({
  dni: "12345678",
  nombre: "Juan",
  apellido: "Pérez",
  usuario: "juanperez",
  contraseña: "Password123",
  rol: "tecnico",
  legajo: "TEC-001",
  matricula_optico: "MAT-001"
});

// Listar usuarios
const usuarios = await authService.obtenerUsuarios();

// Obtener usuario
const usuario = await authService.obtenerUsuario(1);

// Actualizar usuario
const actualizado = await authService.actualizarUsuario(1, {
  nombre: "Juan Carlos"
});

// Eliminar usuario
await authService.eliminarUsuario(1);
```

### empleadosService.ts
```typescript
import { empleadosService } from "@/service/empleadosService";

// Listar empleados
const empleados = await empleadosService.listar();

// Listar por rol
const tecnicos = await empleadosService.listarPorRol("tecnico");
const medicos = await empleadosService.listarPorRol("medico");
const vendedores = await empleadosService.listarPorRol("vendedor");
```

---

## Flujo Completo de Autenticación

### 1. Login
```
Usuario ingresa credenciales
    ↓
POST /auth/login con {usuario, contraseña}
    ↓
Backend valida en tabla Empleado
    ↓
Respuesta: {access_token}
    ↓
Frontend guarda en localStorage + cookie
    ↓
Redirige a /dashboard
```

### 2. Protección de Rutas
```
Usuario accede a /dashboard
    ↓
Middleware valida token en cookies
    ↓
Si existe token → Permite acceso ✅
Si no existe → Redirige a /login 🔄
```

### 3. Peticiones Autenticadas
```
Frontend hace petición con header Authorization
    ↓
Backend valida token
    ↓
Si válido → Procesa solicitud
Si inválido → Error 401
```

---

## Mapeo de Tipos

### Backend → Frontend

| Backend | Frontend | Ubicación |
|---------|----------|-----------|
| `Empleado` | `Empleado` | `authService.ts` |
| `EmpleadoRegister` | `EmpleadoRegister` | `authService.ts` |
| `TokenResponse` | `AuthResponse` | `authService.ts` |
| `/auth/*` | `authService.*` | `service/authService.ts` |
| `/auth/usuarios` | `empleadosService.*` | `service/empleadosService.ts` |

---

## Validaciones en Backend

### Contraseña (Register)
- ✅ Mínimo 8 caracteres
- ✅ Incluir mayúsculas
- ✅ Incluir dígitos

### Unicidad
- ✅ `usuario` único
- ✅ `dni` único
- ✅ `email` único

### Sanitización
- ✅ DNI: números
- ✅ Email: formato válido
- ✅ Strings: sin caracteres especiales

---

## Roles Disponibles

```
"medico"     → Médico oftalmólogo
"tecnico"    → Técnico óptico
"vendedor"   → Vendedor
"empleado"   → Empleado genérico
```

### Campos por Rol

**Médico**
- matricula (requerido)
- especialidad (requerido)

**Técnico**
- matricula_optico (requerido)

**Vendedor**
- comisiones (opcional, default 0.0)

---

## Ejemplo: Registrar Técnico

### Backend
```python
@router.post("/auth/register", response_model=EmpleadoOut)
async def register(user_data: EmpleadoRegister, db: AsyncSession = Depends(get_db)):
    # Si rol == "tecnico", crea instancia Tecnico
    # Hereda de Empleado que hereda de Persona
```

### Frontend
```typescript
const nuevo = await authService.register({
  dni: "12345678",
  nombre: "Carlos",
  apellido: "López",
  usuario: "clopez",
  contraseña: "SecurePass123",
  rol: "tecnico",
  legajo: "TEC-002",
  matricula_optico: "MAT-02"
});
// Response: Empleado con id, rol, etc.
```

---

## Checklist de Sincronización

✅ Backend devuelve `access_token` en login
✅ Frontend guarda en localStorage + cookie
✅ Middleware valida token en cookies
✅ API base incluye Authorization header
✅ authService mapea a `/auth/*`
✅ empleadosService mapea a `/auth/usuarios`
✅ Tipos coinciden entre backend y frontend
✅ Validaciones en backend reflejadas en frontend

---

## Troubleshooting

### Error: "Credenciales inválidas"
- Verificar que `usuario` existe en BD
- Verificar que contraseña es correcta
- Backend busca en tabla `empleados` con columna `usuario`

### Error: "Usuario, DNI o email ya existe"
- Usuario ya registrado
- DNI duplicado
- Email duplicado

### Error: Token no se valida
- Verificar que token se guardó en cookie
- Verificar nombre de cookie: `token`
- Middleware espera cookie con nombre `token`

### Error: No se redirige a dashboard
- Verificar que middlewre.ts existe
- Verificar que token se guardó correctamente
- Revisar console del navegador para errores

---

## Notas Importantes

🔐 **Seguridad**:
- Contraseñas hasheadas con bcrypt
- Tokens simples (TODO: implementar JWT)
- CORS configurado para localhost:3000

📝 **Datos**:
- `tipo_persona` discriminador para herencia
- Empleados heredan de Persona
- Roles determinan subclase (Medico, Tecnico, Vendedor)

⚙️ **API**:
- Base URL: `http://localhost:8000`
- Autenticación: En headers `Authorization: Bearer <token>`
- Token válido por: 24 horas (max-age=86400)
