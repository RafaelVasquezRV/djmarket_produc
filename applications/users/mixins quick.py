from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

class AlmacenPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    @login_required
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='ALMACEN').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users_app:user-login'))

class VentasPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    @login_required
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='VENTAS').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users_app:user-login'))

class AdminPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    @login_required
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='ADMINISTRADOR').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('users_app:user-login'))