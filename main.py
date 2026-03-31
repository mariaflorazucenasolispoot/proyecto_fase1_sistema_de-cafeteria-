"""
Punto de entrada principal del Sistema de Cafetería.

Demuestra el uso de:
- Patrón Singleton  (SistemaCafeteria, Inventario)
- Patrón Factory Method (registrar_producto → FabricaBebida/FabricaComida/FabricaPostre)
- Patrón Observer (ObservadorCajero, ObservadorCocinero)
- Patrón Strategy (PagoEfectivo, PagoTarjeta, PagoDigital)
"""

from src.modelos.pedido import EstadoPedido
from src.patrones.estrategia_pago import PagoDigital, PagoEfectivo, PagoTarjeta
from src.patrones.observador import ObservadorCajero, ObservadorCocinero
from src.sistema_cafeteria import SistemaCafeteria


def main() -> None:
    # ------------------------------------------------------------------ #
    # 1. Obtener la instancia única del sistema (Singleton)               #
    # ------------------------------------------------------------------ #
    sistema = SistemaCafeteria()

    # ------------------------------------------------------------------ #
    # 2. Registrar observadores (Observer)                                #
    # ------------------------------------------------------------------ #
    cajero = ObservadorCajero("Ana")
    cocinero = ObservadorCocinero("Luis")
    sistema.registrar_observador(cajero)
    sistema.registrar_observador(cocinero)

    # ------------------------------------------------------------------ #
    # 3. Registrar productos usando Factory Method                        #
    # ------------------------------------------------------------------ #
    cafe = sistema.registrar_producto(
        "bebida", "Café Americano", 25.00,
        "Café negro servido caliente", temperatura="caliente"
    )
    agua = sistema.registrar_producto(
        "bebida", "Agua Natural", 10.00,
        "Agua embotellada 500 ml", temperatura="fría"
    )
    torta = sistema.registrar_producto(
        "comida", "Torta de jamón", 45.00,
        "Torta con jamón, queso y jitomate", calorias=520
    )
    pay = sistema.registrar_producto(
        "postre", "Pay de queso", 35.00,
        "Pay de queso con base de galleta", contiene_gluten=True
    )

    # ------------------------------------------------------------------ #
    # 4. Abastecer inventario                                             #
    # ------------------------------------------------------------------ #
    sistema.abastecer(cafe, 20)
    sistema.abastecer(agua, 30)
    sistema.abastecer(torta, 10)
    sistema.abastecer(pay, 15)

    print(sistema.menu)
    print()
    print(sistema.inventario)
    print()

    # ------------------------------------------------------------------ #
    # 5. Crear un pedido y agregar ítems                                  #
    # ------------------------------------------------------------------ #
    pedido1 = sistema.crear_pedido("María García")
    sistema.agregar_item_a_pedido(pedido1, "Café Americano", 2)
    sistema.agregar_item_a_pedido(pedido1, "Pay de queso", 1)

    print(pedido1)
    print()

    # ------------------------------------------------------------------ #
    # 6. Cambiar estado del pedido (Observer notifica automáticamente)    #
    # ------------------------------------------------------------------ #
    sistema.actualizar_estado_pedido(pedido1, EstadoPedido.EN_PREPARACION)
    sistema.actualizar_estado_pedido(pedido1, EstadoPedido.LISTO)
    print()

    # ------------------------------------------------------------------ #
    # 7. Procesar pago con Strategy                                       #
    # ------------------------------------------------------------------ #
    # Pago en efectivo
    resultado = sistema.procesar_pago(pedido1, PagoEfectivo(100.00))
    print(f"\n{resultado}")
    print()

    # Segundo pedido con pago por tarjeta
    pedido2 = sistema.crear_pedido("Carlos López")
    sistema.agregar_item_a_pedido(pedido2, "Torta de jamón", 1)
    sistema.agregar_item_a_pedido(pedido2, "Agua Natural", 1)
    sistema.actualizar_estado_pedido(pedido2, EstadoPedido.EN_PREPARACION)
    sistema.actualizar_estado_pedido(pedido2, EstadoPedido.LISTO)
    resultado2 = sistema.procesar_pago(pedido2, PagoTarjeta("4111111111111234", "crédito"))
    print(f"\n{resultado2}")
    print()

    # Tercer pedido con pago digital
    pedido3 = sistema.crear_pedido("Sofía Martínez")
    sistema.agregar_item_a_pedido(pedido3, "Agua Natural", 2)
    sistema.actualizar_estado_pedido(pedido3, EstadoPedido.EN_PREPARACION)
    sistema.actualizar_estado_pedido(pedido3, EstadoPedido.LISTO)
    resultado3 = sistema.procesar_pago(pedido3, PagoDigital("sofia@email.com", "MercadoPago"))
    print(f"\n{resultado3}")

    # ------------------------------------------------------------------ #
    # 8. Verificar que Singleton retorna la misma instancia               #
    # ------------------------------------------------------------------ #
    sistema_b = SistemaCafeteria()
    assert sistema is sistema_b, "¡Singleton fallido! Se crearon dos instancias."
    print("\n[OK] SistemaCafeteria es Singleton: ambas referencias apuntan a la misma instancia.")


if __name__ == "__main__":
    main()
