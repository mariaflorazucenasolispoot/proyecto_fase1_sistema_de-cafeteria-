"""
Módulo de cliente del sistema de cafetería.

Principios SOLID aplicados:
- S (Single Responsibility): Cliente sólo gestiona los datos del cliente.
"""


class Cliente:
    """
    Representa a un cliente de la cafetería.

    Almacena información personal y el historial de pedidos realizados.
    """

    def __init__(self, nombre: str, correo: str) -> None:
        self._nombre = nombre
        self._correo = correo
        self._historial_pedidos: list = []

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    @property
    def historial_pedidos(self) -> list:
        return list(self._historial_pedidos)

    def agregar_pedido(self, pedido) -> None:
        """Agrega un pedido al historial del cliente."""
        self._historial_pedidos.append(pedido)

    def __str__(self) -> str:
        return f"Cliente({self._nombre}, {self._correo})"

    def __repr__(self) -> str:
        return f"Cliente(nombre={self._nombre!r}, correo={self._correo!r})"
