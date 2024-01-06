# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    View,
)
# local
from applications.venta.models import SaleDetail
from applications.users.mixins import AlmacenPermisoMixin
#
from .models import Product, Provider
from .forms import ProductForm, ProviderForm
from applications.utils import render_to_pdf

# Create your views here.

class ProviderListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/lista-proveedor.html"
    context_object_name = 'proveedores'
    paginate_by = 10

    def get_queryset(self):
        kword = self.request.GET.get("kword", '')
        order = self.request.GET.get("order", '')
        queryset = Provider.objects.buscar_proveedor(kword, order)
        return queryset


class ProviderCreateView(AlmacenPermisoMixin, CreateView):
    template_name = "producto/form_proveedor.html"
    form_class = ProviderForm
    success_url = reverse_lazy('producto_app:proveedor-lista')

class ProviderUpdateView(AlmacenPermisoMixin, UpdateView):
    template_name = "producto/form_proveedor.html"
    model = Provider
    form_class = ProviderForm
    success_url = reverse_lazy('producto_app:proveedor-lista')

class ProviderDeleteView(AlmacenPermisoMixin, DeleteView):
    template_name = "producto/delete-provider.html"
    model = Provider
    success_url = reverse_lazy('producto_app:proveedor-lista')

class ProviderDetailView(AlmacenPermisoMixin, DetailView):
    template_name = "producto/detail-provider.html"
    model = Provider
    success_url = reverse_lazy('producto_app:proveedor-lista')

class ProviderDetailViewPdf(AlmacenPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        proveedor = Provider.objects.get(id=self.kwargs['pk'])
        data = {
            'provider': proveedor,
        }
        pdf = render_to_pdf('producto/detail-provider-print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class ProductListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/lista.html"
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        kword = self.request.GET.get("kword", '')
        order = self.request.GET.get("order", '')
        queryset = Product.objects.buscar_producto(kword, order)
        return queryset

class ProductCreateView(AlmacenPermisoMixin, CreateView):
    template_name = "producto/form_producto.html"
    form_class = ProductForm
    success_url = reverse_lazy('producto_app:producto-lista')

class ProductUpdateView(AlmacenPermisoMixin, UpdateView):
    template_name = "producto/form_producto.html"
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('producto_app:producto-lista')

class ProductDeleteView(AlmacenPermisoMixin, DeleteView):
    template_name = "producto/delete.html"
    model = Product
    success_url = reverse_lazy('producto_app:producto-lista')

class ProductDetailView(AlmacenPermisoMixin, DetailView):
    template_name = "producto/detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        context["ventas_mes"] = SaleDetail.objects.ventas_mes_producto(
            self.kwargs['pk']
        )
        return context

class ProductDetailViewPdf(AlmacenPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        producto = Product.objects.get(id=self.kwargs['pk'])
        data = {
            'product': producto,
            'ventas_mes': SaleDetail.objects.ventas_mes_producto(self.kwargs['pk'])
        }
        pdf = render_to_pdf('producto/detail-print.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class FiltrosProductListView(AlmacenPermisoMixin, ListView):
    template_name = "producto/filtros.html"
    context_object_name = 'productos'

    def get_queryset(self):

        queryset = Product.objects.filtrar(
            kword=self.request.GET.get("kword", ''),
            date_start=self.request.GET.get("date_start", ''),
            date_end=self.request.GET.get("date_end", ''),
            provider=self.request.GET.get("provider", ''),
            marca=self.request.GET.get("marca", ''),
            order=self.request.GET.get("order", ''),
        )
        return queryset
    
def error_404(request, exception=None):
    return render(request, 'home/404.html')