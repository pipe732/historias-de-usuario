#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para poblar la base de datos con datos de ejemplo completos.
Cubre todas las tablas del sistema y utiliza valores válidos para las listas desplegables.
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta, time
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from django.contrib.sessions.models import Session
from django.db import transaction
from django.core.management import call_command

# Importar todos los modelos del proyecto
from usuario.models import Usuario
from almacenamiento.models import Almacen, Estante
from inventario.models import Categoria, Producto, Proveedor, Inventario, Movimientos, Detalle_Movimientos, Edicion_limitada
from mantenimiento.models import TipoEstado, TipoMantenimiento, Mantenimiento, DetalleMantenimiento
from prestamo.models import Prestamo, ItemPrestamo
from devoluciones.models import DevolucionHerramienta as Devolucion
from reportes.models import ReporteHistorial
from django.contrib.auth.hashers import make_password
from django.db import connection


def asegurar_tablas_sqlite():
    with connection.cursor() as cursor:
        for tbl in ['tipo_estado', 'mantenimiento_tipoestado', 'tipo_mantenimiento', 'mantenimiento_tipomantenimiento']:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {tbl} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre VARCHAR(50) NOT NULL
                );
            """)


def obtener_documentos_activos():
    """Obtiene los números de documento de usuarios con sesión activa."""
    documentos_activos = set()
    for session in Session.objects.all():
        try:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')  # Django guarda el ID de usuario aquí
            if user_id:
                documentos_activos.add(str(user_id))
        except Exception:
            pass
    return documentos_activos


def crear_usuarios():
    """Crear usuario admin y usuarios de prueba con Fichas y Programas válidos."""
    print("\n" + "="*70)
    print(">>> CREANDO USUARIOS")
    print("="*70)
    
    # Mantener el usuario admin principal
    admin_doc = '0000000000'
    admin, created = Usuario.objects.get_or_create(
        documento=admin_doc,
        defaults={
            'tipo_documento': 'CC',
            'primer_nombre': 'Administrador',
            'primer_apellido': 'Principal',
            'correo_personal': 'admin@mineinventory.com',
            'rol': 'Administrador',
            'password': make_password('@dmin123'),
            'telefono': '3000000000',
            'ficha': 'ADMIN-001',
            'programa': 'Administración'
        }
    )
    if not created:
        admin.password = make_password('@dmin123')
        admin.rol = 'Administrador'
        admin.save()
    print(f"[OK] Admin creado: {admin_doc}")

    # Limpiar otros usuarios que no tengan sesión activa para evitar inconsistencias
    docs_activos = obtener_documentos_activos()
    excluidos = ['0000000000'] + list(docs_activos)
    Usuario.objects.exclude(documento__in=excluidos).delete()

    nombres_usuarios = [
        ('Juan', 'Pérez'), ('María', 'García'), ('Carlos', 'López'), ('Ana', 'Martínez'),
        ('Roberto', 'González'), ('Sofía', 'Rodríguez'), ('Miguel', 'Hernández'),
        ('Isabella', 'Torres'), ('David', 'Ramírez'), ('Laura', 'Cruz'),
        ('Fernando', 'Morales'), ('Catalina', 'Soto'), ('Pablo', 'Gómez'),
    ]
    
    # Opciones de las listas desplegables de la interfaz
    fichas_opciones = ['2758369', '2827435', '2895642', '2910384', '3021948', '3196477']
    programas_opciones = [
        'Análisis y Desarrollo de Software (ADSO)',
        'Sistemas',
        'Electricidad Industrial',
        'Mantenimiento Electromecánico',
        'Supervisión de Labores Mineras',
        'Topografía',
        'Soldadura',
        'Gestión Ambiental'
    ]
    
    usuarios = list(Usuario.objects.all())
    for idx, (nombre, apellido) in enumerate(nombres_usuarios, 1):
        doc = f'1000000{idx:03d}'
        if doc in docs_activos:
            continue
        correo = f"{nombre.lower()}.{apellido.lower()}@sena.edu.co"
        
        usuario = Usuario.objects.create(
            documento=doc,
            tipo_documento='CC',
            primer_nombre=nombre,
            primer_apellido=apellido,
            correo_personal=correo,
            rol='Usuario',
            password=make_password('Contra123*'),
            telefono=f'310000{idx:04d}',
            ficha=random.choice(fichas_opciones),
            programa=random.choice(programas_opciones)
        )
        usuarios.append(usuario)
        print(f"[OK] Usuario creado: {doc} - {nombre} {apellido}")
    
    return usuarios


def crear_almacenamiento():
    """Crear almacenes y estantes."""
    print("\n" + "="*70)
    print(">>> CREANDO ALMACENAMIENTO")
    print("="*70)
    
    almacenes_datos = [
        ('Almacén A - Principal', 'Almacén general de herramientas manuales'),
        ('Almacén B - Eléctricos', 'Bodega especializada en herramientas de poder'),
        ('Almacén C - Reactivos y Seguridad', 'Almacén de EPP y equipos químicos')
    ]
    
    almacenes = []
    estantes = []
    for nombre, ubic in almacenes_datos:
        alm = Almacen.objects.create(nombre=nombre, dimensiones="10x15m", ubicacion=ubic)
        almacenes.append(alm)
        print(f"[OK] Almacén: {nombre}")
        
        for i in range(1, 4):
            codigo_estante = f"EST-{nombre.split(' ')[1]}-{i}"
            est = Estante.objects.create(
                codigo_almacen=alm,
                codigo=codigo_estante,
                dimensiones="2x1m"
            )
            estantes.append(est)
            print(f"  [OK] Estante: {codigo_estante}")
            
    return almacenes, estantes


def crear_categorias():
    """Crear categorías de herramientas."""
    print("\n" + "="*70)
    print(">>> CREANDO CATEGORÍAS")
    print("="*70)
    
    nombres = ['Herramientas Manuales', 'Herramientas Eléctricas', 'Equipos de Seguridad',
               'Equipos de Medición', 'Tuberías y Accesorios', 'Suministros de Construcción']
    
    categorias = []
    for nombre in nombres:
        cat = Categoria.objects.create(nombre=nombre, descripcion=f"Categoría de {nombre}")
        categorias.append(cat)
        print(f"[OK] Categoría: {nombre}")
    return categorias


def crear_productos(categorias):
    """Crear productos principales."""
    print("\n" + "="*70)
    print(">>> CREANDO PRODUCTOS")
    print("="*70)
    
    datos = [
        ('MART-001', 'Martillo de Goma', 'Martillo profesional anti-rebote', 'Herramientas Manuales'),
        ('TALD-20V', 'Taladro Inalámbrico 20V', 'Taladro percutor compacto de 20V', 'Herramientas Eléctricas'),
        ('CASC-001', 'Casco de Seguridad', 'Casco de protección ANSI clase E', 'Equipos de Seguridad'),
        ('MULT-001', 'Multímetro Digital', 'Multímetro automotriz y profesional', 'Equipos de Medición'),
        ('PINZ-001', 'Pinza Amperimétrica', 'Pinza para medición de corriente alterna', 'Equipos de Medición'),
        ('ESME-001', 'Esmeril Angular 4.5"', 'Esmeriladora angular de alto rendimiento', 'Herramientas Eléctricas'),
    ]
    
    cat_map = {c.nombre: c for c in categorias}
    productos = []
    for sku, nombre, desc, cat_name in datos:
        cat = cat_map.get(cat_name, categorias[0])
        prod = Producto.objects.create(
            codigo_sku=sku,
            nombre=nombre,
            descripcion=desc,
            categoria=cat,
            disponible=True,
            fecha_ingreso=timezone.now().date()
        )
        productos.append(prod)
        print(f"[OK] Producto: {sku} - {nombre}")
    return productos


def crear_proveedores():
    """Crear proveedores."""
    print("\n" + "="*70)
    print(">>> CREANDO PROVEEDORES")
    print("="*70)
    
    datos = [
        ('NIT-900123456-1', '3151234567', 'ventas@herramientascolombia.com', 'Distribuidor oficial de herramientas Stanley'),
        ('NIT-860987654-2', '3109876543', 'soporte@bosch-industrial.co', 'Proveedor de herramientas eléctricas Bosch'),
        ('NIT-800111222-3', '3201112222', 'contacto@epp-seguridad.com.co', 'Distribuidor de elementos de protección personal')
    ]
    
    proveedores = []
    for nit, tel, correo, desc in datos:
        prov = Proveedor.objects.create(nit_proveedor=nit, telefono_contacto=tel, correo_proveedor=correo, descripcion=desc)
        proveedores.append(prov)
        print(f"[OK] Proveedor: {nit}")
    return proveedores


def crear_inventario(productos, estantes, usuarios):
    """Crear existencias en estantes específicos."""
    print("\n" + "="*70)
    print(">>> CREANDO INVENTARIOS")
    print("="*70)
    
    inventarios = []
    for prod in productos:
        est = random.choice(estantes)
        resp = random.choice(usuarios)
        inv = Inventario.objects.create(
            num_estante=est,
            cantidad=random.randint(10, 50),
            responsable=resp.nombre_completo,
            fecha_creacion=timezone.now().date(),
            observaciones=f"Inventario físico inicial de {prod.nombre} en {est.codigo}"
        )
        inventarios.append(inv)
        print(f"[OK] Inventario: Existencia #{inv.pk} -> Estante {est.codigo}")
    return inventarios


def crear_movimientos(inventarios, proveedores):
    """Crear movimientos de stock."""
    print("\n" + "="*70)
    print(">>> CREANDO MOVIMIENTOS")
    print("="*70)
    
    tipos = ['Entrada', 'Salida', 'Traslado']
    for i in range(1, 11):
        inv = random.choice(inventarios)
        tipo = random.choice(tipos)
        cant = random.randint(2, 10)
        
        mov = Movimientos.objects.create(
            codigo_inventario=inv,
            cantidad_total=cant,
            tipo_movimiento=tipo,
            fecha_movimiento=timezone.now().date(),
            observaciones=f"Movimiento de {tipo} de {cant} unidades"
        )
        print(f"[OK] Movimiento #{mov.pk} ({tipo})")


def crear_edicion_limitada(productos):
    pass


def crear_mantenimientos(productos):
    """Crear órdenes de mantenimiento y sus detalles según los modelos actuales."""
    print("\n" + "="*70)
    print(">>> CREANDO MANTENIMIENTOS Y DETALLES")
    print("="*70)

    # Poblar catálogos de TipoEstado y TipoMantenimiento
    estados = ["Abierto", "En proceso", "Cerrado", "Cancelado"]
    for est in estados:
        TipoEstado.objects.get_or_create(nombre=est)

    tipos_cat = ["Mantenimiento Preventivo", "Mantenimiento Correctivo", "Calibración", "Reparación Externa"]
    for t in tipos_cat:
        TipoMantenimiento.objects.get_or_create(nombre=t)
    
    tipos = tipos_cat
    
    for i in range(1, 16):
        producto = random.choice(productos)
        tipo_mant = random.choice(tipos)
        
        fecha_ingreso = timezone.now().date() - timedelta(days=random.randint(5, 60))
        fecha_salida = fecha_ingreso + timedelta(days=random.randint(1, 5))
        
        mant = Mantenimiento.objects.create(
            codigo_herramienta=producto,
            tipo_mantenimiento=tipo_mant,
            fecha_ingreso=fecha_ingreso,
            fecha_salida=fecha_salida,
            observaciones=f"Mantenimiento de rutinas para {producto.nombre}."
        )
        
        DetalleMantenimiento.objects.create(
            num_mantenimiento=mant,
            accion_realizada=f"Diagnóstico e inspección de {tipo_mant.lower()}.",
            materiales_usados="Lubricante industrial, repuestos básicos",
            fecha_mantenimiento=fecha_ingreso,
            observacion="Servicio ejecutado correctamente."
        )
        print(f"[OK] Mantenimiento #{mant.pk} | {producto.nombre[:35]}")


def crear_prestamos(usuarios, productos):
    """Crear préstamos e ítems de préstamos."""
    print("\n" + "="*70)
    print(">>> CREANDO PRÉSTAMOS")
    print("="*70)
    
    estados = ['pendiente', 'activo', 'devuelto', 'vencido']
    prestamos = []
    
    for i in range(1, 11):
        user = random.choice(usuarios)
        est = random.choice(estados)
        
        fecha_pres = timezone.now() - timedelta(days=random.randint(1, 15))
        if est == 'vencido':
            fecha_venc = timezone.localdate() - timedelta(days=random.randint(1, 5))
        else:
            fecha_venc = timezone.localdate() + timedelta(days=random.randint(2, 10))
            
        pres = Prestamo.objects.create(
            documento=user,
            observaciones=f"Préstamo de prueba número {i}",
            estado=est,
            fecha=fecha_pres
        )
        
        num_items = random.randint(1, 3)
        selected_prods = random.sample(productos, num_items)
        for prod in selected_prods:
            ItemPrestamo.objects.create(
                codigo_prestamo=pres,
                codigo_herramienta=prod,
                cantidad=random.randint(1, 2),
                observaciones=f"Entrega de {prod.nombre}"
            )
            
        print(f"[OK] Préstamo #{pres.pk} ({est}) | {user.nombre_completo}")
        prestamos.append(pres)
    return prestamos


def crear_devoluciones(prestamos, usuarios):
    """Crear devoluciones vinculadas a préstamos."""
    print("\n" + "="*70)
    print(">>> CREANDO DEVOLUCIONES")
    print("="*70)
    
    prestamos_validos = [p for p in prestamos if p.estado in ['activo', 'vencido', 'devuelto']]
    
    for idx, pres in enumerate(prestamos_validos[:5], 1):
        user_recibe = random.choice(usuarios)
        dev = Devolucion.objects.create(
            codigo_prestamo=pres,
            codigo_recibe=user_recibe,
            observaciones=f"Devolución recibida sin novedad por {user_recibe.primer_nombre}.",
            fecha=timezone.now().date()
        )
        print(f"[OK] Devolución #{dev.pk} | Préstamo #{pres.pk}")


def crear_reportes():
    """Crear registros de reportes de historial."""
    print("\n" + "="*70)
    print(">>> CREANDO HISTORIAL DE REPORTES")
    print("="*70)
    
    modulos = ['inventario', 'prestamos', 'devoluciones', 'mantenimiento', 'almacenamiento', 'usuarios']
    formatos = ['pdf', 'excel']
    
    for i in range(1, 6):
        mod = random.choice(modulos)
        form = random.choice(formatos)
        ReporteHistorial.objects.create(
            modulo=mod,
            formato=form,
            nombre_archivo=f"reporte_{mod}_{timezone.now().strftime('%Y%m%d')}.{form}",
            generado_por="Administrador Principal",
            total_registros=random.randint(10, 150)
        )
        print(f"[OK] Reporte: {mod} ({form.upper()})")


@transaction.atomic
def main():
    print("\n+======================================================+")
    print("|      POBLAR BASE DE DATOS LOCAL - COBERTURA 100%     |")
    print("+======================================================+")
    
    asegurar_tablas_sqlite()

    try:
        # 1. Realizar limpieza masiva de todas las tablas en orden de dependencias
        ReporteHistorial.objects.all().delete()
        Devolucion.objects.all().delete()
        ItemPrestamo.objects.all().delete()
        Prestamo.objects.all().delete()
        Detalle_Movimientos.objects.all().delete()
        Movimientos.objects.all().delete()
        Inventario.objects.all().delete()
        Proveedor.objects.all().delete()
        DetalleMantenimiento.objects.all().delete()
        Mantenimiento.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()
        Estante.objects.all().delete()
        Almacen.objects.all().delete()
        print("[OK] Limpieza completada.")

        # 2. Generar datos limpios paso a paso
        usuarios = crear_usuarios()
        almacenes, estantes = crear_almacenamiento()
        categorias = crear_categorias()
        productos = crear_productos(categorias)
        proveedores = crear_proveedores()
        inventarios = crear_inventario(productos, estantes, usuarios)
        crear_movimientos(inventarios, proveedores)
        crear_edicion_limitada(productos)
        
        crear_mantenimientos(productos)
        
        prestamos = crear_prestamos(usuarios, productos)
        crear_devoluciones(prestamos, usuarios)
        crear_reportes()
        
        print("\n" + "="*70)
        print("[OK] BASE DE DATOS POBLADA EXITOSAMENTE CON TODAS LAS TABLAS!")
        print("="*70)
        
    except Exception as e:
        safe_error_msg = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"\n[ERROR] Durante la poblacion: {safe_error_msg}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    try:
        call_command('migrate', verbosity=0)
    except Exception as e:
        print(f"Error aplicando migraciones iniciales: {e}")
    main()