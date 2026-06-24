-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         PostgreSQL 18.2 on x86_64-windows, compiled by msvc-19.44.35222, 64-bit
-- SO del servidor:              
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES  */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura para tabla public.alembic_version
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num" VARCHAR(32) NOT NULL,
	PRIMARY KEY ("version_num")
);

-- Volcando datos para la tabla public.alembic_version: -1 rows
/*!40000 ALTER TABLE "alembic_version" DISABLE KEYS */;
INSERT INTO "alembic_version" ("version_num") VALUES
	('a1b2c3d4e5f6');
/*!40000 ALTER TABLE "alembic_version" ENABLE KEYS */;

-- Volcando estructura para tabla public.detalleVentas
CREATE TABLE IF NOT EXISTS "detalleVentas" (
	"id" SERIAL NOT NULL,
	"venta_id" INTEGER NOT NULL,
	"producto_id" INTEGER NOT NULL,
	"cantidad" INTEGER NOT NULL,
	"precio_unitario" DOUBLE PRECISION NOT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "detalleVentas_producto_id_fkey" FOREIGN KEY ("producto_id") REFERENCES "productos" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "detalleVentas_venta_id_fkey" FOREIGN KEY ("venta_id") REFERENCES "ventas" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.detalleVentas: -1 rows
/*!40000 ALTER TABLE "detalleVentas" DISABLE KEYS */;
/*!40000 ALTER TABLE "detalleVentas" ENABLE KEYS */;

-- Volcando estructura para tabla public.empleados
CREATE TABLE IF NOT EXISTS "empleados" (
	"id" INTEGER NOT NULL,
	"legajo" VARCHAR(50) NOT NULL,
	"usuario" VARCHAR(50) NOT NULL,
	"contraseña" VARCHAR(100) NOT NULL,
	"rol" VARCHAR(50) NOT NULL,
	PRIMARY KEY ("id"),
	UNIQUE "empleados_legajo_key" ("legajo"),
	UNIQUE "ix_empleados_usuario" ("usuario"),
	CONSTRAINT "empleados_id_fkey" FOREIGN KEY ("id") REFERENCES "personas" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.empleados: -1 rows
/*!40000 ALTER TABLE "empleados" DISABLE KEYS */;
INSERT INTO "empleados" ("id", "legajo", "usuario", "contraseña", "rol") VALUES
	(1, 'TEC-001', 'liotect', 'password123', 'tecnico'),
	(36, 'VED-456', 'LM22', 'password22', 'vendedor'),
	(3, 'MED-789', 'AVargas45', 'password89', 'medico'),
	(39, 'TEC001', 'maria_tec', 'pass456', 'tecnico'),
	(41, 'MED1781681929', 'carlos_med1781681929', 'pass123', 'medico'),
	(43, 'MED1781682104', 'carlos_med1781682104', 'pass123', 'medico'),
	(45, 'MED1781682162', 'carlos_med1781682162', 'pass123', 'medico');
/*!40000 ALTER TABLE "empleados" ENABLE KEYS */;

-- Volcando estructura para tabla public.etapas_trabajo
CREATE TABLE IF NOT EXISTS "etapas_trabajo" (
	"id" SERIAL NOT NULL,
	"orden_id" INTEGER NOT NULL,
	"etapa" VARCHAR(50) NOT NULL,
	"tecnico_id" INTEGER NULL DEFAULT NULL,
	"completado" BOOLEAN NOT NULL DEFAULT false,
	"notas" TEXT NULL DEFAULT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "etapas_trabajo_orden_id_fkey" FOREIGN KEY ("orden_id") REFERENCES "ordenes_trabajo" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "etapas_trabajo_tecnico_id_fkey" FOREIGN KEY ("tecnico_id") REFERENCES "tecnicos" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.etapas_trabajo: -1 rows
/*!40000 ALTER TABLE "etapas_trabajo" DISABLE KEYS */;
/*!40000 ALTER TABLE "etapas_trabajo" ENABLE KEYS */;

-- Volcando estructura para tabla public.historico_estados
CREATE TABLE IF NOT EXISTS "historico_estados" (
	"id" SERIAL NOT NULL,
	"orden_id" INTEGER NOT NULL,
	"estado_anterior" VARCHAR(50) NULL DEFAULT NULL,
	"estado_nuevo" VARCHAR(50) NOT NULL,
	"tecnico_id" INTEGER NULL DEFAULT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "historico_estados_orden_id_fkey" FOREIGN KEY ("orden_id") REFERENCES "ordenes_trabajo" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "historico_estados_tecnico_id_fkey" FOREIGN KEY ("tecnico_id") REFERENCES "tecnicos" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.historico_estados: -1 rows
/*!40000 ALTER TABLE "historico_estados" DISABLE KEYS */;
/*!40000 ALTER TABLE "historico_estados" ENABLE KEYS */;

-- Volcando estructura para tabla public.medicos
CREATE TABLE IF NOT EXISTS "medicos" (
	"id" INTEGER NOT NULL,
	"matricula" VARCHAR(50) NOT NULL,
	"especialidad" VARCHAR(100) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "medicos_id_fkey" FOREIGN KEY ("id") REFERENCES "empleados" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.medicos: -1 rows
/*!40000 ALTER TABLE "medicos" DISABLE KEYS */;
INSERT INTO "medicos" ("id", "matricula", "especialidad") VALUES
	(41, 'MAT1781681929', 'Oftalmologia'),
	(43, 'MAT1781682104', 'Oftalmologia'),
	(45, 'MAT1781682162', 'Oftalmologia');
/*!40000 ALTER TABLE "medicos" ENABLE KEYS */;

-- Volcando estructura para tabla public.ordenes_trabajo
CREATE TABLE IF NOT EXISTS "ordenes_trabajo" (
	"id" SERIAL NOT NULL,
	"venta_id" INTEGER NOT NULL,
	"estado" VARCHAR(50) NOT NULL DEFAULT 'recibida',
	"descripcion_trabajo" TEXT NULL DEFAULT NULL,
	"fecha_entrega_esperada" TIMESTAMP NULL DEFAULT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	UNIQUE "ordenes_trabajo_venta_id_key" ("venta_id"),
	CONSTRAINT "ordenes_trabajo_venta_id_fkey" FOREIGN KEY ("venta_id") REFERENCES "ventas" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.ordenes_trabajo: -1 rows
/*!40000 ALTER TABLE "ordenes_trabajo" DISABLE KEYS */;
/*!40000 ALTER TABLE "ordenes_trabajo" ENABLE KEYS */;

-- Volcando estructura para tabla public.pacientes
CREATE TABLE IF NOT EXISTS "pacientes" (
	"id" INTEGER NOT NULL,
	"obra_social" VARCHAR(100) NULL DEFAULT NULL,
	"historial_medico" VARCHAR(500) NULL DEFAULT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "pacientes_id_fkey" FOREIGN KEY ("id") REFERENCES "personas" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.pacientes: -1 rows
/*!40000 ALTER TABLE "pacientes" DISABLE KEYS */;
INSERT INTO "pacientes" ("id", "obra_social", "historial_medico") VALUES
	(38, 'Relojeros', 'Fondo de ojos'),
	(2, 'Relojeros', 'Rayos X'),
	(46, 'Osrja Relojeros', 'Consulta medica'),
	(47, 'Perfumistas', 'Fondo de ojos');
/*!40000 ALTER TABLE "pacientes" ENABLE KEYS */;

-- Volcando estructura para tabla public.personas
CREATE TABLE IF NOT EXISTS "personas" (
	"id" SERIAL NOT NULL,
	"dni" VARCHAR(20) NOT NULL,
	"nombre" VARCHAR(100) NOT NULL,
	"apellido" VARCHAR(100) NOT NULL,
	"telefono" VARCHAR(50) NULL DEFAULT NULL,
	"email" VARCHAR(100) NULL DEFAULT NULL,
	"tipo_persona" VARCHAR(50) NOT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	UNIQUE "ix_personas_dni" ("dni"),
	KEY "ix_personas_id" ("id")
);

-- Volcando datos para la tabla public.personas: -1 rows
/*!40000 ALTER TABLE "personas" DISABLE KEYS */;
INSERT INTO "personas" ("id", "dni", "nombre", "apellido", "telefono", "email", "tipo_persona", "fecha_creacion", "fecha_actualizacion") VALUES
	(1, '12345678', 'Lionel', 'Messi', '1122334455', 'lio@optica.com', 'tecnico', '2026-06-04 02:39:43.433182-03', '2026-06-04 02:39:43.433182-03'),
	(36, '78923123', 'Lautaro', 'Martinez', '1123456789', 'LMartinez@example.com', 'vendedor', '2026-06-09 02:38:16.595987-03', '2026-06-09 02:38:16.595987-03'),
	(3, '23564789', 'Andres', 'Vargas', '1145123698', 'Vandres@example.com', 'tecnico', '2026-06-09 02:11:37.807908-03', '2026-06-09 03:30:42.12222-03'),
	(38, '23569781', 'Thiago', 'Messi', '1123458971', 'ThgMessi@test.com', 'paciente', '2026-06-09 04:00:23.463508-03', '2026-06-09 04:00:23.463508-03'),
	(2, '22333888', 'Leo', 'Vargas', '1145897823', 'Leo@test.com', 'paciente', '2026-06-09 01:58:30.105633-03', '2026-06-09 04:01:55.981122-03'),
	(39, '87654321', 'Maria', 'Garcia', '0987654321', 'maria@example.com', 'tecnico', '2026-06-17 04:37:33.468981-03', '2026-06-17 04:37:33.468981-03'),
	(41, '99681929', 'Carlos', 'Lopez', '5555555555', 'updated1781681929@example.com', 'medico', '2026-06-17 04:38:49.937215-03', '2026-06-17 04:38:49.992134-03'),
	(43, '99682104', 'Carlos', 'Lopez', '5555555555', 'updated1781682104@example.com', 'medico', '2026-06-17 04:41:44.495422-03', '2026-06-17 04:41:44.56967-03'),
	(46, '88682162', 'Juan', 'Perez', '1111111111', 'juan1781682162@example.com', 'paciente', '2026-06-17 04:42:42.096808-03', '2026-06-17 04:42:42.096808-03'),
	(45, '99682162', 'Carlos', 'Lopez', '5555555555', 'updated1781682162@example.com', 'medico', '2026-06-17 04:42:42.08041-03', '2026-06-17 04:42:42.157581-03'),
	(47, '45556987', 'Mario', 'Castañeda', '1123235689', 'mario@example.com', 'paciente', '2026-06-18 03:27:07.718647-03', '2026-06-18 03:27:07.718647-03');
/*!40000 ALTER TABLE "personas" ENABLE KEYS */;

-- Volcando estructura para tabla public.productos
CREATE TABLE IF NOT EXISTS "productos" (
	"id" SERIAL NOT NULL,
	"sku" VARCHAR(50) NOT NULL,
	"tipoNombre" VARCHAR(100) NOT NULL,
	"precio" DOUBLE PRECISION NOT NULL,
	"stockDisponible" INTEGER NOT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	UNIQUE "productos_sku_key" ("sku")
);

-- Volcando datos para la tabla public.productos: -1 rows
/*!40000 ALTER TABLE "productos" DISABLE KEYS */;
INSERT INTO "productos" ("id", "sku", "tipoNombre", "precio", "stockDisponible", "fecha_creacion", "fecha_actualizacion") VALUES
	(1, 'RX7207L 8302 55', 'Ray-Ban', 200000, 3, '2026-06-17 05:35:02.622714-03', '2026-06-17 05:35:02.622714-03');
/*!40000 ALTER TABLE "productos" ENABLE KEYS */;

-- Volcando estructura para tabla public.recetas
CREATE TABLE IF NOT EXISTS "recetas" (
	"uuid" SERIAL NOT NULL,
	"turno_id" INTEGER NOT NULL,
	"paciente_id" INTEGER NOT NULL,
	"medico_id" INTEGER NOT NULL,
	"fecha_emision" TIMESTAMP NOT NULL,
	"fecha_vencimiento" TIMESTAMP NOT NULL,
	"od_esfera" DOUBLE PRECISION NULL DEFAULT NULL,
	"od_cilindro" DOUBLE PRECISION NULL DEFAULT NULL,
	"od_eje" INTEGER NULL DEFAULT NULL,
	"od_adicion" DOUBLE PRECISION NULL DEFAULT NULL,
	"oi_esfera" DOUBLE PRECISION NULL DEFAULT NULL,
	"oi_cilindro" DOUBLE PRECISION NULL DEFAULT NULL,
	"oi_eje" INTEGER NULL DEFAULT NULL,
	"oi_adicion" DOUBLE PRECISION NULL DEFAULT NULL,
	"distancia_pupilar" DOUBLE PRECISION NULL DEFAULT NULL,
	"tipo_lente" VARCHAR(50) NULL DEFAULT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("uuid"),
	CONSTRAINT "recetas_medico_id_fkey" FOREIGN KEY ("medico_id") REFERENCES "medicos" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "recetas_paciente_id_fkey" FOREIGN KEY ("paciente_id") REFERENCES "pacientes" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "recetas_turno_id_fkey" FOREIGN KEY ("turno_id") REFERENCES "turnos" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.recetas: -1 rows
/*!40000 ALTER TABLE "recetas" DISABLE KEYS */;
INSERT INTO "recetas" ("uuid", "turno_id", "paciente_id", "medico_id", "fecha_emision", "fecha_vencimiento", "od_esfera", "od_cilindro", "od_eje", "od_adicion", "oi_esfera", "oi_cilindro", "oi_eje", "oi_adicion", "distancia_pupilar", "tipo_lente", "fecha_creacion", "fecha_actualizacion") VALUES
	(3, 1, 46, 45, '2026-06-17 04:42:42.174337', '2027-06-17 04:42:42.167203', -1.5, -0.5, 90, 0, -2, 0, 180, 0, 62, 'Monofocal', '2026-06-17 04:42:42.16921-03', '2026-06-17 04:42:42.16921-03');
/*!40000 ALTER TABLE "recetas" ENABLE KEYS */;

-- Volcando estructura para tabla public.tecnicos
CREATE TABLE IF NOT EXISTS "tecnicos" (
	"id" INTEGER NOT NULL,
	"matricula_optico" VARCHAR(50) NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "tecnicos_id_fkey" FOREIGN KEY ("id") REFERENCES "empleados" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.tecnicos: -1 rows
/*!40000 ALTER TABLE "tecnicos" DISABLE KEYS */;
INSERT INTO "tecnicos" ("id", "matricula_optico") VALUES
	(1, 'MAT-10'),
	(3, 'MAT-89'),
	(39, 'OP001');
/*!40000 ALTER TABLE "tecnicos" ENABLE KEYS */;

-- Volcando estructura para tabla public.turnos
CREATE TABLE IF NOT EXISTS "turnos" (
	"id" SERIAL NOT NULL,
	"fecha_hora" TIMESTAMP NOT NULL,
	"motivo" VARCHAR(255) NOT NULL,
	"estado" VARCHAR(50) NOT NULL,
	"paciente_id" INTEGER NOT NULL,
	"medico_id" INTEGER NOT NULL,
	"fecha_creacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	CONSTRAINT "turnos_medico_id_fkey" FOREIGN KEY ("medico_id") REFERENCES "medicos" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "turnos_paciente_id_fkey" FOREIGN KEY ("paciente_id") REFERENCES "pacientes" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.turnos: -1 rows
/*!40000 ALTER TABLE "turnos" DISABLE KEYS */;
INSERT INTO "turnos" ("id", "fecha_hora", "motivo", "estado", "paciente_id", "medico_id", "fecha_creacion", "fecha_actualizacion") VALUES
	(1, '2026-06-18 04:42:42.10654', 'Examen de oftalmologia', 'pendiente', 46, 45, '2026-06-17 04:42:42.108975-03', '2026-06-17 04:42:42.108975-03');
/*!40000 ALTER TABLE "turnos" ENABLE KEYS */;

-- Volcando estructura para tabla public.vendedores
CREATE TABLE IF NOT EXISTS "vendedores" (
	"id" INTEGER NOT NULL,
	"comisiones" DOUBLE PRECISION NOT NULL,
	PRIMARY KEY ("id"),
	CONSTRAINT "vendedores_id_fkey" FOREIGN KEY ("id") REFERENCES "empleados" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.vendedores: -1 rows
/*!40000 ALTER TABLE "vendedores" DISABLE KEYS */;
INSERT INTO "vendedores" ("id", "comisiones") VALUES
	(36, 0);
/*!40000 ALTER TABLE "vendedores" ENABLE KEYS */;

-- Volcando estructura para tabla public.ventas
CREATE TABLE IF NOT EXISTS "ventas" (
	"id" SERIAL NOT NULL,
	"numeroComprobante" VARCHAR(50) NOT NULL,
	"fecha_creacion" TIMESTAMP NOT NULL,
	"estado_pago" VARCHAR(50) NOT NULL,
	"total" DOUBLE PRECISION NOT NULL,
	"paciente_id" INTEGER NOT NULL,
	"vendedor_id" INTEGER NOT NULL,
	"receta_id" INTEGER NULL DEFAULT NULL,
	"fecha_actualizacion" TIMESTAMPTZ NOT NULL DEFAULT now(),
	PRIMARY KEY ("id"),
	UNIQUE "ventas_numeroComprobante_key" ("numeroComprobante"),
	CONSTRAINT "ventas_paciente_id_fkey" FOREIGN KEY ("paciente_id") REFERENCES "pacientes" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "ventas_receta_id_fkey" FOREIGN KEY ("receta_id") REFERENCES "recetas" ("uuid") ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT "ventas_vendedor_id_fkey" FOREIGN KEY ("vendedor_id") REFERENCES "vendedores" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Volcando datos para la tabla public.ventas: -1 rows
/*!40000 ALTER TABLE "ventas" DISABLE KEYS */;
/*!40000 ALTER TABLE "ventas" ENABLE KEYS */;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
