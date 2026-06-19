#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de ejemplo completos.
Versión corregida y compatible con el modelo actual de Mantenimiento.
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
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction

# Importar modelos
from usuario.models import Usuario
from almacenamiento.models import Almacen, Estante
from inventario.models import Categoria, Producto
from mantenimiento.models import TipoEstado, TipoMantenimiento, Mantenimiento, DetalleMantenimiento
from prestamo.models import Prestamo, ItemPrestamo
from devoluciones.models import Devolucion
from reportes.models import ReporteHistorial


def crear_usuarios():
    """Crear usuario admin y usuarios de prueba."""
    print("\n" + "="*70)
    print("► CREANDO USUARIOS")
    print("="*70)
    
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
    print(f"✓ Admin creado: {admin_doc}")

    nombres_usuarios = [
        ('Juan', 'Pérez'), ('María', 'García'), ('Carlos', 'López'), ('Ana', 'Martínez'),
        ('Roberto', 'González'), ('Sofía', 'Rodríguez'), ('Miguel', 'Hernández'),
        ('Isabella', 'Torres'), ('David', 'Ramírez'), ('Laura', 'Cruz'),
        ('Fernando', 'Morales'), ('Catalina', 'Soto'), ('Pablo', 'Gómez'),
    ]
    
    usuarios = [admin]
    for idx, (nombre, apellido) in enumerate(nombres_usuarios, 1):
        doc = f'1000000{idx:03d}'
        correo = f"{nombre.lower()}.{apellido.lower()}@sena.edu.co"
        
        usuario, _ = Usuario.objects.get_or_create(
            numero_documento=doc,
            defaults={
                'tipo_documento': 'CC',
                'nombre_completo': f'{nombre} {apellido}',
                'correo': correo,
                'rol': 'Usuario',
                'password': make_password('Contra123*'),
                'telefono': f'310000{idx:04d}',
                'numero_ficha': f'FICHA-{idx:05d}',
                'nombre_programa': random.choice(['Minería', 'Construcción', 'Mecánica', 'Electricidad'])
            }
        )
        usuarios.append(usuario)
        print(f"✓ Usuario creado: {doc} - {nombre} {apellido}")
    
    return usuarios


def crear_categorias():
    print("\n" + "="*70)
    print("► CREANDO CATEGORÍAS")
    print("="*70)
    
    nombres = ['Herramientas Manuales', 'Herramientas Eléctricas', 'Equipos de Seguridad',
               'Equipos de Medición', 'Tuberías y Accesorios', 'Suministros de Construcción']
    
    categorias = []
    for nombre in nombres:
        cat, _ = Categoria.objects.get_or_create(nombre=nombre)
        categorias.append(cat)
        print(f"✓ Categoría: {nombre}")
    return categorias


def crear_productos(categorias):
    print("\n" + "="*70)
    print("► CREANDO PRODUCTOS")
    print("="*70)
    
    datos = [
        ('MART-001', 'Martillo de Goma', 'Martillo profesional', 35, 'Herramientas Manuales'),
        ('TALD-20V', 'Taladro Inalámbrico 20V', 'Taladro compacto', 12, 'Herramientas Eléctricas'),
        ('CASC-001', 'Casco de Seguridad', 'Casco ANSI', 50, 'Equipos de Seguridad'),
        ('MULT-001', 'Multímetro Digital', 'Multímetro profesional', 8, 'Equipos de Medición'),
    ]
    
    cat_map = {c.nombre: c for c in categorias}
    productos = []
    for sku, nombre, desc, stock, cat_name in datos:
        cat = cat_map.get(cat_name, categorias[0])
        prod, _ = Producto.objects.get_or_create(
            codigo_sku=sku,
            defaults={
                'nombre': nombre,
                'descripcion': desc,
                'stock': stock,
                'categoria': cat,
                'disponible': True,
                'ubicacion': 'Almacén Principal'
            }
        )
        productos.append(prod)
        print(f"✓ Producto: {sku} - {nombre}")
    return productos


