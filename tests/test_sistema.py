"""
Pruebas unitarias del sistema de cafetería.

Cubren:
- Modelos: Producto, Pedido, Cliente, Empleado, Menu
- Patrones: Singleton, Factory Method, Observer, Strategy
- Sistema integrado: SistemaCafeteria
"""

import pytest

from src.inventario import Inventario
from src.modelos.cliente import Cliente
from src.modelos.empleado import Cajero, Cocinero
from src.modelos.menu import Menu
from src.modelos.pedido import EstadoPedido, ItemPedido, Pedido
from src.modelos.producto import Bebida, Comida, IProducto, Postre, Producto
from src.patrones.estrategia_pago import (
    ContextoPago,
    PagoDigital,
    PagoEfectivo,
    PagoTarjeta,
)
from src.patrones.fabrica import FabricaBebida, FabricaComida, FabricaPostre, obtener_fabrica
from src.patrones.observador import (
    IObservador,
    ObservadorCajero,
    ObservadorCocinero,
    SujetoObservable,
)
from src.sistema_cafeteria import SistemaCafeteria


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def resetear_singletons():
    """Reinicia los singletons antes de cada prueba para garantizar aislamiento."""
    SistemaCafeteria.resetear()
    Inventario.resetear()
    # Resetear contador de IDs de Pedido
    Pedido._siguiente_id = 1
    yield
    SistemaCafeteria.resetear()
    Inventario.resetear()
    Pedido._siguiente_id = 1


@pytest.fixture
def cafe():
    return Bebida("Café Americano", 25.00, "Café negro", temperatura="caliente")


@pytest.fixture
def torta():
    return Comida("Torta de jamón", 45.00, "Torta con jamón", calorias=520)


@pytest.fixture
def pay():
    return Postre("Pay de queso", 35.00, "Pay de queso", contiene_gluten=True)


@pytest.fixture
def sistema():
    s = SistemaCafeteria()
    cafe = s.registrar_producto("bebida", "Café Americano", 25.00, "Café negro", temperatura="caliente")
    torta = s.registrar_producto("comida", "Torta de jamón", 45.00, "Torta con jamón", calorias=520)
    pay = s.registrar_producto("postre", "Pay de queso", 35.00, "Pay de queso", contiene_gluten=True)
    s.abastecer(cafe, 10)
    s.abastecer(torta, 10)
    s.abastecer(pay, 10)
    return s


# ===========================================================================
# MODELOS
# ===========================================================================

class TestProducto:
    def test_bebida_categoria(self, cafe):
        assert cafe.obtener_categoria() == "Bebida"

    def test_comida_categoria(self, torta):
        assert torta.obtener_categoria() == "Comida"

    def test_postre_categoria(self, pay):
        assert pay.obtener_categoria() == "Postre"

    def test_precio_negativo_lanza_error(self):
        with pytest.raises(ValueError):
            Bebida("Jugo", -5.00, "desc")

    def test_calorias_negativas_lanza_error(self):
        with pytest.raises(ValueError):
            Comida("Tacos", 20.00, "desc", calorias=-100)

    def test_str_contiene_nombre_y_precio(self, cafe):
        texto = str(cafe)
        assert "Café Americano" in texto
        assert "25.00" in texto

    def test_es_instancia_de_iproducto(self, cafe, torta, pay):
        assert isinstance(cafe, IProducto)
        assert isinstance(torta, IProducto)
        assert isinstance(pay, IProducto)

    def test_producto_es_abstracto(self):
        with pytest.raises(TypeError):
            Producto("x", 1.0, "desc")  # type: ignore[abstract]


class TestCliente:
    def test_atributos(self):
        c = Cliente("María", "maria@test.com")
        assert c.nombre == "María"
        assert c.correo == "maria@test.com"

    def test_historial_vacio_inicial(self):
        c = Cliente("Pedro", "pedro@test.com")
        assert c.historial_pedidos == []

    def test_agregar_pedido(self):
        c = Cliente("Pedro", "pedro@test.com")
        pedido = Pedido("Pedro")
        c.agregar_pedido(pedido)
        assert len(c.historial_pedidos) == 1

    def test_historial_es_copia(self):
        c = Cliente("Pedro", "pedro@test.com")
        historial = c.historial_pedidos
        historial.append("intruso")
        assert len(c.historial_pedidos) == 0


