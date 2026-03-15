"""
Módulo de empleados del sistema de cafetería.

Principios SOLID aplicados:
- S (Single Responsibility): Cada tipo de empleado tiene su propia responsabilidad.
- O (Open/Closed): Se pueden añadir nuevos roles sin modificar Empleado.
- L (Liskov Substitution): Cajero y Cocinero sustituyen a Empleado en cualquier contexto.
"""

from abc import ABC, abstractmethod


class Empleado(ABC):
    """
    Clase base abstracta para todos los empleados de la cafetería.

    Define el contrato común (nombre, empleado_id, salario) y
    el método abstracto que cada rol concreto debe implementar.
    """

    def __init__(self, nombre: str, empleado_id: int, salario: float) -> None:
        if salario < 0:
            raise ValueError("El salario no puede ser negativo.")
        self._nombre = nombre
        self._empleado_id = empleado_id
        self._salario = salario

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def empleado_id(self) -> int:
        return self._empleado_id

    @property
    def salario(self) -> float:
        return self._salario

    @abstractmethod
    def realizar_tarea(self) -> str:
        """Ejecuta la tarea principal del empleado según su rol."""

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self._empleado_id}, nombre={self._nombre!r})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"nombre={self._nombre!r}, "
            f"empleado_id={self._empleado_id}, "
            f"salario={self._salario})"
        )


class Cajero(Empleado):
    """
    Empleado responsable de atender la caja y procesar pagos.

    También actúa como Observador del patrón Observer para
    recibir notificaciones de nuevos pedidos.
    """

    def realizar_tarea(self) -> str:
        return f"{self._nombre} está procesando el cobro en caja."

    def notificar_nuevo_pedido(self, pedido_id: int) -> None:
        """Notifica al cajero sobre un nuevo pedido."""
        print(f"[Cajero {self._nombre}] Nuevo pedido #{pedido_id} recibido.")


class Cocinero(Empleado):
    """
    Empleado responsable de preparar los pedidos en cocina.

    También actúa como Observador del patrón Observer para
    recibir notificaciones cuando hay pedidos listos para preparar.
    """

    def __init__(
        self, nombre: str, empleado_id: int, salario: float, especialidad: str = "General"
    ) -> None:
        super().__init__(nombre, empleado_id, salario)
        self._especialidad = especialidad

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def realizar_tarea(self) -> str:
        return f"{self._nombre} está preparando un pedido ({self._especialidad})."

    def notificar_pedido_listo(self, pedido_id: int) -> None:
        """Notifica al cocinero que debe preparar el pedido."""
        print(f"[Cocinero {self._nombre}] Preparando pedido #{pedido_id}.")
