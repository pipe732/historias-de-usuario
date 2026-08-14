# prestamo/signals.py
"""
Signals para el módulo de préstamos.

Conectar en prestamo/apps.py dentro de ready():

    class PrestamoConfig(AppConfig):
        name = 'prestamo'

        def ready(self):
            import prestamo.signals  # noqa: F401
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import Prestamo, ItemPrestamo


# ── Estados que el flujo de negocio controla explícitamente ───────────────
# El signal nunca debe sobreescribir estos estados; solo la vista o el
# administrador tienen autoridad para cambiarlos.
ESTADOS_PROTEGIDOS = {'pendiente', 'rechazado'}


# ── 1. Recalcular estado del préstamo cuando un ítem cambia ────────────────
@receiver(post_save, sender=ItemPrestamo)
def recalcular_estado_en_cambio_item(sender, instance, **kwargs):
    """
    Cada vez que un ItemPrestamo es guardado (devuelto=True/False, cantidad, etc.)
    se recalcula el estado del préstamo padre de forma automática.

    Se usa update_fields internamente para no disparar el signal de nuevo.

    IMPORTANTE: si el préstamo está en 'pendiente' o 'rechazado' el signal
    no lo toca, porque esos estados los gestiona explícitamente la vista de
    aprobación/rechazo.
    """
    try:
        prestamo = instance.prestamo
    except Prestamo.DoesNotExist:
        return

    # No interferir con préstamos pendientes de aprobación ni rechazados
    if prestamo.estado in ESTADOS_PROTEGIDOS:
        return

    items = prestamo.items.all()
    if not items.exists():
        return

    total = items.count()
    try:
        devueltos = items.filter(devuelto=True).count()
    except Exception:
        devueltos = 0

    if devueltos == total and total > 0:
        nuevo = 'devuelto'
    elif devueltos == 0:
        nuevo = 'vencido' if getattr(prestamo, 'esta_vencido', False) else prestamo.estado
    else:
        nuevo = 'parcial'

    if prestamo.estado != nuevo:
        update_fields = {'estado': nuevo}
        if hasattr(prestamo, 'fecha_actualizacion'):
            update_fields['fecha_actualizacion'] = timezone.now()
        Prestamo.objects.filter(pk=prestamo.pk).update(**update_fields)


@receiver(post_delete, sender=ItemPrestamo)
def recalcular_estado_en_borrado_item(sender, instance, **kwargs):
    """Igual que el anterior, pero disparado cuando se elimina un ítem."""
    try:
        prestamo = instance.prestamo
    except Prestamo.DoesNotExist:
        return

    # No interferir con préstamos pendientes de aprobación ni rechazados
    if prestamo.estado in ESTADOS_PROTEGIDOS:
        return

    items = prestamo.items.all()
    if not items.exists():
        return

    total = items.count()
    try:
        devueltos = items.filter(devuelto=True).count()
    except Exception:
        devueltos = 0

    if devueltos == total and total > 0:
        nuevo = 'devuelto'
    elif devueltos == 0:
        nuevo = 'vencido' if getattr(prestamo, 'esta_vencido', False) else prestamo.estado
    else:
        nuevo = 'parcial'

    if prestamo.estado != nuevo:
        update_fields = {'estado': nuevo}
        if hasattr(prestamo, 'fecha_actualizacion'):
            update_fields['fecha_actualizacion'] = timezone.now()
        Prestamo.objects.filter(pk=prestamo.pk).update(**update_fields)


# ── 2. Auto-marcar vencidos al guardar cualquier Prestamo ──────────────────
@receiver(post_save, sender=Prestamo)
def auto_marcar_vencido(sender, instance, created, update_fields, **kwargs):
    """
    Si el préstamo tiene fecha_vencimiento pasada y no está devuelto,
    lo marca como 'vencido' automáticamente en el siguiente save.

    Se ignora cuando el save proviene del propio signal (update_fields=['estado',...])
    para evitar bucles infinitos.

    También se ignora si el préstamo está en un estado protegido.
    """
    # Evitar bucle: si el save ya viene de aquí (solo actualiza estado/fecha)
    if update_fields and set(update_fields) <= {'estado', 'fecha_actualizacion'}:
        return

    # No tocar préstamos pendientes de aprobación ni rechazados
    if instance.estado in ESTADOS_PROTEGIDOS:
        return

    fecha_venc = getattr(instance, 'fecha_vencimiento', None)
    if (
        fecha_venc
        and instance.estado in ('activo', 'parcial')
        and timezone.localdate() > fecha_venc
    ):
        Prestamo.objects.filter(pk=instance.pk).update(
            estado='vencido',
            fecha_actualizacion=timezone.now(),
        )