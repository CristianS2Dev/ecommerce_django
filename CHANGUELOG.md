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

---

## [v3.2.1-alpha.1] - 17-04-2025

### Added

- Se mejoran las opciones de filtrado en el listado de productos (categoría, precio, marca, color).

### Changed

- Se refactorizan los templates para mejorar el diseño y la integración de la barra lateral.
- Se actualizan las vistas de gestión de productos y variantes para una mejor experiencia de usuario.
- Se ajusta el comportamiento del modal de inicio de sesión para un manejo adecuado de la sesión.

### Fixed

- Se modifica el campo `imagen_perfil` en el modelo `usuario` para permitir valores nulos y establecer una ruta de imagen por defecto.

---

## [v3.1.1-alpha.1] - 17-04-2025

### Added

- Se implementan vistas y URLs para gestionar variantes de productos (añadir, editar, eliminar).
- Se agrega paginación a la vista de listado de productos e integración de opciones de filtrado (categoría, precio, marca, color).
- Se mejora la vista de detalle de productos para mostrar variantes disponibles y su stock.
- Se actualiza el carrito de compras para asociar los artículos con variantes específicas.
- Se añaden estilos CSS para colores y tallas seleccionados.

### Changed

- Se actualizan las vistas de gestión de productos para manejar variantes durante la creación y edición de productos.
- Se mejora la interfaz de usuario para la selección de colores y tallas en las páginas de detalle de productos.
- Se refactorizan los templates para optimizar las vistas de listado y detalle de productos.
- Se actualizan los templates de navegación e índice para mejorar la experiencia del usuario.

---

## [v3.0.0-alpha.1] - 17-04-2025

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
