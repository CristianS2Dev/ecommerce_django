> [!TIP]
> ### Cómo llenar el *CHANGELOG*
> El CHANGELOG.md debe registrar los cambios realizados en el proyecto de forma clara y estructurada. Usa este formato para mantener el orden:
> ## [Versión] - Fecha
> ### Added
> - Descripción de nuevas funcionalidades o recursos añadidos.
> ### Fixed
> - Descripción de errores solucionados.
> ### Changed
> - Descripción de cambios en funcionalidades existentes.
> ### Removed
> - Descripción de funcionalidades o recursos eliminados.
> ### Note
> - Notas adicionales sobre los cambios realizados.
---

# CHANGELOG

## [v3.0.0] - 17-04-2025

### Added

- Nueva estructura de carpetas optimizada para una mejor organización del código.
- Se reestructura el proyecto para facilitar el mantenimiento y la escalabilidad.
- Se migran las funcionalidades existentes desde el proyecto anterior.
- Se documentan mejor los componentes del sistema.
- Se agrega una separación clara entre módulos como productos, usuarios, carrito, y direcciones.
- Se implementa nuevamente el filtrado de productos por nombre, categoría y marca en `mis_productos.html`.

### Changed

- Se refactoriza el código de vistas y modelos para adaptarlos a la nueva estructura.
- Se mejora la legibilidad y organización del frontend (templates y archivos estáticos).
- Se actualizan las rutas y nombres de archivos para mayor coherencia.
- Se actualizan las funciones relacionadas con productos (agregar, editar, eliminar) según la nueva estructura modular.

### Removed

- Se eliminan archivos y templates no utilizados durante la migración.
- Se eliminan funciones duplicadas o que ya no eran necesarias tras la reestructuración.


### Note

- Validar las funcionalidades de detalle de productos y carrito de compras tras la migración.