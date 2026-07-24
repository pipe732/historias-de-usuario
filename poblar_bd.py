#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script completo para poblar la base de datos con gran cantidad de datos reales y detallados.
Cubre todos los módulos: Usuarios, Almacenamiento, Categorías, Productos, Inventario,
Movimientos, Proveedores, Mantenimiento, Préstamos, Devoluciones y Reportes.
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta, time
from decimal import Decimal

# Forzar codificación utf-8 en la salida de consola
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Configurar entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session

# Importar modelos de la aplicación
from usuario.models import Usuario
from almacenamiento.models import Almacen, Estante
from inventario.models import Categoria, Producto, Proveedor as ProveedorInventario, Inventario, Movimientos, Detalle_Movimientos, Edicion_limitada
from mantenimiento.models import TipoEstado, TipoMantenimiento, Mantenimiento, DetalleMantenimiento
from prestamo.models import Prestamo, ItemPrestamo
from devoluciones.models import Devolucion
from reportes.models import ReporteHistorial
from configuracion.models import ConfiguracionSistema

try:
    from provedores.models import Proveedor as ProveedorApp, Trabajador
    HAS_PROVEDORES_APP = True
except Exception:
    HAS_PROVEDORES_APP = False


def obtener_documentos_activos():
    """Obtiene los números de documento de usuarios con sesión activa."""
    documentos_activos = set()
    for session in Session.objects.all():
        try:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id') or data.get('usuario_documento')
            if user_id:
                documentos_activos.add(str(user_id))
        except Exception:
            pass
    return documentos_activos


def crear_usuarios():
    """Crea un grupo extenso de usuarios con roles y datos reales del SENA."""
    print("\n" + "="*75)
    print(" 1. CREANDO USUARIOS")
    print("="*75)

    docs_activos = obtener_documentos_activos()
    print(f"   [i] Documentos con sesión activa detectados: {docs_activos}")

    # 1. Administrador Principal (no eliminar ni modificar credenciales)
    admin_doc = '0000000000'
    admin_user, _ = Usuario.objects.get_or_create(
        numero_documento=admin_doc,
        defaults={
            'tipo_documento': 'CC',
            'nombre_completo': 'Administrador Principal',
            'correo': 'admin@mineinventory.com',
            'rol': 'Administrador',
            'password': make_password('@dmin123'),
            'telefono': '3000000000',
            'numero_ficha': 'ADMIN-001',
            'nombre_programa': 'Gestión de Minería e Inventarios'
        }
    )
    print(f"   [OK] Admin asegurado: {admin_doc} (Admin Principal)")

    # 2. Administrador Secundario
    admin2_doc = '1052390443'
    admin2_user, _ = Usuario.objects.get_or_create(
        numero_documento=admin2_doc,
        defaults={
            'tipo_documento': 'CC',
            'nombre_completo': 'Felipe Instructor Administrador',
            'correo': 'felipe.admin@sena.edu.co',
            'rol': 'Administrador',
            'password': make_password('123456'),
            'telefono': '3158901234',
            'numero_ficha': 'ADMIN-002',
            'nombre_programa': 'Supervisión Minera'
        }
    )
    print(f"   [OK] Admin 2 asegurado: {admin2_doc} - Felipe Instructor")

    # Limpiar usuarios anteriores que no estén activos ni sean los admins principales
    excluidos = ['0000000000', '1052390443'] + list(docs_activos)
    Usuario.objects.exclude(numero_documento__in=excluidos).delete()

    fichas_opciones = ['2758369', '2827435', '2895642', '2910384', '3021948', '3196477', '3254109', '3341902']
    programas_opciones = [
        'Análisis y Desarrollo de Software (ADSO)',
        'Supervisión de Labores Mineras',
        'Mantenimiento Electromecánico Industrial',
        'Electricidad Industrial',
        'Topografía y Georreferenciación',
        'Soldadura y Ensayos No Destructivos',
        'Gestión Ambiental y Salud Ocupacional',
        'Mecánica Minera y Pesada'
    ]

    nombres_base = [
        ('Víctor', 'Rojas'), ('Carlos', 'Mendoza'), ('María', 'Fernández'),
        ('Ana', 'Gómez'), ('Andrés', 'Castro'), ('Isabella', 'Torres'),
        ('Javier', 'Ramírez'), ('Laura', 'Sánchez'), ('Diego', 'Morales'),
        ('Sofia', 'Vargas'), ('Camilo', 'Herrera'), ('Daniela', 'Ríos'),
        ('Mateo', 'Suárez'), ('Valentina', 'Ortega'), ('Santiago', 'Jiménez'),
        ('Lucía', 'Pineda'), ('Gabriel', 'Nieto'), ('Elena', 'Duarte'),
        ('Nicolás', 'Silva'), ('Mariana', 'Acosta'), ('Alejandro', 'Paredes'),
        ('Paula', 'Bermúdez'), ('David', 'Londoño'), ('Cynthia', 'Moreno')
    ]

    usuarios_creados = [admin_user, admin2_user]

    for i, (nom, ape) in enumerate(nombres_base, start=1):
        doc = f"1055127{i:03d}"
        if doc in docs_activos:
            continue
        correo = f"{nom.lower()}.{ape.lower()}{i}@sena.edu.co"
        rol = 'Administrador' if i <= 3 else 'Usuario'

        usr = Usuario.objects.create(
            numero_documento=doc,
            tipo_documento='CC' if i % 4 != 0 else 'CE',
            nombre_completo=f"{nom} {ape}",
            correo=correo,
            rol=rol,
            password=make_password('123456'),
            telefono=f"310789{i:04d}",
            numero_ficha=random.choice(fichas_opciones),
            nombre_programa=random.choice(programas_opciones)
        )
        usuarios_creados.append(usr)
        print(f"   [OK] Usuario ({rol}): {doc} -- {nom} {ape}")

    return usuarios_creados


