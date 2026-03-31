# Sistema de Cafetería — Fase 1

> **Proyecto Integrador** · Programación Orientada a Objetos · Principios SOLID · Patrones de Diseño

---

## Descripción

Sistema de gestión para una cafetería implementado en **Python**, que modela productos, pedidos, clientes, empleados, inventario y pagos. El diseño aplica programación orientada a objetos, los principios **SOLID** y cuatro patrones de diseño.

---

## Estructura del Proyecto

```
proyecto_fase1_sistema_de-cafeteria-/
├── diagrama_clases.puml          # Diagrama de clases PlantUML
├── main.py                       # Demo completa del sistema
├── src/
│   ├── modelos/
│   │   ├── producto.py           # IProducto, Producto, Bebida, Comida, Postre
│   │   ├── pedido.py             # EstadoPedido, ItemPedido, Pedido
│   │   ├── cliente.py            # Cliente
│   │   ├── empleado.py           # Empleado (abstract), Cajero, Cocinero
│   │   └── menu.py               # Menu
│   ├── patrones/
│   │   ├── observador.py         # Patrón Observer
│   │   ├── fabrica.py            # Patrón Factory Method
│   │   └── estrategia_pago.py   # Patrón Strategy
│   ├── inventario.py             # Inventario (Singleton)
│   └── sistema_cafeteria.py     # SistemaCafeteria (Singleton)
└── tests/
    └── test_sistema.py           # 56 pruebas unitarias (pytest)
```

---

## Diagrama de Clases (PlantUML)

El archivo [`diagrama_clases.puml`](diagrama_clases.puml) contiene el diagrama de clases completo en formato **PlantUML**.

Para visualizarlo puedes:

- Usar la extensión **PlantUML** en VS Code.
- Pegarlo en [https://www.plantuml.com/plantuml/uml/](https://www.plantuml.com/plantuml/uml/).
- Ejecutar `plantuml diagrama_clases.puml` si tienes PlantUML instalado.

---

## Programación Orientada a Objetos

| Elemento OOP        | Implementación                                                             |
|---------------------|----------------------------------------------------------------------------|
| **Abstracción**     | `IProducto`, `IObservador`, `IFabricaProducto`, `IEstrategiaPago`         |
| **Encapsulamiento** | Atributos protegidos (`_nombre`, `_precio`, …) expuestos con `@property`  |
| **Herencia**        | `Bebida`, `Comida`, `Postre` → `Producto`; `Cajero`, `Cocinero` → `Empleado` |
| **Polimorfismo**    | Todos los productos implementan `obtener_categoria()`; todas las estrategias implementan `procesar_pago()` |
| **Interfaces**      | Clases abstractas (`ABC`) usadas como contratos explícitos                 |

---

## Principios SOLID

| Principio                    | Aplicación                                                                        |
|------------------------------|-----------------------------------------------------------------------------------|
| **S** — Single Responsibility | Cada clase tiene una única razón para cambiar (`Pedido`, `Menu`, `Inventario`, …) |
| **O** — Open / Closed         | Nuevas categorías de producto o métodos de pago sin modificar clases existentes   |
| **L** — Liskov Substitution   | `Bebida`, `Comida` y `Postre` sustituyen a `Producto` sin romper el contrato      |
| **I** — Interface Segregation | Interfaces pequeñas y enfocadas (`IObservador`, `IFabricaProducto`, …)            |
| **D** — Dependency Inversion  | `SistemaCafeteria` depende de abstracciones, no de clases concretas               |

---

## Patrones de Diseño

### 1. Singleton
> **Clases:** `SistemaCafeteria`, `Inventario`

Garantiza que exista **una única instancia** del sistema de cafetería y del inventario en toda la aplicación. Se implementa sobreescribiendo `__new__` para retornar siempre la misma instancia.

```python
sistema_a = SistemaCafeteria()
sistema_b = SistemaCafeteria()
assert sistema_a is sistema_b  # True
```

### 2. Factory Method
> **Clases:** `IFabricaProducto`, `FabricaBebida`, `FabricaComida`, `FabricaPostre`

Define una interfaz para crear productos y delega a las subclases la instanciación del tipo concreto. El sistema registra productos sin conocer la clase concreta.

```python
sistema.registrar_producto("bebida", "Café", 25.0, "Café negro", temperatura="caliente")
sistema.registrar_producto("comida", "Torta", 45.0, "Torta de jamón", calorias=520)
```

### 3. Observer
> **Clases:** `IObservador`, `SujetoObservable`, `ObservadorCajero`, `ObservadorCocinero`

Permite que cajeros y cocineros se suscriban a los cambios de estado de los pedidos y reciban notificaciones automáticas.

```python
sistema.registrar_observador(ObservadorCajero("Ana"))
sistema.registrar_observador(ObservadorCocinero("Luis"))
sistema.actualizar_estado_pedido(pedido, EstadoPedido.LISTO)
# → [Cajero Ana] Pedido #1 → Estado: LISTO
# → [Cocinero Luis] Pedido #1 → Estado: LISTO
```

### 4. Strategy
> **Clases:** `IEstrategiaPago`, `PagoEfectivo`, `PagoTarjeta`, `PagoDigital`, `ContextoPago`

Encapsula los distintos algoritmos de pago y los hace intercambiables en tiempo de ejecución sin modificar el código cliente.

```python
sistema.procesar_pago(pedido, PagoEfectivo(100.0))
sistema.procesar_pago(pedido, PagoTarjeta("4111111111111234", "crédito"))
sistema.procesar_pago(pedido, PagoDigital("user@mail.com", "MercadoPago"))
```

---

## Ejecución

```bash
# Instalar dependencias de pruebas
pip install pytest

# Ejecutar la demo
python main.py

# Ejecutar pruebas unitarias (56 tests)
python -m pytest tests/ -v
```

---

## Pruebas

56 pruebas unitarias organizadas en:

- `TestProducto` — validación de modelos y herencia
- `TestCliente`, `TestEmpleado`, `TestMenu`, `TestPedido`
- `TestSingleton` — instancia única
- `TestFactoryMethod` — creación correcta de productos
- `TestObserver` — notificaciones de cambio de estado
- `TestStrategy` — cálculo de pagos y cambio de estrategia
- `TestInventario` — control de stock
- `TestSistemaCafeteria` — flujo integrado end-to-end

