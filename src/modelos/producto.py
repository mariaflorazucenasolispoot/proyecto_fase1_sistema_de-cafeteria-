"""
Módulo de productos del sistema de cafetería.

Principios SOLID aplicados:
- S (Single Responsibility): Cada clase maneja únicamente la lógica de su tipo de producto.
- O (Open/Closed): Se pueden agregar nuevas categorías sin modificar las existentes.
- L (Liskov Substitution): Bebida, Comida y Postre sustituyen a Producto sin romper el contrato.
- I (Interface Segregation): IProducto define sólo lo que todos los productos necesitan.
- D (Dependency Inversion): Los módulos de alto nivel dependen de IProducto, no de clases concretas.
"""

from abc import ABC, abstractmethod


class IProducto(ABC):
    """Interfaz que deben cumplir todos los productos de la cafetería."""

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Retorna el nombre del producto."""

    @property
    @abstractmethod
    def precio(self) -> float:
        """Retorna el precio del producto."""

    @property
    @abstractmethod
    def descripcion(self) -> str:
        """Retorna la descripción del producto."""

    @abstractmethod
    def obtener_categoria(self) -> str:
        """Retorna la categoría del producto."""


class Producto(IProducto, ABC):
    """
    Clase base abstracta para todos los productos de la cafetería.

    Encapsula los atributos comunes (nombre, precio, descripción) y
    define el contrato que deben respetar los productos concretos.
    """

    def __init__(self, nombre: str, precio: float, descripcion: str) -> None:
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._nombre = nombre
        self._precio = precio
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio(self) -> float:
        return self._precio

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @abstractmethod
    def obtener_categoria(self) -> str:
        """Retorna la categoría concreta del producto."""

    def __str__(self) -> str:
        return f"[{self.obtener_categoria()}] {self._nombre} - ${self._precio:.2f}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"nombre={self._nombre!r}, precio={self._precio})"
        )


class Bebida(Producto):
    """
    Producto de tipo bebida.

    Extiende Producto añadiendo el atributo de temperatura (fría/caliente).
    """

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        temperatura: str = "fría",
    ) -> None:
        super().__init__(nombre, precio, descripcion)
        self._temperatura = temperatura

    @property
    def temperatura(self) -> str:
        return self._temperatura

    def obtener_categoria(self) -> str:
        return "Bebida"


class Comida(Producto):
    """
    Producto de tipo comida.

    Extiende Producto añadiendo el número de calorías.
    """

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        calorias: int = 0,
    ) -> None:
        super().__init__(nombre, precio, descripcion)
        if calorias < 0:
            raise ValueError("Las calorías no pueden ser negativas.")
        self._calorias = calorias

    @property
    def calorias(self) -> int:
        return self._calorias

    def obtener_categoria(self) -> str:
        return "Comida"


class Postre(Producto):
    """
    Producto de tipo postre.

    Extiende Producto añadiendo la indicación de contenido de gluten.
    """

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        contiene_gluten: bool = True,
    ) -> None:
        super().__init__(nombre, precio, descripcion)
        self._contiene_gluten = contiene_gluten

    @property
    def contiene_gluten(self) -> bool:
        return self._contiene_gluten

    def obtener_categoria(self) -> str:
        return "Postre"
