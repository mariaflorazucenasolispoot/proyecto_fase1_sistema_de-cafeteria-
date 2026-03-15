"""
Patrón de diseño: Observer (Observador)
=======================================
Permite que los objetos (observadores) se suscriban a eventos emitidos por
un sujeto y reciban notificaciones automáticas al cambiar el estado.

Clases:
- IObservador: interfaz que deben implementar todos los observadores.
- SujetoObservable: mixin que añade la capacidad de gestionar observadores.
- ObservadorCajero: observador concreto para el personal de caja.
- ObservadorCocinero: observador concreto para el personal de cocina.

Principios SOLID aplicados:
- I (Interface Segregation): IObservador define sólo el método actualizar().
- D (Dependency Inversion): SujetoObservable depende de IObservador, no de clases concretas.
"""

from abc import ABC, abstractmethod
from typing import List


class IObservador(ABC):
    """Interfaz que deben implementar todos los observadores del sistema."""

    @abstractmethod
    def actualizar(self, pedido) -> None:
        """Recibe la notificación de cambio de estado de un pedido."""


class SujetoObservable:
    """
    Mixin que provee gestión de observadores.

    Las clases que hereden de SujetoObservable pueden notificar
    cambios de estado a sus observadores registrados.
    """

    def __init__(self) -> None:
        self._observadores: List[IObservador] = []

    def suscribir(self, observador: IObservador) -> None:
        """Registra un nuevo observador."""
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador: IObservador) -> None:
        """Elimina un observador registrado."""
        self._observadores = [o for o in self._observadores if o is not observador]

    def notificar(self, pedido) -> None:
        """Notifica a todos los observadores sobre un cambio de estado."""
        for observador in self._observadores:
            observador.actualizar(pedido)


class ObservadorCajero(IObservador):
    """
    Observador concreto que representa al personal de caja.

    Recibe notificaciones cuando un pedido cambia de estado, por ejemplo
    cuando está listo para entregar al cliente.
    """

    def __init__(self, nombre_cajero: str) -> None:
        self._nombre = nombre_cajero

    @property
    def nombre(self) -> str:
        return self._nombre

    def actualizar(self, pedido) -> None:
        """Procesa la notificación recibida del sujeto."""
        print(
            f"[Cajero {self._nombre}] Pedido #{pedido.pedido_id} "
            f"({pedido.cliente_nombre}) → Estado: {pedido.estado.name}"
        )


class ObservadorCocinero(IObservador):
    """
    Observador concreto que representa al personal de cocina.

    Recibe notificaciones cuando hay un nuevo pedido pendiente de preparar.
    """

    def __init__(self, nombre_cocinero: str) -> None:
        self._nombre = nombre_cocinero

    @property
    def nombre(self) -> str:
        return self._nombre

    def actualizar(self, pedido) -> None:
        """Procesa la notificación recibida del sujeto."""
        print(
            f"[Cocinero {self._nombre}] Pedido #{pedido.pedido_id} "
            f"para {pedido.cliente_nombre!r} → Estado: {pedido.estado.name}"
        )
