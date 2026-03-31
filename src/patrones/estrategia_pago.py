"""
Patrón de diseño: Strategy (Estrategia)
========================================
Define una familia de algoritmos (métodos de pago), los encapsula en clases
independientes y los hace intercambiables sin alterar el código cliente.

Clases:
- IEstrategiaPago: interfaz de estrategia de pago.
- PagoEfectivo: paga con efectivo y calcula el cambio.
- PagoTarjeta: paga con tarjeta de débito/crédito.
- PagoDigital: paga con billetera digital (p.ej. PayPal, MercadoPago).
- ContextoPago: contexto que usa una estrategia de pago concreta.

Principios SOLID aplicados:
- O (Open/Closed): Se pueden agregar nuevas estrategias sin modificar ContextoPago.
- L (Liskov Substitution): Cualquier IEstrategiaPago puede ser usada en ContextoPago.
- D (Dependency Inversion): ContextoPago depende de IEstrategiaPago, no de implementaciones.
"""

from abc import ABC, abstractmethod


class IEstrategiaPago(ABC):
    """Interfaz del patrón Strategy para los métodos de pago."""

    @abstractmethod
    def procesar_pago(self, monto: float) -> str:
        """Procesa el pago del monto indicado y retorna un mensaje de confirmación."""


class PagoEfectivo(IEstrategiaPago):
    """Estrategia de pago con efectivo; calcula el cambio a devolver."""

    def __init__(self, monto_entregado: float) -> None:
        self._monto_entregado = monto_entregado

    def procesar_pago(self, monto: float) -> str:
        if self._monto_entregado < monto:
            raise ValueError(
                f"Efectivo insuficiente: se entregaron ${self._monto_entregado:.2f} "
                f"pero el total es ${monto:.2f}."
            )
        cambio = self._monto_entregado - monto
        return (
            f"Pago en efectivo de ${monto:.2f} procesado. "
            f"Cambio: ${cambio:.2f}"
        )


class PagoTarjeta(IEstrategiaPago):
    """Estrategia de pago con tarjeta de débito o crédito."""

    def __init__(self, numero_tarjeta: str, tipo: str = "débito") -> None:
        # Almacena sólo los últimos 4 dígitos por seguridad
        self._ultimos_digitos = numero_tarjeta[-4:]
        self._tipo = tipo

    def procesar_pago(self, monto: float) -> str:
        return (
            f"Pago con tarjeta {self._tipo} (****{self._ultimos_digitos}) "
            f"de ${monto:.2f} procesado correctamente."
        )


class PagoDigital(IEstrategiaPago):
    """Estrategia de pago con billetera digital (PayPal, MercadoPago, etc.)."""

    def __init__(self, cuenta: str, plataforma: str = "MercadoPago") -> None:
        self._cuenta = cuenta
        self._plataforma = plataforma

    def procesar_pago(self, monto: float) -> str:
        return (
            f"Pago digital vía {self._plataforma} desde {self._cuenta} "
            f"de ${monto:.2f} procesado correctamente."
        )


class ContextoPago:
    """
    Contexto del patrón Strategy.

    Permite cambiar la estrategia de pago en tiempo de ejecución y
    delega la ejecución del pago a la estrategia configurada.
    """

    def __init__(self, estrategia: IEstrategiaPago) -> None:
        self._estrategia = estrategia

    @property
    def estrategia(self) -> IEstrategiaPago:
        return self._estrategia

    def establecer_estrategia(self, estrategia: IEstrategiaPago) -> None:
        """Reemplaza la estrategia de pago activa."""
        self._estrategia = estrategia

    def ejecutar_pago(self, monto: float) -> str:
        """Ejecuta el pago usando la estrategia actual."""
        if monto <= 0:
            raise ValueError("El monto a pagar debe ser mayor a cero.")
        return self._estrategia.procesar_pago(monto)