class TestEmpleado:
    def test_cajero_realizar_tarea(self):
        cajero = Cajero("Ana", 1, 8000.0)
        assert "Ana" in cajero.realizar_tarea()

    def test_cocinero_realizar_tarea(self):
        cocinero = Cocinero("Luis", 2, 7500.0, "Cocina mexicana")
        assert "Luis" in cocinero.realizar_tarea()

    def test_salario_negativo_lanza_error(self):
        with pytest.raises(ValueError):
            Cajero("X", 1, -100.0)

    def test_cocinero_especialidad(self):
        cocinero = Cocinero("Chef", 3, 9000.0, "Repostería")
        assert cocinero.especialidad == "Repostería"


class TestMenu:
    def test_agregar_y_obtener_producto(self, cafe):
        menu = Menu()
        menu.agregar_producto(cafe)
        assert menu.obtener_producto("Café Americano") is cafe

    def test_listar_productos(self, cafe, torta):
        menu = Menu()
        menu.agregar_producto(cafe)
        menu.agregar_producto(torta)
        assert len(menu.listar_productos()) == 2

    def test_listar_por_categoria(self, cafe, torta, pay):
        menu = Menu()
        for p in [cafe, torta, pay]:
            menu.agregar_producto(p)
        bebidas = menu.listar_por_categoria("bebida")
        assert len(bebidas) == 1 and bebidas[0] is cafe

    def test_producto_inexistente_lanza_error(self):
        menu = Menu()
        with pytest.raises(KeyError):
            menu.obtener_producto("No existe")

    def test_eliminar_producto(self, cafe):
        menu = Menu()
        menu.agregar_producto(cafe)
        menu.eliminar_producto("Café Americano")
        with pytest.raises(KeyError):
            menu.obtener_producto("Café Americano")


class TestPedido:
    def test_estado_inicial_pendiente(self, cafe):
        pedido = Pedido("Cliente")
        assert pedido.estado == EstadoPedido.PENDIENTE

    def test_total_correcto(self, cafe):
        pedido = Pedido("Cliente")
        pedido.agregar_item(ItemPedido(cafe, 2))
        assert pedido.total == pytest.approx(50.00)

    def test_items_son_copia(self, cafe):
        pedido = Pedido("Cliente")
        pedido.agregar_item(ItemPedido(cafe, 1))
        items = pedido.items
        items.clear()
        assert len(pedido.items) == 1

    def test_agregar_item_fuera_de_estado_pendiente(self, cafe):
        pedido = Pedido("Cliente")
        pedido.cambiar_estado(EstadoPedido.EN_PREPARACION)
        with pytest.raises(RuntimeError):
            pedido.agregar_item(ItemPedido(cafe, 1))

    def test_item_cantidad_invalida(self, cafe):
        with pytest.raises(ValueError):
            ItemPedido(cafe, 0)

    def test_cambiar_estado_notifica_observador(self, cafe):
        pedido = Pedido("Cliente")
        notificaciones = []

        class ObsTest(IObservador):
            def actualizar(self, p):
                notificaciones.append(p.estado)

        pedido.suscribir_observador(ObsTest())
        pedido.cambiar_estado(EstadoPedido.LISTO)
        assert notificaciones == [EstadoPedido.LISTO]


# ===========================================================================
# PATRONES DE DISEÑO
# ===========================================================================

class TestSingleton:
    def test_sistema_cafeteria_singleton(self):
        a = SistemaCafeteria()
        b = SistemaCafeteria()
        assert a is b

    def test_inventario_singleton(self):
        a = Inventario()
        b = Inventario()
        assert a is b


