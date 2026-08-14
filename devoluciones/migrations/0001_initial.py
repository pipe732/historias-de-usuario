import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prestamo', '0001_initial'),
        ("usuario", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name='Devolucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('devolucion_total', models.BooleanField(default=True, help_text='True = todas las herramientas; False = devolución parcial')),
                ('motivo', models.TextField()),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=20)),
                ('estado_equipo', models.CharField(choices=[('excelente', 'Excelente'), ('limpieza', 'Requiere Limpieza'), ('mantenimiento', 'Requiere Mantenimiento'), ('danado', 'Dañado / Defectuoso')], default='excelente', max_length=30, verbose_name='Estado de la herramienta')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('items', models.ManyToManyField(blank=True, related_name='devoluciones', to='prestamo.itemprestamo', verbose_name='Ítems devueltos')),
                ('prestamo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='devoluciones', to='prestamo.prestamo', verbose_name='Préstamo')),
            ],
            options={
                'verbose_name': 'Devolución',
                'verbose_name_plural': 'Devoluciones',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name="DevolucionHerramienta",
            fields=[
                (
                    "codigo_devolucion",
                    models.AutoField(
                        db_column="codigo_devolucion", primary_key=True, serialize=False
                    ),
                ),
                (
                    "observaciones",
                    models.TextField(
                        blank=True, null=True, verbose_name="Observaciones"
                    ),
                ),
                (
                    "fecha",
                    models.DateField(
                        auto_now_add=True, verbose_name="Fecha de devolución"
                    ),
                ),
                (
                    "devolucion_total",
                    models.BooleanField(
                        default=True,
                        help_text="True = todas las herramientas; False = devolución parcial",
                    ),
                ),
                (
                    "motivo",
                    models.TextField(blank=True, null=True, verbose_name="Motivo"),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("pendiente", "Pendiente"),
                            ("aprobada", "Aprobada"),
                            ("rechazada", "Rechazada"),
                        ],
                        default="pendiente",
                        max_length=20,
                    ),
                ),
                (
                    "estado_equipo",
                    models.CharField(
                        choices=[
                            ("excelente", "Excelente"),
                            ("limpieza", "Requiere Limpieza"),
                            ("mantenimiento", "Requiere Mantenimiento"),
                            ("danado", "Dañado / Defectuoso"),
                        ],
                        default="excelente",
                        max_length=30,
                        verbose_name="Estado de la herramienta",
                    ),
                ),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_actualizacion", models.DateTimeField(auto_now=True)),
                (
                    "codigo_prestamo",
                    models.ForeignKey(
                        db_column="codigo_prestamo",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="devoluciones",
                        to="prestamo.prestamo",
                        verbose_name="Préstamo",
                    ),
                ),
                (
                    "codigo_recibe",
                    models.ForeignKey(
                        blank=True,
                        db_column="codigo_recibe",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="devoluciones_recibidas",
                        to="usuario.usuario",
                        verbose_name="Usuario que recibe",
                    ),
                ),
                (
                    "items",
                    models.ManyToManyField(
                        blank=True,
                        related_name="devoluciones",
                        to="prestamo.detalleprestamo",
                        verbose_name="Ítems devueltos",
                    ),
                ),
            ],
            options={
                "verbose_name": "Devolución",
                "verbose_name_plural": "Devoluciones",
                "db_table": "devolucion_herramienta",
                "ordering": ["-fecha_creacion"],
            },
        ),
    ]

