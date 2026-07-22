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

# Importar todos los modelos del proyecto
from usuario.models import Usuario
from almacenamiento.models import Almacen, Estante
from inventario.models import Categoria, Producto, Proveedor, Inventario, Movimientos, Detalle_Movimientos, Edicion_limitada
from mantenimiento.models import TipoEstado, TipoMantenimiento, Mantenimiento, DetalleMantenimiento
from prestamo.models import Prestamo, ItemPrestamo
from devoluciones.models import Devolucion
from reportes.models import ReporteHistorial
from django.contrib.auth.hashers import make_password


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
    admin, _ = Usuario.objects.get_or_create(
        numero_documento=admin_doc,
        defaults={
            'tipo_documento': 'CC',
            'nombre_completo': 'Administrador Principal',
            'correo': 'admin@mineinventory.com',
            'rol': 'Administrador',
            'password': make_password('@dmin123'),
            'telefono': '3000000000',
            'numero_ficha': 'ADMIN-001',
            'nombre_programa': 'Administración'
        }
    )
    print(f"[OK] Admin creado: {admin_doc}")

    # Limpiar otros usuarios que no tengan sesión activa para evitar inconsistencias
    docs_activos = obtener_documentos_activos()
    excluidos = ['0000000000'] + list(docs_activos)
    Usuario.objects.exclude(numero_documento__in=excluidos).delete()

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
            numero_documento=doc,
            tipo_documento='CC',
            nombre_completo=f'{nombre} {apellido}',
            correo=correo,
            rol='Usuario',
            password=make_password('Contra123*'),
            telefono=f'310000{idx:04d}',
            numero_ficha=random.choice(fichas_opciones),
            nombre_programa=random.choice(programas_opciones)
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
        ('Almacén A - Principal', 'Almacén general de herramientas manuales', 500),
        ('Almacén B - Eléctricos', 'Bodega especializada en herramientas de poder', 200),
        ('Almacén C - Reactivos y Seguridad', 'Almacén de EPP y equipos químicos', 300)
    ]
    
    almacenes = []
    estantes = []
    for nombre, detalles, cap in almacenes_datos:
        alm = Almacen.objects.create(nombre=nombre, detalles=detalles, capacidad=cap)
        almacenes.append(alm)
        print(f"[OK] Almacén: {nombre}")
        
        for i in range(1, 4):
            codigo_estante = f"EST-{nombre.split(' ')[1]}-{i}"
            est = Estante.objects.create(
                almacen=alm,
                codigo=codigo_estante,
                detalles=f"Estante {i} en {nombre}",
                capacidad=100
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
        ('MART-001', 'Martillo de Goma', 'Martillo profesional anti-rebote', 35, 'Herramientas Manuales'),
        ('TALD-20V', 'Taladro Inalámbrico 20V', 'Taladro percutor compacto de 20V', 12, 'Herramientas Eléctricas'),
        ('CASC-001', 'Casco de Seguridad', 'Casco de protección ANSI clase E', 50, 'Equipos de Seguridad'),
        ('MULT-001', 'Multímetro Digital', 'Multímetro automotriz y profesional', 8, 'Equipos de Medición'),
        ('PINZ-001', 'Pinza Amperimétrica', 'Pinza para medición de corriente alterna', 15, 'Equipos de Medición'),
        ('ESME-001', 'Esmeril Angular 4.5"', 'Esmeriladora angular de alto rendimiento', 6, 'Herramientas Eléctricas'),
    ]
    
    cat_map = {c.nombre: c for c in categorias}
    productos = []
    for sku, nombre, desc, stock, cat_name in datos:
        cat = cat_map.get(cat_name, categorias[0])
        prod = Producto.objects.create(
            codigo_sku=sku,
            nombre=nombre,
            descripcion=desc,
            stock=stock,
            categoria=cat,
            disponible=True,
            ubicacion='Almacén A - Principal'
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
    """Crear inventarios en estantes específicos."""
    print("\n" + "="*70)
    print(">>> CREANDO INVENTARIOS")
    print("="*70)
    
    inventarios = []
    for prod in productos:
        est = random.choice(estantes)
        resp = random.choice(usuarios)
        inv = Inventario.objects.create(
            producto=prod,
            id_estante=est.codigo,
            cantidad=prod.stock,
            responsable=resp.nombre_completo,
            observaciones=f"Inventario físico inicial en {est.codigo}"
        )
        inventarios.append(inv)
        print(f"[OK] Inventario: [{prod.codigo_sku}] {prod.nombre} -> Estante {est.codigo}")
    return inventarios


def crear_movimientos(inventarios, proveedores):
    """Crear movimientos de stock."""
    print("\n" + "="*70)
    print(">>> CREANDO MOVIMIENTOS")
    print("="*70)
    
    tipos = ['entrada', 'salida', 'ajuste']
    for i in range(1, 11):
        inv = random.choice(inventarios)
        prov = random.choice(proveedores) if random.choice([True, False]) else None
        tipo = random.choice(tipos)
        cant = random.randint(2, 10)
        
        mov = Movimientos.objects.create(
            inventario=inv,
            proveedor=prov,
            cantidad=cant,
            tipo_de_movimiento=tipo
        )
        
        Detalle_Movimientos.objects.create(
            movimiento=mov,
            inventario=inv,
            descripcion=f"Movimiento de {tipo} de {cant} unidades del producto {inv.producto.nombre}."
        )
        print(f"[OK] Movimiento #{i} ({tipo}) | {inv.producto.nombre}")


def crear_edicion_limitada(productos):
    """Crear ediciones limitadas de productos."""
    print("\n" + "="*70)
    print(">>> CREANDO EDICIONES LIMITADAS")
    print("="*70)
    
    for prod in productos[:2]:
        ed = Edicion_limitada.objects.create(
            producto=prod,
            nombre=f"Edición Oro - {prod.nombre}",
            estado='V',
            observaciones="Edición especial numerada",
            fecha_inicio=timezone.now().date(),
            fecha_fin=timezone.now() + timedelta(days=60)
        )
        print(f"[OK] Edición Limitada: {ed.nombre} para {prod.nombre}")


def crear_tipos_mantenimiento():
    """Crear tipos de mantenimiento."""
    print("\n" + "="*70)
    print(">>> CREANDO TIPOS DE MANTENIMIENTO")
    print("="*70)
    
    datos = [
        ("Mantenimiento Correctivo", "Reparación de fallas y daños", "#FF4D4D"),
        ("Mantenimiento Preventivo", "Mantenimiento periódico preventivo", "#4CAF50"),
        ("Calibración", "Ajuste de precisión de instrumentos", "#2196F3"),
        ("Reparación Externa", "Servicio técnico tercerizado", "#FF9800"),
    ]
    
    tipos = []
    for nombre, desc, color in datos:
        tipo = TipoMantenimiento.objects.create(nombre=nombre, descripcion=desc, color=color, activo=True)
        tipos.append(tipo)
        print(f"[OK] Tipo: {nombre}")
    return tipos


def crear_tipos_estado():
    """Crear tipos de estado para mantenimiento."""
    print("\n" + "="*70)
    print(">>> CREANDO TIPOS DE ESTADO")
    print("="*70)
    
    datos = [
        ('DANADO', 'Dañado', 'danado', 'no_disponible', '#FF0000'),
        ('REPARACION', 'En Reparación', 'reparacion', 'no_disponible', '#FFA500'),
        ('CALIBRACION', 'Calibración Pendiente', 'calibracion', 'disponible_restringido', '#FFD700'),
        ('PREVENTIVO', 'Mantenimiento Preventivo', 'preventivo', 'parcialmente_disponible', '#4CAF50'),
    ]
    
    tipos = []
    for codigo, nombre, categoria, impacto, color in datos:
        tipo = TipoEstado.objects.create(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            impacto_disponibilidad=impacto,
            color=color,
            nivel_estado=3,
            activo=True
        )
        tipos.append(tipo)
        print(f"[OK] Estado: {codigo} - {nombre}")
    return tipos


def crear_mantenimientos(productos, tipos_estado, tipos_mantenimiento, usuarios):
    """Crear órdenes de mantenimiento y sus detalles."""
    print("\n" + "="*70)
    print(">>> CREANDO MANTENIMIENTOS Y DETALLES")
    print("="*70)
    
    prioridades = ['baja', 'media', 'alta', 'critica']
    estados = ['abierto', 'en_proceso', 'cerrado']
    
    for i in range(1, 26):
        producto = random.choice(productos)
        tipo_estado = random.choice(tipos_estado)
        tipo_mant = random.choice(tipos_mantenimiento)
        responsable = random.choice(usuarios)
        creado_por = random.choice(usuarios)
        
        fecha_reporte = timezone.now().date() - timedelta(days=random.randint(1, 60))
        fecha_inicio = fecha_reporte + timedelta(days=random.randint(1, 5))
        
        mant = Mantenimiento.objects.create(
            pk=i,
            producto=producto,
            tipo_mantenimiento=tipo_mant,
            tipo_estado=tipo_estado,
            estado_registro=random.choice(estados),
            prioridad=random.choice(prioridades),
            fecha_reporte=fecha_reporte,
            fecha_inicio=fecha_inicio,
            responsable=responsable,
            creado_por=creado_por,
            costo_estimado=Decimal(random.randint(50000, 800000)),
        )
        
        DetalleMantenimiento.objects.create(
            mantenimiento=mant,
            tipo_mantenimiento=tipo_mant,
            tipo='diagnostico',
            descripcion=f"Diagnóstico inicial: {random.choice(['Desgaste severo', 'Falla eléctrica', 'Problema mecánico', 'Falta de calibración'])} en {producto.nombre}.",
            registrado_por=creado_por
        )
        print(f"[OK] Mantenimiento #{i:2d} | {producto.nombre[:35]}")


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
            usuario=user.numero_documento,
            nombre_usuario=user.nombre_completo,
            observaciones=f"Préstamo de prueba número {i}",
            motivo_solicitud="Trabajo de campo en el centro de formación",
            estado=est,
            fecha_vencimiento=fecha_venc,
            hora_max_entrega=time(17, 0)
        )
        
        num_items = random.randint(1, 3)
        selected_prods = random.sample(productos, num_items)
        for prod in selected_prods:
            ItemPrestamo.objects.create(
                prestamo=pres,
                producto=prod,
                cantidad=random.randint(1, 2),
                serial_entregado=f"SR-{prod.codigo_sku}-{random.randint(1000, 9999)}",
                devuelto=(est == 'devuelto')
            )
            
        print(f"[OK] Préstamo #{pres.pk} ({est}) | {user.nombre_completo}")
        prestamos.append(pres)
    return prestamos