def crear_almacenamiento():
    """Crea Almacenes y Estantes de almacenamiento."""
    print("\n" + "="*75)
    print(" 2. CREANDO ALMACENES Y ESTANTES")
    print("="*75)

    almacenes_def = [
        ('Almacén Central - Mina Principal', 'Almacén general de herramientas de excavación y perforación', 800),
        ('Bodega B - Equipos Eléctricos', 'Almacén climatizado para herramientas de poder y diagnóstico', 450),
        ('Bodega C - EPP y Químicos', 'Resguardo de elementos de seguridad, cascos y reactivos', 600),
        ('Taller de Mantenimiento y Calibración', 'Espacio técnico de reparación y ajuste de precisión', 300)
    ]

    almacenes = []
    estantes = []

    for nombre, detalles, cap in almacenes_def:
        alm = Almacen.objects.create(nombre=nombre, detalles=detalles, capacidad=cap)
        almacenes.append(alm)
        print(f"   [OK] Almacen: {nombre} (Capacidad: {cap})")

        prefix = nombre.split(' ')[0][0] + nombre.split(' ')[1][0] if ' ' in nombre else 'AL'
        for k in range(1, 4):
            cod = f"EST-{prefix}-{k:02d}"
            est = Estante.objects.create(
                almacen=alm,
                codigo=cod,
                detalles=f"Estante Nivel {k} en {nombre}",
                capacidad=150
            )
            estantes.append(est)
            print(f"      [OK] Estante: {cod}")

    return almacenes, estantes


def crear_categorias():
    """Crea Categorías de productos."""
    print("\n" + "="*75)
    print(" 3. CREANDO CATEGORIAS")
    print("="*75)

    cats_def = [
        ('Herramientas Manuales', 'Herramientas de percusión, corte y ajuste de uso manual'),
        ('Herramientas Eléctricas', 'Herramientas motorizadas y de alta potencia'),
        ('Elementos de Protección Personal (EPP)', 'Cascos, arneses, botas y mascarillas de seguridad'),
        ('Equipos de Medición y Topografía', 'Teodolitos, niveles láser y multímetros de calibración'),
        ('Seguridad Subterránea y Alumbrado', 'Lámparas mineras, detectores de gas y autorrescatadores'),
        ('Tuberías y Bombeo Industrial', 'Bombas sumergibles, mangueras de alta presión y acoples'),
        ('Maquinaria Pesada y Perforación', 'Perforadoras neumáticas, martillos de fondo y repuestos')
    ]

    categorias = []
    for nom, desc in cats_def:
        cat = Categoria.objects.create(nombre=nom, descripcion=desc)
        categorias.append(cat)
        print(f"   [OK] Categoria: {nom}")

    return categorias


