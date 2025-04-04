from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django import forms
from .models import User
import re
from django.utils.text import slugify
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    city = forms.ChoiceField(
        required=True,
        choices=[
            ('', 'Selecciona una ciudad'),
            ('bogota', 'Bogotá'),
            ('medellin', 'Medellín'),
            ('cali', 'Cali'),
            ('barranquilla', 'Barranquilla'),
            ('cartagena', 'Cartagena'),
        ]
    )
    address = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'city', 'address', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminar el campo username del formulario ya que lo generaremos automáticamente
        if 'username' in self.fields:
            del self.fields['username']
    
    def generate_username(self, first_name, last_name):
        # Generar un nombre de usuario a partir del nombre y apellido
        if not first_name or not last_name:
            return ""
        
        # Convertir a minúsculas y eliminar acentos
        base_username = slugify(f"{first_name} {last_name}").replace('-', '')
        
        # Verificar si el nombre de usuario ya existe
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            # Si existe, añadir un número al final
            username = f"{base_username}{counter}"
            counter += 1
            
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.city = self.cleaned_data['city']
        user.address = self.cleaned_data['address']
        
        # Generar nombre de usuario automáticamente
        user.username = self.generate_username(user.first_name, user.last_name)
        
        user.user_type = 'customer'  # Por defecto, todos los usuarios registrados son clientes
        
        if commit:
            user.save()
        return user

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este correo electrónico ya está registrado.')
                return render(request, 'shop/register.html', {'form': form})
            
            user = form.save()
            # Usar el nombre completo en el mensaje de éxito
            full_name = f"{user.first_name} {user.last_name}"
            messages.success(request, f'¡Cuenta creada exitosamente para {full_name}! Tu nombre de usuario es: {user.username}')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'shop/register.html', {'form': form})


class AdminLoginView(LoginView):
    template_name = 'shop/admin_login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        # Obtener el usuario autenticado
        user = form.get_user()
        
        # Verificar si el usuario es administrador o empleado
        if user.user_type in ['admin', 'employee']:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            # Si no es admin o empleado, mostrar un mensaje de error
            messages.error(self.request, 'No tienes permisos de administrador o empleado para acceder a esta sección.')
            # No iniciar sesión para usuarios sin permisos
            return self.form_invalid(form)
    
    def get_success_url(self):
        # Mantener la referencia a order_management ya que solo cambiamos la URL, no el nombre de la ruta
        return self.get_redirect_url() or reverse_lazy('order_management')


def admin_login_redirect(request):
    """Redirige a los usuarios a la página de login administrativa o al panel administrativo según corresponda"""
    if request.user.is_authenticated:
        if request.user.user_type in ['admin', 'employee']:
            return redirect('order_management')
        else:
            messages.warning(request, 'No tienes permisos para acceder a esta sección. Esta área es solo para administradores y empleados.')
            return redirect('home')
    else:
        # Guardar la URL a la que el usuario intentaba acceder para redirigirlo después del login
        next_url = request.GET.get('next', '')
        if next_url:
            from django.urls import reverse
            return redirect(f"{reverse('admin_login')}?next={next_url}")
        return redirect('admin_login')