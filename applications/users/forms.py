from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
#
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'input-group-field',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'input-group-field',
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'email',
            'full_name',
            'ocupation',
            'genero',
            'date_birth',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',
                    'class': 'input-group-field',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres ...',
                    'class': 'input-group-field',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'placeholder': 'Ocupacion ...',
                    'class': 'input-group-field',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'input-group-field',
                },
            ),
        }
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    email = forms.CharField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'Correo Electronico',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    password_current = forms.CharField(
        label='Contraseña actual',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'Contraseña Actual'
            }
        ),
    )
    password_new = forms.CharField(
        label='Nueva contraseña',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'Nueva Contraseña'
            }
        ),
    )
    password_confirm = forms.CharField(
        label='Confirmar nueva contraseña',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-group-field',
                'placeholder': 'Confirmar nueva Contraseña'
            }
        ),
    )
    
    class Meta:        
        model = User        
        
        fields = (
            'email',
            'full_name',
            'ocupation',
            'genero',
            'date_birth',
            'is_active',
        )
            
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',
                    'class': 'input-group-field',
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres ...',
                    'class': 'input-group-field',
                }
            ),
            'ocupation': forms.Select(
                attrs={
                    'placeholder': 'Ocupacion ...',
                    'class': 'input-group-field',
                }
            ),
            'date_birth': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'input-group-field',
                },
            ),
            'is_active': forms.CheckboxInput(
                attrs={
                },
            ),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.ocupation != '0':
            for field in ['ocupation', 'is_active']:
                self.fields[field].widget.attrs['disabled'] = 'disabled'
            # for field in ['password_current', 'password_new', 'password_confirm']:
            for field in [
                'password_current', 
                'password_new', 
                'password_confirm', 
                'email',
                'full_name',
                'genero',
                'date_birth',
                ]:
                if self.instance == user:
                    self.fields[field].widget.attrs['disabled'] = False
                else:
                    self.fields[field].widget.attrs['disabled'] = 'disabled'
        else:
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = False

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance
        
        # Verificar si el usuario inició la sesión tiene el atributo ocupation igual a 0
        if user.ocupation == '0':
            # Permitir la actualización de la contraseña de otros usuarios
            password_current = cleaned_data.get('password_current')
            password_new = cleaned_data.get('password_new')
            password_confirm = cleaned_data.get('password_confirm')
            
            if password_new != password_confirm:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            
            if password_current and password_new and password_confirm:
                if check_password(password_current, user.password):
                    return cleaned_data
                else:
                    raise forms.ValidationError("La contraseña actual no es correcta.")
            
            return cleaned_data
        else:
            # Restringir la actualización de la contraseña de otros usuarios y permitir solo la actualización de la propia contraseña
            password_new = cleaned_data.get('password_new')
            password_confirm = cleaned_data.get('password_confirm')
            
            if password_new != password_confirm:
                raise forms.ValidationError("Las contraseñas no coinciden.")
            
            if password_new:
                return cleaned_data

            # Si el usuario no tiene permisos suficientes, se lanza una excepción
            raise forms.ValidationError("No tienes permiso para actualizar la contraseña de otros usuarios.")
            
        # return cleaned_data   


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )