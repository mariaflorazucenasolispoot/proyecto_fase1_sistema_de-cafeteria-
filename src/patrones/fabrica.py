"""
Patrón de diseño: Factory Method (Método Fábrica)
==================================================
Define una interfaz para crear objetos, pero delega a las subclases
la decisión de qué clase concreta instanciar.

Clases:
- IFabricaProducto: interfaz de fábrica de productos.
- FabricaBebida: crea instancias de Bebida.
- FabricaComida: crea instancias de Comida.
- FabricaPostre: crea instancias de Postre.

Principios SOLID aplicados:
- O (Open/Closed): Se pueden añadir nuevas fábricas sin modificar las existentes.
- D (Dependency Inversion): Los clientes dependen de IFabricaProducto, no de clases concretas.
"""

from abc import ABC, abstractmethod

from src.modelos.producto import Bebida, Comida, IProducto, Postre


class IFabricaProducto(ABC):
    """Interfaz del patrón Factory Method para la creación de productos."""

    @abstractmethod
    def crear_producto(self, nombre: str, precio: float, descripcion: str, **kwargs) -> IProducto:
        """Crea y retorna un producto de la categoría correspondiente."""


class FabricaBebida(IFabricaProducto):
    """Fábrica concreta que crea instancias de Bebida."""

    def crear_producto(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        temperatura: str = "fría",
        **kwargs,
    ) -> Bebida:
        return Bebida(nombre, precio, descripcion, temperatura)


class FabricaComida(IFabricaProducto):
    """Fábrica concreta que crea instancias de Comida."""

    def crear_producto(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        calorias: int = 0,
        **kwargs,
    ) -> Comida:
        return Comida(nombre, precio, descripcion, calorias)


class FabricaPostre(IFabricaProducto):
    """Fábrica concreta que crea instancias de Postre."""

    def crear_producto(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        contiene_gluten: bool = True,
        **kwargs,
    ) -> Postre:
        return Postre(nombre, precio, descripcion, contiene_gluten)


# Registro de fábricas disponibles (facilita la extensión sin modificar código)
_FABRICAS: dict = {
    "bebida": FabricaBebida(),
    "comida": FabricaComida(),
    "postre": FabricaPostre(),
}


def obtener_fabrica(categoria: str) -> IFabricaProducto:
    """
    Retorna la fábrica correspondiente a la categoría indicada.

    Args:
        categoria: 'bebida', 'comida' o 'postre' (no sensible a mayúsculas).

    Raises:
        ValueError: si la categoría no tiene fábrica registrada.
    """
    fabrica = _FABRICAS.get(categoria.lower())
    if fabrica is None:
        raise ValueError(
            f"Categoría desconocida: '{categoria}'. "
            f"Categorías válidas: {list(_FABRICAS.keys())}"
        )
    return fabrica