def crear_productos(categorias, almacenes):
    """Crea más de 20 productos mineros e industriales reales."""
    print("\n" + "="*75)
    print(" 4. CREANDO PRODUCTOS")
    print("="*75)

    cat_map = {c.nombre: c for c in categorias}

    prods_def = [
        ('MART-001', 'Martillo Neumático de Perforación', 'Martillo de perforación pesada 25kg para mina subterránea', 18, 'Maquinaria Pesada y Perforación', 'SN-MART-1092'),
        ('TALD-20V', 'Taladro Percutor DeWalt 20V XR', 'Taladro percutor con 2 baterías de litio 5Ah y cargador', 14, 'Herramientas Eléctricas', 'SN-TALD-8831'),
        ('CASC-LED', 'Casco Minero con Lámpara LED Reorganizadora', 'Casco de seguridad ANSI Z89.1 con lámpara inalámbrica 12h', 45, 'Elementos de Protección Personal (EPP)', 'SN-CASC-0012'),
        ('DETE-GAS', 'Detector Multigas 4 Gases MSA Altair 4XR', 'Detector de LEL, O2, CO y H2S con conectividad Bluetooth', 8, 'Seguridad Subterránea y Alumbrado', 'SN-MSA-99211'),
        ('TEOD-DIG', 'Teodolito Digital Topcon DT-209', 'Teodolito digital de precisión 9 segundos con pantalla doble', 5, 'Equipos de Medición y Topografía', 'SN-TOP-44102'),
        ('ESME-45I', 'Esmeril Angular Bosch 4.5" 1000W', 'Esmeriladora angular profesional con guarda de protección', 12, 'Herramientas Eléctricas', 'SN-BOS-7712'),
        ('PICO-MIN', 'Picota Minera 4.5 lbs Forjada', 'Picota forjada en acero al carbono con mango de fibra', 30, 'Herramientas Manuales', 'SN-PICO-3310'),
        ('ARNE-SEC', 'Arnés Anticaídas Multipropósito Dieléctrico', 'Arnés 4 argollas con soporte lumbar y cinta reflectiva', 22, 'Elementos de Protección Personal (EPP)', 'SN-ARN-5521'),
        ('MULT-FLU', 'Multímetro Industrial Fluke 179 TRMS', 'Multímetro digital con medición de temperatura y precisión TRMS', 10, 'Equipos de Medición y Topografía', 'SN-FLU-88301'),
        ('BOMB-SUM', 'Bomba Sumergible de Achique 3HP 220V', 'Bomba para aguas cargadas con sólidos de hasta 25mm', 6, 'Tuberías y Bombeo Industrial', 'SN-BOM-1123'),
        ('PALA-MIN', 'Pala Minera Redonda No. 4', 'Pala forjada con puño metálico y cabo de madera tratada', 35, 'Herramientas Manuales', 'SN-PALA-9901'),
        ('LLAV-EXP', 'Llave de Expansión Heavy Duty 18"', 'Llave ajuste continuo en acero cromo vanadio', 16, 'Herramientas Manuales', 'SN-LLAV-4412'),
        ('AUTO-RESC', 'Autorrescatador de Oxígeno OXY-K Plus 30m', 'Equipo de respiración autónoma de emergencia para minería', 15, 'Seguridad Subterránea y Alumbrado', 'SN-OXY-66321'),
        ('CINC-COR', 'Juego de Cinceles y Cortafríos Industriales x6', 'Cinceles de acero cromo vanadio empacados en estuche', 25, 'Herramientas Manuales', 'SN-CINC-1102'),
        ('FLEX-50M', 'Cinta Métrica de Fibra de Vidrio 50m Stanley', 'Flexómetro largo graduado en metros y pies', 20, 'Equipos de Medición y Topografía', 'SN-FLEX-2291'),
        ('SIER-SAB', 'Sierra Sable Inalámbrica Milwaukee M18', 'Sierra reciprocante de alto corte para tubería y metal', 7, 'Herramientas Eléctricas', 'SN-MIL-33821'),
        ('BOTA-DIE', 'Botas de Seguridad Dieléctricas de Caucho', 'Botas con puntera de composite y suela antideslizante', 40, 'Elementos de Protección Personal (EPP)', 'SN-BOT-77311'),
        ('MANG-ALT', 'Manguera de Alta Presión 1" x 50m (200 PSI)', 'Manguera reforzada para aire y agua en perforación', 12, 'Tuberías y Bombeo Industrial', 'SN-MAN-55102'),
        ('COMP-NEU', 'Compresor Neumático Portátil 10 HP', 'Compresor de pistón sobre ruedas para herramientas neumáticas', 4, 'Maquinaria Pesada y Perforación', 'SN-COM-9012'),
        ('CALI-PIE', 'Calibrador Pie de Rey Digital 8" Mitutoyo', 'Pie de rey inox digital precisión 0.01mm', 9, 'Equipos de Medición y Topografía', 'SN-MIT-1120')
    ]

    productos = []
    for sku, nom, desc, stock, cat_nom, serie in prods_def:
        cat = cat_map.get(cat_nom, categorias[0])
        alm = random.choice(almacenes)
        prod = Producto.objects.create(
            codigo_sku=sku,
            nombre=nom,
            descripcion=desc,
            stock=stock,
            categoria=cat,
            numero_serie=serie,
            disponible=True,
            ubicacion=alm.nombre
        )
        productos.append(prod)
        print(f"   [OK] [{sku}] {nom} -- Stock: {stock}")

    return productos


