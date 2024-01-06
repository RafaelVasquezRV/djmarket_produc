#
from django.urls import path
from . import views

app_name = "producto_app"

urlpatterns = [
    path(
        'producto/lista_proveedor/', 
        views.ProviderListView.as_view(),
        name='proveedor-lista',
    ),
    path(
        'producto/agregar_proveedor/', 
        views.ProviderCreateView.as_view(),
        name='provider-add',
    ),
    path(
        'producto/agregar_proveedor/<pk>/', 
        views.ProviderUpdateView.as_view(),
        name='provider-update',
    ),
    path(
        'producto/eliminar_proveedor/<pk>/', 
        views.ProviderDeleteView.as_view(),
        name='provider-delete',
    ),
    path(
        'producto/detalle_proveedor/<pk>/', 
        views.ProviderDetailView.as_view(),
        name='provider-detail',
    ),
    path(
        'producto/detalle_proveedor/print/<pk>/', 
        views.ProviderDetailViewPdf.as_view(),
        name='provider-detail_print',
    ),
    path(
        'producto/lista/', 
        views.ProductListView.as_view(),
        name='producto-lista',
    ),
    path(
        'producto/agregar/', 
        views.ProductCreateView.as_view(),
        name='producto-add',
    ),
    path(
        'producto/agregar/<pk>/', 
        views.ProductUpdateView.as_view(),
        name='producto-update',
    ),
    path(
        'producto/eliminar/<pk>/', 
        views.ProductDeleteView.as_view(),
        name='producto-delete',
    ),
    path(
        'producto/detalle/<pk>/', 
        views.ProductDetailView.as_view(),
        name='producto-detail',
    ),
    path(
        'producto/detalle/print/<pk>/', 
        views.ProductDetailViewPdf.as_view(),
        name='producto-detail_print',
    ),
    path(
        'producto/reporte/', 
        views.FiltrosProductListView.as_view(),
        name='producto-filtros',
    ),
]

handler404 = 'applications.producto.views.error_404'