from django.shortcuts import render, redirect
from django.db.models import Sum, Max
from inventario.models import Producto, Categoria
from django.utils import timezone
from prestamo.models import Prestamo
from devoluciones.models import Devolucion
from django.http import JsonResponse
from django.utils import timezone
#from common.mixins import sesion_requerida 

#@sesion_requerida     
def dashboard_view(request):
    """Home del administrador — solo accesible por admins."""
    import json
    from django.db.models import Count
    # Validar que el usuario sea administrador
    rol = (request.session.get('usuario_rol') or '').strip().lower()
    if rol not in ('administrador', 'admin'):
        return redirect('home_usuario')
    
    # ── Inventario ──
    total_productos  = Producto.objects.count()
    total_categorias = Categoria.objects.count()

    # ── Préstamos estadísticas ──
    prestamos_activos_count   = Prestamo.objects.filter(estado='activo').count()
    prestamos_vencidos_count  = Prestamo.objects.filter(estado='vencido').count()
    prestamos_devueltos_count = Prestamo.objects.filter(estado='devuelto').count()
    prestamos_parciales_count = Prestamo.objects.filter(estado='parcial').count()
    prestamos_recientes       = Prestamo.objects.prefetch_related('items__codigo_herramienta').order_by('-fecha')[:5]

    # ── Devoluciones ──
    devoluciones_pendientes_count = Devolucion.objects.count()
    devoluciones_recientes        = Devolucion.objects.select_related('codigo_prestamo').order_by('-fecha')[:5]

    # ── Stock por categoría ──
    stock_por_categoria = list(
        Categoria.objects
        .annotate(total_stock=Count('herramientas'))
        .order_by('-total_stock')
    )
    max_stock = max([c.total_stock for c in stock_por_categoria], default=1)

    # Datos estructurados para gráficas
    cat_labels = [c.nombre for c in stock_por_categoria[:7]]
    cat_values = [c.total_stock for c in stock_por_categoria[:7]]

    # Salud de Inventario (Disponible / En Préstamo / No disponible)
    herramientas_disponibles = Producto.objects.filter(disponibilidad='Disponible').count()
    if herramientas_disponibles == 0 and total_productos > 0:
        herramientas_disponibles = max(0, total_productos - prestamos_activos_count)
    herramientas_en_prestamo = prestamos_activos_count
    herramientas_no_disponibles = max(0, total_productos - herramientas_disponibles)

    context = {
        'total_productos':                total_productos,
        'total_categorias':               total_categorias,
        'prestamos_activos_count':        prestamos_activos_count,
        'prestamos_vencidos_count':       prestamos_vencidos_count,
        'prestamos_devueltos_count':      prestamos_devueltos_count,
        'prestamos_parciales_count':      prestamos_parciales_count,
        'devoluciones_pendientes_count':  devoluciones_pendientes_count,
        'prestamos_recientes':            prestamos_recientes,
        'devoluciones_recientes':         devoluciones_recientes,
        'stock_por_categoria':            stock_por_categoria,
        'max_stock':                      max_stock,
        # JSON para Chart.js
        'chart_prestamos_json': json.dumps({
            'labels': ['Activos', 'Vencidos', 'Devueltos', 'Parciales'],
            'data': [prestamos_activos_count, prestamos_vencidos_count, prestamos_devueltos_count, prestamos_parciales_count]
        }),
        'chart_categorias_json': json.dumps({
            'labels': cat_labels,
            'data': cat_values
        }),
        'chart_salud_json': json.dumps({
            'labels': ['Disponible', 'En Préstamo', 'No disponible'],
            'data': [herramientas_disponibles, herramientas_en_prestamo, herramientas_no_disponibles]
        })
    }

    return render(request, 'pagina_principal.html', context)


def home_usuario_view(request):
    """Home del usuario — muestra sus propios préstamos."""
    from usuario.models import Usuario

    doc = request.session.get('usuario_documento')
    if not doc:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(documento=doc)
    except Usuario.DoesNotExist:
        return redirect('login')

    # Todos los préstamos del usuario identificado por su documento
    all_prestamos = (
        Prestamo.objects
        .prefetch_related('items__codigo_herramienta')
        .filter(documento=doc)
        .order_by('-fecha')
    )

    total_prestamos    = all_prestamos.count()
    prestamos_activos  = all_prestamos.filter(estado__in=['activo', 'parcial'])
    historial_reciente = all_prestamos.filter(estado='devuelto')
    vencidos_count     = all_prestamos.filter(estado='vencido').count()

    productos_disponibles = Producto.objects.filter(disponibilidad='Disponible').order_by('nombre_herramienta')

    # Alertas de stock bajo / no disponible
    alertas_stock = list(Producto.objects.filter(disponibilidad='No disponible').values_list('nombre_herramienta', flat=True))
    hay_alertas = len(alertas_stock) > 0

    context = {
        'usuario':               usuario,
        'all_prestamos':         all_prestamos,
        'prestamos_activos':     prestamos_activos,
        'historial_reciente':    historial_reciente,
        'total_prestamos':       total_prestamos,
        'vencidos_count':        vencidos_count,
        'productos_disponibles': productos_disponibles,
        'alertas_stock':         alertas_stock,
        'hay_alertas':           hay_alertas,
    }

    return render(request, 'home_usuario.html', context)