def crear_proveedores():
    """Crea proveedores tanto en inventario como en la app provedores."""
    print("\n" + "="*75)
    print(" 5. CREANDO PROVEEDORES")
    print("="*75)

    provs_data = [
        ('NIT-900123456-1', 'Ferretería Industrial del Norte S.A.S', '3151234567', 'ventas@ferreterianorte.com', 'Distribuidor autorizado Stanley, DeWalt y Makita'),
        ('NIT-860987654-2', 'Bosch Tools Colombia S.A.S', '3109876543', 'contacto@bosch-industrial.co', 'Representante directo de herramientas de poder Bosch'),
        ('NIT-800111222-3', 'Seguridad & EPP Minero LTDA', '3201112222', 'servicio@eppseguridad.com', 'Especialista en protección personal, cascos y arneses'),
        ('NIT-901456789-4', 'Equipos Topográficos y Diagnóstico S.A.S', '3004567890', 'info@topografia-col.com', 'Suministro y calibración de teodolitos y sensores MSA'),
        ('NIT-890333444-5', 'Perforación y Maquinaria Minera S.A.', '3183334444', 'ventas@perforacionminera.co', 'Martillos neumático, mangueras y bombas sumergibles')
    ]

    proveedores = []
    for nit, nom_emp, tel, correo, desc in provs_data:
        prov = ProveedorInventario.objects.create(
            nit_proveedor=nit,
            telefono_contacto=tel,
            correo_proveedor=correo,
            descripcion=f"{nom_emp} -- {desc}"
        )
        proveedores.append(prov)
        print(f"   [OK] Proveedor: {nom_emp} (NIT: {nit})")

        if HAS_PROVEDORES_APP:
            try:
                p_app, _ = ProveedorApp.objects.get_or_create(
                    nit=nit,
                    defaults={
                        'nombre_empresa': nom_emp,
                        'telefono': tel,
                        'correo': correo,
                        'direccion': 'Calle 100 # 15-30, Bogotá D.C.',
                        'tipo_servicio': 'Suministros Industriales',
                        'estado': 'Activo',
                        'notas': desc
                    }
                )
                Trabajador.objects.get_or_create(
                    proveedor=p_app,
                    documento=f"9100{random.randint(100, 999)}",
                    defaults={
                        'nombre_completo': f"Asesor {nom_emp.split(' ')[0]}",
                        'telefono': tel,
                        'correo': correo,
                        'cargo': 'Ejecutivo de Cuenta'
                    }
                )
            except Exception:
                pass

    return proveedores


