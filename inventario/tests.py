from django.test import TestCase
from .models import Categoria, Producto


class InventarioModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Electrónica", descripcion="Dispositivos electrónicos y accesorios"
        )
        self.producto = Producto.objects.create(
            codigo_sku="ELC-101",
            nombre="Laptop Dell",
            stock=15,
            categoria=self.categoria,
            disponible=True,
        )

    def test_categoria_creacion(self):
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(str(self.categoria), "Electrónica")

    def test_producto_creacion(self):
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(str(self.producto), "[ELC-101] Laptop Dell")
        self.assertEqual(self.producto.stock, 15)

    def test_producto_categoria_relacion(self):
        self.assertEqual(self.producto.categoria.nombre, "Electrónica")

    def test_producto_disponibilidad(self):
        self.assertTrue(self.producto.disponible)
        self.producto.disponible = False
        self.producto.save()
        self.assertFalse(self.producto.disponible)

    def test_categoria_unica(self):
        from django.db.utils import IntegrityError

        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nombre="Electrónica")
