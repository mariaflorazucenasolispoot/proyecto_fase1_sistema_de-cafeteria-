"""
Módulo de pedidos del sistema de cafetería.

Principios SOLID aplicados:
- S (Single Responsibility): Pedido gestiona el estado/items; ItemPedido encapsula cantidad+producto.
- O (Open/Closed): EstadoPedido se puede extender sin modificar Pedido.
"""

from enum import Enum, auto
from typing import List

from src.modelos.producto import IProducto


class EstadoPedido(Enum):
    """Posibles estados por los que pasa un pedido."""

    PENDIENTE = auto()
    EN_PREPARACION = auto()
    LISTO = auto()
    ENTREGADO = auto()
    CANCELADO = auto()


class ItemPedido:
    """
    Representa un ítem dentro de un pedido.

    Asocia un producto con la cantidad solicitada y calcula el subtotal.
    """

    def __init__(self, producto: IProducto, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")
        self._producto = producto
        self._cantidad = cantidad

    @property
    def producto(self) -> IProducto:
        return self._producto

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def subtotal(self) -> float:
        return self._producto.precio * self._cantidad

    def __str__(self) -> str:
        return f"{self._cantidad}x {self._producto.nombre} = ${self.subtotal:.2f}"

    def __repr__(self) -> str:
        return (
            f"ItemPedido(producto={self._producto!r}, cantidad={self._cantidad})"
        )


class Pedido:
    """
    Representa un pedido realizado en la cafetería.

    Gestiona los ítems, el estado del pedido y el total a cobrar.
    Notifica a los observadores registrados cada vez que cambia su estado
    (patrón Observer delegado al sistema de cafetería).
    """

    _siguiente_id: int = 1

    def __init__(self, cliente_nombre: str) -> None:
        self._id = Pedido._siguiente_id
        Pedido._siguiente_id += 1
        self._cliente_nombre = cliente_nombre
        self._items: List[ItemPedido] = []
        self._estado = EstadoPedido.PENDIENTE
        self._observadores: list = []

    @property
    def pedido_id(self) -> int:
        return self._id

    @property
    def cliente_nombre(self) -> str:
        return self._cliente_nombre

    @property
    def estado(self) -> EstadoPedido:
        return self._estado

    @property
    def items(self) -> List[ItemPedido]:
        return list(self._items)

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self._items)

    def agregar_item(self, item: ItemPedido) -> None:
        """Agrega un ítem al pedido (solo si está PENDIENTE)."""
        if self._estado != EstadoPedido.PENDIENTE:
            raise RuntimeError("No se pueden agregar ítems a un pedido que ya no está pendiente.")
        self._items.append(item)

    def suscribir_observador(self, observador) -> None:
        """Registra un observador para notificaciones de cambio de estado."""
        self._observadores.append(observador)

    def cambiar_estado(self, nuevo_estado: EstadoPedido) -> None:
        """Actualiza el estado y notifica a todos los observadores."""
        self._estado = nuevo_estado
        self._notificar_observadores()

    def _notificar_observadores(self) -> None:
        for obs in self._observadores:
            obs.actualizar(self)

    def __str__(self) -> str:
        lineas = [f"Pedido #{self._id} ({self._cliente_nombre}) - {self._estado.name}"]
        for item in self._items:
            lineas.append(f"  {item}")
        lineas.append(f"  Total: ${self.total:.2f}")
        return "\n".join(lineas)

    def __repr__(self) -> str:
        return f"Pedido(id={self._id}, cliente={self._cliente_nombre!r}, estado={self._estado})"