def crear_devoluciones(prestamos):
    """Crear devoluciones vinculadas a préstamos."""
    print("\n" + "="*70)
    print(">>> CREANDO DEVOLUCIONES")
    print("="*70)
    
    estados = ['pendiente', 'aprobada', 'rechazada']
    prestamos_validos = [p for p in prestamos if p.estado in ['activo', 'vencido']]
    
    for idx, pres in enumerate(prestamos_validos[:4], 1):
        est = random.choice(estados)
        dev = Devolucion.objects.create(
            prestamo=pres,
            devolucion_total=random.choice([True, False]),
            motivo="Devolución rutinaria de fin de formación",
            estado=est
        )
        
        for item in pres.items.all():
            dev.items.add(item)
            
        print(f"[OK] Devolución #{dev.pk} ({est}) | Préstamo #{pres.pk}")


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
    
    try:
        # 1. Realizar limpieza masiva de todas las tablas en orden de dependencias
        print("\n>>> LIMPIANDO BASE DE DATOS...")
        ReporteHistorial.objects.all().delete()
        Devolucion.objects.all().delete()
        ItemPrestamo.objects.all().delete()
        Prestamo.objects.all().delete()
        Edicion_limitada.objects.all().delete()
        Detalle_Movimientos.objects.all().delete()
        Movimientos.objects.all().delete()
        Inventario.objects.all().delete()
        Proveedor.objects.all().delete()
        DetalleMantenimiento.objects.all().delete()
        Mantenimiento.objects.all().delete()
        TipoMantenimiento.objects.all().delete()
        TipoEstado.objects.all().delete()
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
        
        tipos_mant = crear_tipos_mantenimiento()
        tipos_estado = crear_tipos_estado()
        crear_mantenimientos(productos, tipos_estado, tipos_mant, usuarios)
        
        prestamos = crear_prestamos(usuarios, productos)
        crear_devoluciones(prestamos)
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
    main()