# ─────────────────────────────────────────────────────────────
#  NOTIFICACIONES JSON — agregar a pagina_principal/views.py
# ─────────────────────────────────────────────────────────────
def notificaciones_json(request):
    """Devuelve notificaciones activas para el usuario en sesión."""
    doc = request.session.get('usuario_documento')
    rol = (request.session.get('usuario_rol') or '').strip().lower()
    if not doc:
        return JsonResponse({'items': [], 'total': 0})

    hoy      = timezone.localdate()
    proximos = hoy + timezone.timedelta(days=3)
    items    = []

    page = (request.GET.get('page') or '').strip().lower()

    # ── Para admin/administrador: notificaciones globales ────────
    if rol in ('administrador', 'admin'):

        if page not in ('principal', 'inventario'):
            activos = Prestamo.objects.filter(estado__in=['activo', 'parcial']).count()
            if activos:
                items.append({
                    'tipo':  'activo',
                    'icono': 'box-seam',
                    'color': '#1D9E75',
                    'titulo': f'{activos} préstamo{"s" if activos != 1 else ""} activo{"s" if activos != 1 else ""}',
                    'desc':  'Préstamos en curso',
                    'url':   '/prestamo/?estado=activo',
                })

        if page != 'inventario':
            venc = Prestamo.objects.filter(estado='vencido').count()
            if venc:
                items.append({
                    'tipo':  'vencido',
                    'icono': 'exclamation-circle',
                    'color': '#98473E',
                    'titulo': f'{venc} préstamo{"s" if venc != 1 else ""} vencido{"s" if venc != 1 else ""}',
                    'desc':  'Requieren atención inmediata',
                    'url':   '/prestamo/?estado=vencido',
                })

            venc_no_marcados = Prestamo.objects.filter(
                estado__in=['activo', 'parcial'],
                fecha__lt=hoy,
            ).count()
            if venc_no_marcados:
                items.append({
                    'tipo':  'vencido_no_marcado',
                    'icono': 'alarm',
                    'color': '#98473E',
                    'titulo': f'{venc_no_marcados} préstamo{"s" if venc_no_marcados != 1 else ""} con fecha vencida',
                    'desc':  'Activos pero ya pasaron su fecha límite',
                    'url':   '/prestamo/',
                })

        if page not in ('principal', 'inventario'):
            devs = Devolucion.objects.count()
            if devs:
                items.append({
                    'tipo':  'devolucion',
                    'icono': 'arrow-counterclockwise',
                    'color': '#094D92',
                    'titulo': f'{devs} devolución{"es" if devs != 1 else ""} registrada{"s" if devs != 1 else ""}',
                    'desc':  'Revisar en módulo de devoluciones',
                    'url':   '/devoluciones/',
                })

        if page != 'principal':
            productos_sin = list(
                Producto.objects.filter(disponibilidad='No disponible')
                .values_list('nombre_herramienta', flat=True)
                .order_by('nombre_herramienta')
            )
            if productos_sin:
                for nombre in productos_sin:
                    items.append({
                        'tipo':  'stock',
                        'icono': 'box-seam',
                        'color': '#71816D',
                        'titulo': f'{nombre}',
                        'desc':  'No disponible — verificar inventario',
                        'url':   '/inventario/',
                    })

    else:
        # ── Para usuario normal: solo sus préstamos ──────────────
        venc_u = Prestamo.objects.filter(documento=doc, estado='vencido').count()
        if venc_u:
            items.append({
                'tipo':  'vencido',
                'icono': 'exclamation-circle',
                'color': '#98473E',
                'titulo': f'{venc_u} préstamo{"s" if venc_u != 1 else ""} vencido{"s" if venc_u != 1 else ""}',
                'desc':  'Contacta al administrador',
                'url':   '/prestamo/usuario/',
            })

    return JsonResponse({'items': items, 'total': len(items)})