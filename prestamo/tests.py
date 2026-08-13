from django.test import TestCase
from .models import Prestamo, ItemPrestamo
from inventario.models import Producto, Categoria
from usuario.models import Usuario
from django.utils import timezone


class PrestamoModelTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create(
            documento="12345678",
            primer_nombre="Juan",
            primer_apellido="Perez",
            tipo_documento="CC"
        )
        self.categoria = Categoria.objects.create(nombre="Herramientas")
        self.producto = Producto.objects.create(
            codigo_sku="HRR-001", nombre="Taladro", stock=5, categoria=self.categoria
        )
        self.prestamo = Prestamo.objects.create(
            documento=self.user,
            nombre_usuario="Juan Perez",
            estado="pendiente",
            fecha_vencimiento=timezone.now().date() + timezone.timedelta(days=3)
        )
        self.item = ItemPrestamo.objects.create(
            codigo_prestamo=self.prestamo, codigo_herramienta=self.producto, cantidad=1
        )

    def test_prestamo_creacion(self):
        self.assertEqual(Prestamo.objects.count(), 1)
        self.assertEqual(self.prestamo.usuario, "12345678")
        self.assertEqual(self.prestamo.estado, "pendiente")

    def test_item_prestamo_creacion(self):
        self.assertEqual(ItemPrestamo.objects.count(), 1)
        self.assertEqual(self.item.cantidad, 1)

    def test_prestamo_str(self):
        self.assertIn("12345678", str(self.prestamo))

    def test_item_str(self):
        self.assertIn("Taladro", str(self.item))

    def test_item_estado_default(self):
        self.assertFalse(self.item.devuelto)
