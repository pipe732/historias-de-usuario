# devoluciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Devolucion
from prestamo.models import Prestamo, ItemPrestamo
from common.mixins import sesion_requerida
from inventario.models import Proveedor, Inventario, Movimientos, Detalle_Movimientos
from inventario.forms import ProveedorForm, InventarioForm, MovimientosForm



@sesion_requerida
def lista_inventario_detalle(request):
    """Vista de los registros de Inventario (estantes/cantidades), separada de Producto."""
    registros = Inventario.objects.select_related("producto").all()

    if request.method == "POST":
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro de inventario creado correctamente.")
            return redirect("inventario:lista_inventario_detalle")
        else:
            messages.error(request, "Revisa los datos del formulario.")
    else:
        form = InventarioForm()

    context = {
        "registros": registros,
        "form": form,
    }
    return render(request, "inventario_detalle.html", context)


@sesion_requerida
def lista_movimientos(request):
    movimientos = Movimientos.objects.select_related("inventario", "proveedor").all().order_by("-fecha_movimiento")

    if request.method == "POST":
        form = MovimientosForm(request.POST)
        if form.is_valid():
            movimiento = form.save()

            # Actualiza el stock del producto según el tipo de movimiento
            inv = movimiento.inventario
            if movimiento.tipo_de_movimiento == "entrada":
                inv.cantidad += movimiento.cantidad
            elif movimiento.tipo_de_movimiento == "salida":
                if movimiento.cantidad > inv.cantidad:
                    messages.error(request, "No hay suficiente stock en este inventario para esa salida.")
                    movimiento.delete()
                    return redirect("inventario:lista_movimientos")
                inv.cantidad -= movimiento.cantidad
            inv.save()

            messages.success(request, "Movimiento registrado correctamente.")
            return redirect("inventario:lista_movimientos")
        else:
            messages.error(request, "Revisa los datos del formulario.")
    else:
        form = MovimientosForm()

    context = {
        "movimientos": movimientos,
        "form": form,
    }
    return render(request, "movimientos.html", context)


@sesion_requerida
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()

    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor registrado correctamente.")
            return redirect("inventario:lista_proveedores")
        else:
            messages.error(request, "Revisa los datos del formulario.")
    else:
        form = ProveedorForm()

    context = {
        "proveedores": proveedores,
        "form": form,
    }
    return render(request, "proveedores.html", context)   


@sesion_requerida 
def devoluciones_view(request):
    edit_id = None

    if request.method == 'POST':
        action = request.POST.get('action', 'crear')

        if action == 'crear':
            prestamo_id      = request.POST.get('prestamo_id', '').strip()
            motivo           = request.POST.get('motivo', '').strip()
            devolucion_total = request.POST.get('devolucion_total', 'true') == 'true'
            motivo_requerido = request.POST.get('motivo_requerido', 'true') == 'true'
            items_ids        = request.POST.getlist('items')

            errores = []
            if not prestamo_id:
                errores.append('No se indicó el préstamo.')

            # El motivo solo es obligatorio en devoluciones parciales
            if motivo_requerido and len(motivo) < 10:
                errores.append('El motivo debe tener al menos 10 caracteres.')

            if not items_ids:
                errores.append('Debes seleccionar al menos un ítem.')

            prestamo = None
            if prestamo_id:
                try:
                    prestamo = Prestamo.objects.get(pk=prestamo_id)
                    if prestamo.fecha_vencimiento and prestamo.fecha_vencimiento < timezone.localdate():
                        errores.append('No se puede devolver un préstamo con fecha de vencimiento en el pasado.')
                except Prestamo.DoesNotExist:
                    errores.append('Préstamo no encontrado.')

            if errores:
                for e in errores:
                    messages.error(request, e)
            else:
                prestamo   = get_object_or_404(Prestamo, pk=prestamo_id)
                devolucion = Devolucion.objects.create(
                    prestamo=prestamo,
                    motivo=motivo,
                    devolucion_total=devolucion_total,
                )
                items = ItemPrestamo.objects.filter(pk__in=items_ids, prestamo=prestamo)
                devolucion.items.set(items)

                # Recoger cantidades parciales por ítem
                cantidades = {}
                for item in items:
                    key = f'cantidad_{item.pk}'
                    try:
                        cant = int(request.POST.get(key, item.cantidad))
                        cantidades[item.pk] = max(1, min(cant, item.cantidad))
                    except (ValueError, TypeError):
                        cantidades[item.pk] = item.cantidad

                devolucion.aplicar(cantidades=cantidades)
                messages.success(request, 'Devolución registrada exitosamente.')
                return redirect('devoluciones')

        elif action == 'editar':
            pk           = request.POST.get('devolucion_id')
            instancia    = get_object_or_404(Devolucion, pk=pk)

            # No hay estado que editar, solo motivo
            messages.info(request, f'Devolución #{pk} no editable.')
            return redirect('devoluciones')

    devoluciones = Devolucion.objects.select_related('prestamo').prefetch_related('items__producto').all()

    # Préstamos que aún tienen ítems pendientes de devolución
    prestamos_activos = (
        Prestamo.objects
        .filter(estado__in=['activo', 'parcial', 'vencido'])
        .prefetch_related('items__producto')
        .order_by('-fecha_prestamo')
    )

    context = {
        'edit_id':           edit_id,
        'devoluciones':      devoluciones,
        'prestamos_activos': prestamos_activos,
    }


    return render(request, 'devoluciones.html', context)