class TestFactoryMethod:
    def test_fabrica_bebida_crea_bebida(self):
        fabrica = FabricaBebida()
        producto = fabrica.crear_producto("Té", 15.0, "Té verde", temperatura="caliente")
        assert isinstance(producto, Bebida)
        assert producto.temperatura == "caliente"

    def test_fabrica_comida_crea_comida(self):
        fabrica = FabricaComida()
        producto = fabrica.crear_producto("Sandwich", 30.0, "Sandwich mixto", calorias=400)
        assert isinstance(producto, Comida)
        assert producto.calorias == 400

    def test_fabrica_postre_crea_postre(self):
        fabrica = FabricaPostre()
        producto = fabrica.crear_producto("Galleta", 12.0, "Galleta de choco", contiene_gluten=False)
        assert isinstance(producto, Postre)
        assert not producto.contiene_gluten

    def test_obtener_fabrica_invalida_lanza_error(self):
        with pytest.raises(ValueError):
            obtener_fabrica("sopa")

    def test_obtener_fabrica_case_insensitive(self):
        fabrica = obtener_fabrica("BEBIDA")
        assert isinstance(fabrica, FabricaBebida)


class TestObserver:
    def test_observadores_reciben_notificacion(self):
        sujeto = SujetoObservable()
        recibidos = []

        class ObsTest(IObservador):
            def actualizar(self, pedido):
                recibidos.append(pedido)

        obs = ObsTest()
        sujeto.suscribir(obs)
        pedido_mock = object()
        sujeto.notificar(pedido_mock)
        assert recibidos == [pedido_mock]

    def test_desuscribir_elimina_observador(self):
        sujeto = SujetoObservable()
        recibidos = []

        class ObsTest(IObservador):
            def actualizar(self, pedido):
                recibidos.append(pedido)

        obs = ObsTest()
        sujeto.suscribir(obs)
        sujeto.desuscribir(obs)
        sujeto.notificar(object())
        assert recibidos == []

    def test_suscripcion_duplicada_ignorada(self):
        sujeto = SujetoObservable()
        recibidos = []

        class ObsTest(IObservador):
            def actualizar(self, pedido):
                recibidos.append(pedido)

        obs = ObsTest()
        sujeto.suscribir(obs)
        sujeto.suscribir(obs)  # segunda suscripción ignorada
        sujeto.notificar(object())
        assert len(recibidos) == 1

    def test_observador_cajero_imprime(self, capsys, cafe):
        cajero = ObservadorCajero("Ana")
        pedido = Pedido("Cliente")
        pedido.agregar_item(ItemPedido(cafe, 1))
        pedido.cambiar_estado(EstadoPedido.LISTO)
        cajero.actualizar(pedido)
        capturado = capsys.readouterr()
        assert "Ana" in capturado.out

    def test_observador_cocinero_imprime(self, capsys, cafe):
        cocinero = ObservadorCocinero("Luis")
        pedido = Pedido("Cliente")
        pedido.agregar_item(ItemPedido(cafe, 1))
        pedido.cambiar_estado(EstadoPedido.EN_PREPARACION)
        cocinero.actualizar(pedido)
        capturado = capsys.readouterr()
        assert "Luis" in capturado.out


class TestStrategy:
    def test_pago_efectivo_correcto(self):
        pago = PagoEfectivo(100.0)
        resultado = pago.procesar_pago(85.0)
        assert "15.00" in resultado

    def test_pago_efectivo_insuficiente(self):
        pago = PagoEfectivo(50.0)
        with pytest.raises(ValueError):
            pago.procesar_pago(85.0)

    def test_pago_tarjeta_oculta_digitos(self):
        pago = PagoTarjeta("4111111111111234", "crédito")
        resultado = pago.procesar_pago(50.0)
        assert "1234" in resultado
        assert "4111" not in resultado

    def test_pago_digital_muestra_plataforma(self):
        pago = PagoDigital("user@test.com", "PayPal")
        resultado = pago.procesar_pago(30.0)
        assert "PayPal" in resultado

    def test_contexto_pago_monto_invalido(self):
        contexto = ContextoPago(PagoEfectivo(100.0))
        with pytest.raises(ValueError):
            contexto.ejecutar_pago(0)

    def test_contexto_pago_cambiar_estrategia(self):
        contexto = ContextoPago(PagoEfectivo(100.0))
        contexto.establecer_estrategia(PagoTarjeta("1234567890121234"))
        assert isinstance(contexto.estrategia, PagoTarjeta)


