from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q  # Con Q se combinan condiciones de búsqueda en Django, y pudo usar operadores lógicos para buscar en varios campos de mis modelos
from django.shortcuts import render, redirect
from .models import Empleado, Cargo, Departamento, TipoContrato, Rol
from .forms import EmpleadoForm, CargoForm, DepartamentoForm, ContratoForm, RolForm

# Paginación
from django.core.paginator import Paginator


def home(request):
    data = {
        'title': 'App Nómina de Empleados',
        'description': 'Gestión de nómina de empleados',
        'author': 'Gabriela Andagoya, Daniel Palma , Edwin Pastor',
        'year': 2025,
    }
    return render(request, 'home.html', data)



def signup(request): # Crear cuenta
    
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
        
            try:
                # Register User
                user = User.objects.create_user(username = request.POST["username"], password = request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                # User already exists
                return render(request, 'signup.html', {
                'form': UserCreationForm, 
                'error': 'Username already exists'})
        return render(request, 'signup.html', {
        'form': UserCreationForm, 
        'error': "Passwords do not match"
        })    

@login_required
def signout(request): # Cerrar sesión
    logout(request)
    return redirect('home')
    
def signin(request):  # Acceder a una cuenta
    # Si el usuario ya está autenticado, redirigir a la página de tareas
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username and password do not match'
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def empleado_list(request):
    query = request.GET.get('q', None)
    if query:
        empleados = Empleado.objects.filter(
            Q(nombre__icontains=query) | Q(cedula__icontains=query) 
            | Q(direccion__icontains=query) | Q(sexo__icontains=query) 
            | Q(sueldo__icontains=query) | Q(cargo__descripcion__icontains=query) 
            | Q(departamento__descripcion__icontains=query) | Q(tipo_contrato__descripcion__icontains=query))
    else:
        empleados = Empleado.objects.all()

    paginator = Paginator(empleados, 5)  # 5 empleados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'empleados': page_obj, 'title': 'Listado de empleados'}
    return render(request, 'empleado/list.html', context)

# vista:
@login_required # Decorador para requerir autenticación

def empleado_create(request):
    context={'title':'Ingresar Empleado'}
    print("metodo: ",request.method)
    if request.method == "GET":
        # print("entro por get")

        form = EmpleadoForm()# instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'empleado/create.html', context)
    else:
        #  print("entro por post")
        form = EmpleadoForm(request.POST) # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            # empleado = form.save(commit=False)# lo tiene en memoria
            # empleado.user = request.user
            # empleado.save() # lo guarda en la BD
            return redirect('empleados:empleado_list')
        else:
            context['form'] = form
            return render(request, 'empleado/create.html',context) 
        #return JsonResponse({"message": "voy a crear un doctor"})

@login_required # Decorador para requerir autenticación

def empleado_update(request,id):
   context={'title':'Actualizar Empleado'}
   empleado = Empleado.objects.get(pk=id)
   if request.method == "GET":
      form = EmpleadoForm(instance=empleado)# Con instance rellena el formulario con los datos del empleado
      context['form'] = form
      return render(request, 'empleado/create.html', context)
   else:
      form = EmpleadoForm(request.POST,instance=empleado)
      if form.is_valid():
          form.save()
          return redirect('empleados:empleado_list')
      else:
          context['form'] = form
          return render(request, 'empleado/create.html', context)

@login_required # Decorador para requerir autenticación

def empleado_delete(request,id):
    empleado = None
    try:
        empleado = Empleado.objects.get(pk=id)
        if request.method == "GET":
            context = {'title':'Eliminar Empleado','empleado':empleado,'error':''}
            return render(request, 'empleado/delete.html',context)
        else:
            empleado.delete()
            return redirect('empleados:empleado_list')
    except:
        context = {'title':'Datos del Empleado','empleado':empleado,'error':'Error al eliminar al empleado'}
        return render(request, 'empleado/delete.html',context)

@login_required
def cargo_list(request):
    query = request.GET.get('q', None)
    if query:
        cargos = Cargo.objects.filter(Q(descripcion__icontains=query))
    else:
        cargos = Cargo.objects.all()

    paginator = Paginator(cargos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'cargos': page_obj, 'title': 'Listado de Cargos'}
    return render(request, 'cargo/list.html', context)


@login_required # Decorador para requerir autenticación

def cargo_create(request):
    context = {'title': 'Ingresar Cargo'}
    if request.method == "GET":
        form = CargoForm()  # instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'cargo/create.html', context)
    else:
        form = CargoForm(request.POST)  # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            return redirect('empleados:cargo_list')
        else:
            context['form'] = form
            return render(request, 'cargo/create.html', context)

@login_required # Decorador para requerir autenticación

def cargo_update(request, id):
    context = {'title': 'Actualizar Cargo'}
    cargo = Cargo.objects.get(pk=id)
    if request.method == "GET":
        form = CargoForm(instance=cargo)  # Con instance rellena el formulario con los datos del cargo
        context['form'] = form
        return render(request, 'cargo/create.html', context)
    else:
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid(): # EL is_valid() valida los datos del formulario
            # form.save(commit=False) # lo tiene en memoria
            form.save()
            return redirect('empleados:cargo_list')
        else:
            context['form'] = form
            return render(request, 'cargo/create.html', context)
 
@login_required # Decorador para requerir autenticación
        
def cargo_delete(request, id):
    cargo = None
    try:
        cargo = Cargo.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Cargo a Eliminar', 'cargo': cargo, 'error': ''}
            return render(request, 'cargo/delete.html', context)
        else:
            cargo.delete()
            return redirect('empleados:cargo_list')
    except:
        context = {'title': 'Datos del Cargo', 'cargo': cargo, 'error': 'Error al eliminar el cargo'}
        return render(request, 'cargo/delete.html', context)
    
@login_required # Decorador para requerir autenticación
    
@login_required
def departamento_list(request):
    query = request.GET.get('q', None)
    if query:
        departamentos = Departamento.objects.filter(Q(name__icontains=query))
    else:
        departamentos = Departamento.objects.all()

    paginator = Paginator(departamentos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'departamentos': page_obj, 'title': 'Listado de Departamentos'}
    return render(request, 'departamento/list.html', context)


def departamento_create(request):
    context = {'title': 'Ingresar Departamento'}
    if request.method == "GET":
        form = DepartamentoForm()  # instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'departamento/create.html', context)
    else:
        form = DepartamentoForm(request.POST)  # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            return redirect('empleados:departamento_list')
        else:
            context['form'] = form
            return render(request, 'departamento/create.html', context)

@login_required # Decorador para requerir autenticación

def departamento_update(request, id):
    context = {'title': 'Actualizar Departamento'}
    departamento = Departamento.objects.get(pk=id)
    if request.method == "GET":
        form = DepartamentoForm(instance=departamento)  # Con instance rellena el formulario con los datos del departamento
        context['form'] = form
        return render(request, 'departamento/create.html', context)
    else:
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('empleados:departamento_list')
        else:
            context['form'] = form
            return render(request, 'departamento/create.html', context)

@login_required # Decorador para requerir autenticación
        
def departamento_delete(request, id):
    departamento = None
    try:
        departamento = Departamento.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Eliminar Departamento', 'departamento': departamento, 'error': ''}
            return render(request, 'departamento/delete.html', context)
        else:
            departamento.delete()
            return redirect('empleados:departamento_list')
    except:
        context = {'title': 'Datos del Departamento', 'departamento': departamento, 'error': 'Error al eliminar el departamento'}
        return render(request, 'departamento/delete.html', context)


@login_required
def contrato_list(request):
    query = request.GET.get('q', None)
    if query:
        contratos = TipoContrato.objects.filter(Q(descripcion__icontains=query))
    else:
        contratos = TipoContrato.objects.all()

    paginator = Paginator(contratos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'contratos': page_obj, 'title': 'Listado de Tipos de Contrato'}
    return render(request, 'contrato/list.html', context)


@login_required # Decorador para requerir autenticación
def contrato_create(request):
    context = {'title': 'Ingresar Tipo de Contrato'}
    if request.method == "GET":
        form = ContratoForm()  # instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'contrato/create.html', context)
    else:
        form = ContratoForm(request.POST)  # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            return redirect('empleados:contrato_list')
        else:
            context['form'] = form
            return render(request, 'contrato/create.html', context)

@login_required # Decorador para requerir autenticación
def contrato_update(request, id):
    context = {'title': 'Actualizar Tipo de Contrato'}
    contrato = TipoContrato.objects.get(pk=id)
    if request.method == "GET":
        form = ContratoForm(instance=contrato)  # Con instance rellena el formulario con los datos del contrato
        context['form'] = form
        return render(request, 'contrato/create.html', context)
    else:
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect('empleados:contrato_list')
        else:
            context['form'] = form
            return render(request, 'contrato/create.html', context)

@login_required # Decorador para requerir autenticación
def contrato_delete(request, id):
    contrato = None
    try:
        contrato = TipoContrato.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Tipo de Contrato a Eliminar', 'contrato': contrato, 'error': ''}
            return render(request, 'contrato/delete.html', context)
        else:
            contrato.delete()
            return redirect('empleados:contrato_list')
    except:
        context = {'title': 'Datos del Tipo de Contrato', 'contrato': contrato, 'error': 'Error al eliminar el tipo de contrato'}
        return render(request, 'contrato/delete.html', context)

@login_required
def rol_list(request):
    query = request.GET.get('q', None) 
    if query:
        roles = Rol.objects.filter(
            Q(empleado__nombre__icontains=query) | Q(aniomes__icontains=query)
            | Q(sueldo__icontains=query) | Q(horas_extra__icontains=query)
            | Q(bono__icontains=query) | Q(iess__icontains=query)
            | Q(tot_ing__icontains=query) | Q(tot_des__icontains=query)
            | Q(neto__icontains=query)
        )
    else:
        roles = Rol.objects.all()

    paginator = Paginator(roles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'roles': page_obj, 'title': 'Listado de Roles'}
    return render(request, 'roles/list.html', context)


@login_required # Decorador para requerir autenticación
def rol_create(request):
    context = {'title': 'Ingresar Rol'}
    if request.method == "GET":
        form = RolForm()  # instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'roles/create.html', context)
    else:
        form = RolForm(request.POST)  # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            return redirect('empleados:rol_list')
        else:
            context['form'] = form
            return render(request, 'roles/create.html', context)

@login_required # Decorador para requerir autenticación
        
def rol_update(request, id):
    context = {'title': 'Actualizar Rol'}
    rol = Rol.objects.get(pk=id)
    if request.method == "GET":
        form = RolForm(instance=rol)  # Con instance rellena el formulario con los datos del rol
        context['form'] = form
        return render(request, 'roles/create.html', context)
    else:
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            form.save()
            return redirect('empleados:rol_list')
        else:
            context['form'] = form
            return render(request, 'roles/create.html', context)

@login_required # Decorador para requerir autenticación
        
def rol_delete(request, id):
    rol = None
    try:
        rol = Rol.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Rol a Eliminar', 'rol': rol, 'error': ''}
            return render(request, 'roles/delete.html', context)
        else:
            rol.delete()
            return redirect('empleados:rol_list')
    except:
        context = {'title': 'Datos del Rol', 'rol': rol, 'error': 'Error al eliminar el rol'}
        return render(request, 'roles/delete.html', context)
    
