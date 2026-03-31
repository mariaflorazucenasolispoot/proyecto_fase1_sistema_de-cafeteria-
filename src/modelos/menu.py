"""
Módulo del menú del sistema de cafetería.

Principios SOLID aplicados:
- S (Single Responsibility): Menu sólo gestiona la colección de productos disponibles.
- O (Open/Closed): Se pueden agregar/quitar productos sin modificar la lógica del menú.
"""

from typing import Dict, List

from src.modelos.producto import IProducto


class Menu:
    """
    Representa el menú de la cafetería.

    Permite agregar y consultar productos disponibles por nombre o categoría.
    """

    def __init__(self) -> None:
        self._productos: Dict[str, IProducto] = {}

    def agregar_producto(self, producto: IProducto) -> None:
        """Añade un producto al menú."""
        self._productos[producto.nombre] = producto

    def eliminar_producto(self, nombre: str) -> None:
        """Elimina un producto del menú por nombre."""
        self._productos.pop(nombre, None)

    def obtener_producto(self, nombre: str) -> IProducto:
        """Retorna un producto por nombre; lanza KeyError si no existe."""
        if nombre not in self._productos:
            raise KeyError(f"El producto '{nombre}' no existe en el menú.")
        return self._productos[nombre]

    def listar_productos(self) -> List[IProducto]:
        """Retorna todos los productos del menú."""
        return list(self._productos.values())

    def listar_por_categoria(self, categoria: str) -> List[IProducto]:
        """Retorna los productos que pertenecen a una categoría dada."""
        return [
            p for p in self._productos.values()
            if p.obtener_categoria().lower() == categoria.lower()
        ]

    def __str__(self) -> str:
        if not self._productos:
            return "El menú está vacío."
        lineas = ["=== Menú de la Cafetería ==="]
        for producto in self._productos.values():
            lineas.append(f"  {producto}")
        return "\n".join(lineas)