def crear_inventario_y_movimientos(productos, estantes, usuarios, proveedores):
    """Crea registros de inventario físico y movimientos de entrada/salida."""
    print("\n" + "="*75)
    print(" 6. CREANDO INVENTARIOS Y MOVIMIENTOS")
    print("="*75)

    inventarios = []
    for prod in productos:
        est = random.choice(estantes)
        usr = random.choice(usuarios)

        inv = Inventario.objects.create(
            producto=prod,
            id_estante=est.codigo,
            cantidad=prod.stock,
            responsable=usr.nombre_completo,
            observaciones=f"Registro de inventario verificado en estante {est.codigo}"
        )
        inventarios.append(inv)

    print(f"   [OK] Inventario asignado a {len(inventarios)} productos en estantes.")

    # Movimientos de inventario
    tipos_mov = ['entrada', 'salida', 'ajuste']
    for k in range(1, 21):
        inv = random.choice(inventarios)
        prov = random.choice(proveedores) if k % 2 == 0 else None
        tipo = random.choice(tipos_mov)
        cant = random.randint(1, 8)

        mov = Movimientos.objects.create(
            inventario=inv,
            proveedor=prov,
            cantidad=cant,
            tipo_de_movimiento=tipo
        )

        Detalle_Movimientos.objects.create(
            movimiento=mov,
            inventario=inv,
            descripcion=f"Movimiento de {tipo.upper()} por {cant} unidades del producto [{inv.producto.codigo_sku}] {inv.producto.nombre}."
        )

    print("   [OK] 20 movimientos de stock y detalles creados.")

    # Ediciones Limitadas
    for prod in productos[:3]:
        Edicion_limitada.objects.create(
            producto=prod,
            nombre=f"Edición Especial SENA -- {prod.nombre}",
            estado='V',
            observaciones="Lote conmemorativo numerado para formación de aprendices",
            fecha_inicio=timezone.now().date(),
            fecha_fin=timezone.now() + timedelta(days=90)
        )
    print("   [OK] 3 ediciones limitadas creadas.")


def crear_mantenimiento(productos, usuarios):
    """Crea catálogo de mantenimientos, estados y órdenes."""
    print("\n" + "="*75)
    print(" 7. CREANDO MANTENIMIENTOS")
    print("="*75)

    # Tipos de Mantenimiento
    tm_def = [
        ("Mantenimiento Correctivo", "Reparación urgente ante avería o daño en campo", "#E53E3E"),
        ("Mantenimiento Preventivo", "Revisión periódica de lubricación, carbones y ajustes", "#38A169"),
        ("Calibración y Metrología", "Ajuste de sensores de gas y teodolitos con certificación", "#3182CE"),
        ("Reparación Externa Especializada", "Envío a taller especializado del fabricante", "#DD6B20")
    ]
    tipos_mant = []
    for nom, desc, color in tm_def:
        tm = TipoMantenimiento.objects.create(nombre=nom, descripcion=desc, color=color, activo=True)
        tipos_mant.append(tm)

    # Tipos de Estado
    te_def = [
        ('DANADO', 'Dañado / Inoperativo', 'danado', 'no_disponible', 4, '#E53E3E'),
        ('REPARACION', 'En Reparación', 'reparacion', 'no_disponible', 3, '#DD6B20'),
        ('CALIBRACION', 'Calibración Pendiente', 'calibracion', 'disponible_restringido', 2, '#D69E2E'),
        ('OPERATIVO', 'Operativo y Verificado', 'operativo', 'totalmente_disponible', 1, '#38A169')
    ]
    tipos_estado = []
    for cod, nom, cat, imp, niv, color in te_def:
        te = TipoEstado.objects.create(
            codigo=cod,
            nombre=nom,
            categoria=cat,
            impacto_disponibilidad=imp,
            nivel_estado=niv,
            color=color,
            activo=True
        )
        tipos_estado.append(te)

    # Mantenimientos reales
    prioridades = ['baja', 'media', 'alta', 'critica']
    estados_reg = ['abierto', 'en_proceso', 'cerrado']

    for i in range(1, 28):
        prod = random.choice(productos)
        tm = random.choice(tipos_mant)
        te = random.choice(tipos_estado)
        resp = random.choice(usuarios)
        creador = random.choice(usuarios)

        f_rep = timezone.now().date() - timedelta(days=random.randint(2, 45))
        f_ini = f_rep + timedelta(days=random.randint(1, 3))
        f_fin = f_ini + timedelta(days=random.randint(2, 7)) if random.choice([True, False]) else None

        c_est = Decimal(random.randint(80000, 650000))
        c_real = c_est + Decimal(random.randint(-15000, 45000)) if f_fin else None

        m = Mantenimiento.objects.create(
            producto=prod,
            tipo_mantenimiento=tm,
            tipo_estado=te,
            responsable=resp,
            creado_por=creador,
            estado_registro=random.choice(estados_reg),
            prioridad=random.choice(prioridades),
            fecha_reporte=f_rep,
            fecha_inicio=f_ini,
            fecha_fin_estimada=f_ini + timedelta(days=5),
            fecha_fin_real=f_fin,
            tiempo_empleado_horas=Decimal(random.randint(2, 18)) if f_fin else None,
            ubicacion_snapshot=prod.ubicacion,
            costo_estimado=c_est,
            costo_real=c_real
        )

        DetalleMantenimiento.objects.create(
            mantenimiento=m,
            tipo_mantenimiento=tm,
            tipo='diagnostico',
            descripcion=f"Diagnóstico técnico: {random.choice(['Reemplazo de escobillas', 'Limpieza de circuito interno', 'Cambio de manguera de presión', 'Ajuste de óptica y pantalla', 'Inspección de fugas de gas'])} en {prod.nombre}.",
            registrado_por=creador
        )

    print("   [OK] 27 mantenimientos con diagnósticos registrados.")