# ===========================================================================
# INVENTARIO
# ===========================================================================

class TestInventario:
    def test_agregar_y_consultar_stock(self, cafe):
        inv = Inventario()
        inv.agregar_stock(cafe, 5)
        assert inv.consultar_stock(cafe) == 5

    def test_reducir_stock(self, cafe):
        inv = Inventario()
        inv.agregar_stock(cafe, 5)
        inv.reducir_stock(cafe, 3)
        assert inv.consultar_stock(cafe) == 2

    def test_stock_insuficiente_lanza_error(self, cafe):
        inv = Inventario()
        inv.agregar_stock(cafe, 2)
        with pytest.raises(ValueError):
            inv.reducir_stock(cafe, 5)

    def test_hay_disponibilidad(self, cafe):
        inv = Inventario()
        inv.agregar_stock(cafe, 3)
        assert inv.hay_disponibilidad(cafe, 3)
        assert not inv.hay_disponibilidad(cafe, 4)

    def test_cantidad_cero_lanza_error(self, cafe):
        inv = Inventario()
        with pytest.raises(ValueError):
            inv.agregar_stock(cafe, 0)


# ===========================================================================
# SISTEMA INTEGRADO
# ===========================================================================

class TestSistemaCafeteria:
    def test_registrar_producto_con_fabrica(self):
        sistema = SistemaCafeteria()
        producto = sistema.registrar_producto(
            "bebida", "Té Verde", 18.0, "Té verde caliente", temperatura="caliente"
        )
        assert isinstance(producto, Bebida)
        assert sistema.menu.obtener_producto("Té Verde") is producto

    def test_flujo_completo_pedido_y_pago(self, sistema):
        cajero = ObservadorCajero("Ana")
        sistema.registrar_observador(cajero)

        pedido = sistema.crear_pedido("María García")
        sistema.agregar_item_a_pedido(pedido, "Café Americano", 2)
        sistema.agregar_item_a_pedido(pedido, "Pay de queso", 1)

        assert pedido.total == pytest.approx(85.0)

        sistema.actualizar_estado_pedido(pedido, EstadoPedido.EN_PREPARACION)
        sistema.actualizar_estado_pedido(pedido, EstadoPedido.LISTO)

        resultado = sistema.procesar_pago(pedido, PagoEfectivo(100.0))
        assert "15.00" in resultado
        assert pedido.estado == EstadoPedido.ENTREGADO

    def test_pago_pedido_ya_entregado_lanza_error(self, sistema):
        pedido = sistema.crear_pedido("Pedro")
        sistema.agregar_item_a_pedido(pedido, "Café Americano", 1)
        sistema.actualizar_estado_pedido(pedido, EstadoPedido.LISTO)
        sistema.procesar_pago(pedido, PagoEfectivo(50.0))
        with pytest.raises(RuntimeError):
            sistema.procesar_pago(pedido, PagoEfectivo(50.0))

    def test_stock_se_reduce_al_agregar_item(self, sistema):
        pedido = sistema.crear_pedido("X")
        sistema.agregar_item_a_pedido(pedido, "Café Americano", 3)
        assert sistema.inventario.consultar_stock(
            sistema.menu.obtener_producto("Café Americano")
        ) == 7

    def test_stock_insuficiente_lanza_error(self, sistema):
        pedido = sistema.crear_pedido("X")
        with pytest.raises(ValueError):
            sistema.agregar_item_a_pedido(pedido, "Café Americano", 100)

    def test_obtener_pedido_invalido_lanza_error(self, sistema):
        with pytest.raises(KeyError):
            sistema.obtener_pedido(9999)
