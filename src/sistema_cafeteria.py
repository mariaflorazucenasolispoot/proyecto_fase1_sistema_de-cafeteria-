"""
Módulo principal del sistema de cafetería.

Patrón de diseño: Singleton
============================
SistemaCafeteria es el punto de entrada único de la aplicación. Coordina
el menú, el inventario, los pedidos y las notificaciones a los empleados.

Principios SOLID aplicados:
- S (Single Responsibility): SistemaCafeteria orquesta la lógica de negocio de alto nivel.
- D (Dependency Inversion): Depende de abstracciones (IObservador, IFabricaProducto, etc.).
"""

from typing import Dict, List

from src.inventario import Inventario
from src.modelos.menu import Menu
from src.modelos.pedido import EstadoPedido, ItemPedido, Pedido
from src.modelos.producto import IProducto
from src.patrones.estrategia_pago import ContextoPago, IEstrategiaPago
from src.patrones.fabrica import IFabricaProducto, obtener_fabrica
from src.patrones.observador import IObservador, SujetoObservable


class SistemaCafeteria(SujetoObservable):
    """
    Núcleo del sistema de cafetería.

    Implementa Singleton para garantizar una instancia única y
    hereda de SujetoObservable para gestionar las notificaciones
    a cajeros y cocineros (patrón Observer).
    """

    _instancia: "SistemaCafeteria | None" = None

    def __new__(cls) -> "SistemaCafeteria":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            # Inicialización única de atributos de instancia
            cls._instancia.__inicializar()
        return cls._instancia

    def __inicializar(self) -> None:
        """Inicializa los componentes internos del sistema (llamado una sola vez)."""
        SujetoObservable.__init__(self)
        self._menu = Menu()
        self._inventario = Inventario()
        self._pedidos: Dict[int, Pedido] = {}

    @classmethod
    def resetear(cls) -> None:
        """Reinicia el singleton (útil para pruebas unitarias)."""
        cls._instancia = None
        Inventario.resetear()

    # ------------------------------------------------------------------
    # Gestión del menú
    # ------------------------------------------------------------------

    @property
    def menu(self) -> Menu:
        return self._menu

    def registrar_producto(
        self, categoria: str, nombre: str, precio: float, descripcion: str, **kwargs
    ) -> IProducto:
        """
        Crea un producto mediante la fábrica correspondiente y lo agrega al menú.

        Usa el patrón Factory Method internamente.
        """
        fabrica: IFabricaProducto = obtener_fabrica(categoria)
        producto = fabrica.crear_producto(nombre, precio, descripcion, **kwargs)
        self._menu.agregar_producto(producto)
        return producto

    # ------------------------------------------------------------------
    # Gestión del inventario
    # ------------------------------------------------------------------

    @property
    def inventario(self) -> Inventario:
        return self._inventario

    def abastecer(self, producto: IProducto, cantidad: int) -> None:
        """Incrementa el stock del producto en el inventario."""
        self._inventario.agregar_stock(producto, cantidad)

    # ------------------------------------------------------------------
    # Gestión de pedidos
    # ------------------------------------------------------------------

    def crear_pedido(self, cliente_nombre: str) -> Pedido:
        """Crea un nuevo pedido para el cliente indicado."""
        pedido = Pedido(cliente_nombre)
        self._pedidos[pedido.pedido_id] = pedido
        return pedido

    def agregar_item_a_pedido(
        self, pedido: Pedido, nombre_producto: str, cantidad: int
    ) -> None:
        """
        Agrega un ítem al pedido verificando disponibilidad en inventario.

        Raises:
            ValueError: si no hay stock suficiente.
        """
        producto = self._menu.obtener_producto(nombre_producto)
        if not self._inventario.hay_disponibilidad(producto, cantidad):
            raise ValueError(
                f"Stock insuficiente para '{nombre_producto}'."
            )
        self._inventario.reducir_stock(producto, cantidad)
        pedido.agregar_item(ItemPedido(producto, cantidad))

    def actualizar_estado_pedido(
        self, pedido: Pedido, nuevo_estado: EstadoPedido
    ) -> None:
        """Cambia el estado del pedido y notifica a los observadores globales."""
        pedido.cambiar_estado(nuevo_estado)
        self.notificar(pedido)

    def obtener_pedido(self, pedido_id: int) -> Pedido:
        """Retorna el pedido con el ID indicado."""
        if pedido_id not in self._pedidos:
            raise KeyError(f"No existe el pedido #{pedido_id}.")
        return self._pedidos[pedido_id]

    def listar_pedidos(self) -> List[Pedido]:
        """Retorna todos los pedidos registrados en el sistema."""
        return list(self._pedidos.values())

    # ------------------------------------------------------------------
    # Gestión de pagos
    # ------------------------------------------------------------------

    def procesar_pago(self, pedido: Pedido, estrategia: IEstrategiaPago) -> str:
        """
        Procesa el pago de un pedido usando la estrategia indicada (patrón Strategy).

        Raises:
            RuntimeError: si el pedido ya fue entregado o cancelado.
            ValueError: si el total del pedido es cero o negativo.
        """
        if pedido.estado in (EstadoPedido.ENTREGADO, EstadoPedido.CANCELADO):
            raise RuntimeError(
                f"El pedido #{pedido.pedido_id} ya está {pedido.estado.name}."
            )
        contexto = ContextoPago(estrategia)
        resultado = contexto.ejecutar_pago(pedido.total)
        self.actualizar_estado_pedido(pedido, EstadoPedido.ENTREGADO)
        return resultado

    # ------------------------------------------------------------------
    # Gestión de observadores
    # ------------------------------------------------------------------

    def registrar_observador(self, observador: IObservador) -> None:
        """Registra un observador global (cajero, cocinero, etc.)."""
        self.suscribir(observador)

    def eliminar_observador(self, observador: IObservador) -> None:
        """Elimina un observador global."""
        self.desuscribir(observador)
