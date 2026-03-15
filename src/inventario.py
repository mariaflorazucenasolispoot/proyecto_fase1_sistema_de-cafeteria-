"""
Módulo del inventario del sistema de cafetería.

Patrón de diseño: Singleton
============================
Garantiza que sólo exista una instancia de Inventario en toda la aplicación,
proporcionando un punto global de acceso al stock de productos.

Principios SOLID aplicados:
- S (Single Responsibility): Inventario sólo gestiona el stock de productos.
- D (Dependency Inversion): Usa IProducto como abstracción, no clases concretas.
"""

from typing import Dict

from src.modelos.producto import IProducto


class Inventario:
    """
    Gestiona el inventario de productos disponibles en la cafetería.

    Implementa el patrón Singleton para asegurar una única instancia.
    """

    _instancia: "Inventario | None" = None

    def __new__(cls) -> "Inventario":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._stock: Dict[str, int] = {}
        return cls._instancia

    @classmethod
    def resetear(cls) -> None:
        """Reinicia el singleton (útil para pruebas unitarias)."""
        cls._instancia = None

    def agregar_stock(self, producto: IProducto, cantidad: int) -> None:
        """Incrementa el stock del producto indicado."""
        if cantidad <= 0:
            raise ValueError("La cantidad a agregar debe ser mayor a cero.")
        nombre = producto.nombre
        self._stock[nombre] = self._stock.get(nombre, 0) + cantidad

    def reducir_stock(self, producto: IProducto, cantidad: int) -> None:
        """Reduce el stock del producto indicado."""
        if cantidad <= 0:
            raise ValueError("La cantidad a reducir debe ser mayor a cero.")
        nombre = producto.nombre
        stock_actual = self._stock.get(nombre, 0)
        if stock_actual < cantidad:
            raise ValueError(
                f"Stock insuficiente para '{nombre}': "
                f"disponible={stock_actual}, solicitado={cantidad}."
            )
        self._stock[nombre] = stock_actual - cantidad

    def consultar_stock(self, producto: IProducto) -> int:
        """Retorna la cantidad disponible del producto."""
        return self._stock.get(producto.nombre, 0)

    def hay_disponibilidad(self, producto: IProducto, cantidad: int = 1) -> bool:
        """Indica si hay suficiente stock para la cantidad solicitada."""
        return self.consultar_stock(producto) >= cantidad

    def __str__(self) -> str:
        if not self._stock:
            return "Inventario vacío."
        lineas = ["=== Inventario ==="]
        for nombre, cantidad in self._stock.items():
            lineas.append(f"  {nombre}: {cantidad} unidades")
        return "\n".join(lineas)
