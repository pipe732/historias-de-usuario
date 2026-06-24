from django.urls import path
from . import views


app_name = 'inventario'

urlpatterns = [
    path('', views.inventario, name='inventario'),
    path('detalle/', views.lista_inventario_detalle, name='lista_inventario_detalle'),
    path('movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
]