# Arquitectura y Patrones - Proyecto Visualion_Opt

## Patrones de Diseño por Módulo

### Módulo de Salud (Oftalmología)
**Patrón: Validator**
- Encargado de la lógica de las dioptrías
- Asegura que el médico no ingrese valores imposibles
- Ejemplo: Validar que el Eje no sea mayor a 180°

### Módulo de Taller y Laboratorio
**Patrón: State Pattern (Máquina de Estados)**
- Controla el flujo de estados de las órdenes de trabajo
- Restricción: Una orden no puede pasar a "Listo" si no pasó por "Control de Calidad"
- Estados esperados: Recibida → Biselado → Montaje → Control de Calidad → Listo

### Módulo de Inventario
**Patrón: DTO (Data Transfer Objects)**
- Protección de datos: Solo se envía la información necesaria del producto al vendedor
- Previene exposición innecesaria de datos internos