def crear_prestamos_y_devoluciones(usuarios, productos):
    """Crea un historial denso de préstamos y devoluciones totales/parciales."""
    print("\n" + "="*75)
    print(" 8. CREANDO PRESTAMOS Y DEVOLUCIONES")
    print("="*75)

    motivos = [
        "Prácticas de perforación en socavón de prueba",
        "Medición topográfica y levantamiento de planos",
        "Mantenimiento de tubería de agua y aire comprimido",
        "Capacitación en soldadura y corte industrial",
        "Inspección de seguridad y concentración de gases",
        "Instalación de red eléctrica en taller de maquinaria",
        "Prácticas formativas de la ficha en el centro de minería"
    ]

    prestamos = []

    # 1. Préstamos con distintos estados
    config_prestamos = [
        ('activo', 12),
        ('vencido', 8),
        ('pendiente', 6),
        ('devuelto', 10),
        ('rechazado', 4)
    ]

    for est, cant in config_prestamos:
        for k in range(cant):
            usr = random.choice(usuarios)
            mot = random.choice(motivos)

            f_pres = timezone.now() - timedelta(days=random.randint(1, 20))
            if est == 'vencido':
                f_venc = timezone.localdate() - timedelta(days=random.randint(1, 6))
            else:
                f_venc = timezone.localdate() + timedelta(days=random.randint(2, 12))

            pres = Prestamo.objects.create(
                usuario=usr.numero_documento,
                nombre_usuario=usr.nombre_completo,
                observaciones=f"Solicitud registrada por {usr.nombre_completo}",
                motivo_solicitud=mot,
                motivo_rechazo="Solicitud incompleta o herramientas no disponibles en stock" if est == 'rechazado' else "",
                estado=est,
                fecha_prestamo=f_pres,
                fecha_vencimiento=f_venc,
                hora_max_entrega=time(17, 0)
            )

            # Agregar 1 a 4 herramientas por préstamo
            selected_prods = random.sample(productos, random.randint(1, 4))
            for p in selected_prods:
                dev_val = (est == 'devuelto')
                ItemPrestamo.objects.create(
                    prestamo=pres,
                    producto=p,
                    cantidad=random.randint(1, 3),
                    serial_entregado=f"SR-{p.codigo_sku}-{random.randint(1000, 9999)}",
                    devuelto=dev_val
                )

            prestamos.append(pres)

    print(f"   [OK] {len(prestamos)} préstamos creados (Activos, Vencidos, Pendientes, Devueltos, Rechazados).")

    # 2. Devoluciones
    devs_creadas = 0
    prestamos_para_dev = [p for p in prestamos if p.estado in ['activo', 'vencido', 'devuelto']]

    for p in prestamos_para_dev:
        es_total = random.choice([True, True, False])
        est_dev = random.choice(['aprobada', 'aprobada', 'pendiente', 'rechazada'])

        dev = Devolucion.objects.create(
            prestamo=p,
            devolucion_total=es_total,
            motivo="Devolución de herramientas al finalizar jornada de formación minera",
            estado=est_dev
        )

        items_prestamo = list(p.items.all())
        items_a_devolver = items_prestamo if es_total else items_prestamo[:max(1, len(items_prestamo)//2)]

        for item in items_a_devolver:
            dev.items.add(item)

        if est_dev == 'aprobada':
            dev.aplicar()

        devs_creadas += 1

    print(f"   [OK] {devs_creadas} devoluciones (Totales y Parciales) registradas con aplicación de stock.")


def crear_reportes_y_configuracion():
    """Crea registros en el historial de reportes y configuración del sistema."""
    print("\n" + "="*75)
    print(" 9. HISTORIAL DE REPORTES Y CONFIGURACION")
    print("="*75)

    modulos = ['inventario', 'prestamos', 'devoluciones', 'mantenimiento', 'almacenamiento', 'usuarios']
    formatos = ['excel', 'pdf']

    for j in range(1, 16):
        mod = random.choice(modulos)
        form = random.choice(formatos)
        ReporteHistorial.objects.create(
            modulo=mod,
            formato=form,
            nombre_archivo=f"reporte_{mod}_{timezone.now().strftime('%Y%m%d')}_{j:02d}.{form}",
            generado_por="Administrador Principal",
            total_registros=random.randint(15, 240)
        )

    print("   [OK] 15 registros de historial de exportaciones creados.")

    # Configuración del sistema
    ConfiguracionSistema.objects.get_or_create(
        id=1,
        defaults={
            'almacenamiento': 'local',
            'database_url': 'sqlite:///db.sqlite3'
        }
    )
    print("   [OK] Configuración del sistema verificada.")


@transaction.atomic
def main():
    print("\n" + "="*75)
    print("   MINE INVENTORY -- POBLADO MASIVO COMPLETO DE BASE DE DATOS")
    print("="*75)

    try:
        # 1. Limpieza ordenada
        print("\n [i] Limpiando registros antiguos...")
        ReporteHistorial.objects.all().delete()
        Devolucion.objects.all().delete()
        ItemPrestamo.objects.all().delete()
        Prestamo.objects.all().delete()
        Edicion_limitada.objects.all().delete()
        Detalle_Movimientos.objects.all().delete()
        Movimientos.objects.all().delete()
        Inventario.objects.all().delete()
        ProveedorInventario.objects.all().delete()
        DetalleMantenimiento.objects.all().delete()
        Mantenimiento.objects.all().delete()
        TipoMantenimiento.objects.all().delete()
        TipoEstado.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()
        Estante.objects.all().delete()
        Almacen.objects.all().delete()
        print("   [OK] Limpieza previa de tablas completada.")

        # 2. Generación secuencial de datos
        usuarios = crear_usuarios()
        almacenes, estantes = crear_almacenamiento()
        categorias = crear_categorias()
        productos = crear_productos(categorias, almacenes)
        proveedores = crear_proveedores()
        crear_inventario_y_movimientos(productos, estantes, usuarios, proveedores)
        crear_mantenimiento(productos, usuarios)
        crear_prestamos_y_devoluciones(usuarios, productos)
        crear_reportes_y_configuracion()

        print("\n" + "="*75)
        print(" [ÉXITO] BASE DE DATOS POBLADA EXITOSAMENTE EN TODOS LOS MÓDULOS ")
        print("="*75 + "\n")

    except Exception as e:
        safe_msg = str(e).encode('ascii', 'replace').decode('ascii')
        print(f"\n[ERROR] Durante el poblado: {safe_msg}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