def crear_tipos_mantenimiento():
    print("\n" + "="*70)
    print("► CREANDO TIPOS DE MANTENIMIENTO")
    print("="*70)
    
    datos = [
        ("Mantenimiento Correctivo", "Reparación de fallas", "#FF4D4D"),
        ("Mantenimiento Preventivo", "Mantenimiento programado", "#4CAF50"),
        ("Calibración", "Ajuste y verificación", "#2196F3"),
        ("Reparación Externa", "Enviado a proveedor", "#FF9800"),
    ]
    
    tipos = []
    for nombre, desc, color in datos:
        tipo, _ = TipoMantenimiento.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': desc, 'color': color, 'activo': True}
        )
        tipos.append(tipo)
        print(f"✓ Tipo: {nombre}")
    return tipos


def crear_tipos_estado():
    print("\n" + "="*70)
    print("► CREANDO TIPOS DE ESTADO")
    print("="*70)
    
    datos = [
        ('DANADO', 'Dañado', 'danado', 'no_disponible', '#FF0000'),
        ('REPARACION', 'En Reparación', 'reparacion', 'no_disponible', '#FFA500'),
        ('CALIBRACION', 'Calibración Pendiente', 'calibracion', 'disponible_restringido', '#FFD700'),
        ('PREVENTIVO', 'Mantenimiento Preventivo', 'preventivo', 'parcialmente_disponible', '#4CAF50'),
    ]
    
    tipos = []
    for codigo, nombre, categoria, impacto, color in datos:
        tipo, _ = TipoEstado.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre,
                'categoria': categoria,
                'impacto_disponibilidad': impacto,
                'color': color,
                'nivel_estado': 3,
                'activo': True
            }
        )
        tipos.append(tipo)
        print(f"✓ Estado: {codigo} - {nombre}")
    return tipos


def crear_mantenimientos(productos, tipos_estado, tipos_mantenimiento, usuarios):
    print("\n" + "="*70)
    print("► CREANDO MANTENIMIENTOS Y DETALLES")
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
        
        mant, created = Mantenimiento.objects.get_or_create(
            pk=i,
            defaults={
                'producto': producto,
                'tipo_mantenimiento': tipo_mant,
                'tipo_estado': tipo_estado,
                'estado_registro': random.choice(estados),
                'prioridad': random.choice(prioridades),
                'fecha_reporte': fecha_reporte,
                'fecha_inicio': fecha_inicio,
                'responsable': responsable,
                'creado_por': creado_por,
                'costo_estimado': Decimal(random.randint(50000, 800000)),
            }
        )
        
        if created:
            DetalleMantenimiento.objects.create(
                mantenimiento=mant,
                tipo_mantenimiento=tipo_mant,
                tipo='diagnostico',
                descripcion=f"Diagnóstico inicial: {random.choice(['Desgaste severo', 'Falla eléctrica', 'Problema mecánico', 'Falta de calibración'])} en {producto.nombre}.",
                registrado_por=creado_por
            )
            print(f"✓ Mantenimiento #{i:2d} | {producto.nombre[:35]}")
    
    print(f"\n✓ Total mantenimientos: {Mantenimiento.objects.count()}")


@transaction.atomic
def main():
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + "  POBLAR BASE DE DATOS - VERSIÓN ACTUALIZADA".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        usuarios = crear_usuarios()
        categorias = crear_categorias()
        productos = crear_productos(categorias)
        tipos_mant = crear_tipos_mantenimiento()
        tipos_estado = crear_tipos_estado()
        
        crear_mantenimientos(productos, tipos_estado, tipos_mant, usuarios)
        
        print("\n" + "="*70)
        print("✅ ¡POBLACIÓN COMPLETADA EXITOSAMENTE!")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ Error durante la población: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()