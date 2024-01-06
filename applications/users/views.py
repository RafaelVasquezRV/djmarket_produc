from pyexpat.errors import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import (
    View,
    CreateView,
    ListView,
    #UpdateView,
    DeleteView
)

from django.views.generic.edit import (
    FormView,
    UpdateView
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UserUpdateForm,
    UpdatePasswordForm,
)

from .mixins import (AdminPermisoMixin)
#
from .models import User
# 

# Create your views here.

class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:user-lista')

    def form_valid(self, form):
        #
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            full_name=form.cleaned_data['full_name'],
            ocupation=form.cleaned_data['ocupation'],
            genero=form.cleaned_data['genero'],
            date_birth=form.cleaned_data['date_birth'],
        )
        # enviar el codigo al email del user
        return super(UserRegisterView, self).form_valid(form)



class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:index')
    
    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )



class UserUpdateView(UpdateView, AdminPermisoMixin):
    template_name = "users/update.html"
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_app:user-lista')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = UserUpdateForm(self.request.user)
        return context
    
    

    def form_valid(self, form):
        self.object = form.save(commit=False)
        password_new = form.cleaned_data.get('password_new')
        if password_new:
            self.object.set_password(password_new)

        # Comprobar si el usuario tiene permiso para actualizar los datos
        if self.request.user.ocupation == "0" or self.object == self.request.user:
            # Usar update() para actualizar los campos en la base de datos
            User.objects.filter(pk=self.object.pk).update(
                email=self.object.email,
                # first_name=self.object.first_name,
                # last_name=self.object.last_name,
                full_name=self.object.full_name,
                ocupation=self.object.ocupation,
                is_active=self.object.is_active
            )
        elif self.object == self.request.user:
            # Asegurarnos que ocupation e is_active no cambien
            self.object.ocupation = self.request.user.ocupation
            self.object.is_active = self.request.user.is_active
            self.object.save()
        else:
            messages.error(self.request, 'No tienes permiso para actualizar este usuario')
        return super(UserUpdateView, self).form_valid(form)


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users_app:user-lista')

class UpdatePasswordView(LoginRequiredMixin, FormView):
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        usuario = self.request.user
        if usuario.ocupation != "0":
            return HttpResponse("No tienes permiso para cambiar la contraseña de otro usuario")

        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class UserListView(ListView):
    template_name = "users/lista.html"
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.usuarios_sistema()
    
def error_404(request, exception=None):
    return render(request, 'home/404.html')