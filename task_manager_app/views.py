from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import TaskForm, TaskFilterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

def login_view(request):
    error_message = None
    if request.method == 'POST':
        # Procesar el formulario de inicio de sesión
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('task_manager_app:welcome')
        else:
            # Mostrar un mensaje de error en la plantilla
            error_message = "Credenciales incorrectas."
    
    return render(request, 'task_manager_app/login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('task_manager_app:welcome')


def welcome_view(request):
    return render(request, 'task_manager_app/welcome.html')

@login_required
def task_list_view(request):
    #tasks = Task.objects.filter(user=request.user).order_by('due_date')
    #tasks = Task.objects.filter(Q(user=request.user) | Q(assigned_to=request.user)).order_by('due_date')
    #tasks = Task.objects.filter(Q(user=request.user) | Q(assigned_to=request.user)).distinct().order_by('due_date')

    
    '''assigned_tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')

    if request.user.is_superuser:
        assigned_tasks = assigned_tasks.exclude(user=request.user)'''

    tasks = Task.objects.filter(Q(user=request.user) & ~Q(assigned_to__isnull=False)).order_by('due_date')
    
    assigned_tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')

    form = TaskFilterForm(request.GET)
    if form.is_valid():
        state = form.cleaned_data['state']
        label = form.cleaned_data['label']

        if state:
            tasks = tasks.filter(state=state)
            assigned_tasks = assigned_tasks.filter(state=state)
        if label:
            tasks = tasks.filter(label=label)
            assigned_tasks = assigned_tasks.filter(label=label)

    # Si se envió el formulario o se hizo clic en "Clear Filter", mostrar todas las tareas
    if request.method == 'GET' and not form.is_bound:
        tasks = Task.objects.filter(user=request.user).order_by('due_date')
        assigned_tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')

    return render(request, 'task_manager_app/task_list.html', {'tasks': tasks, 'assigned_tasks': assigned_tasks, 'form': form})



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_manager_app:login')  # Redirigir al login después de registro exitoso
    else:
        form = UserCreationForm()
    return render(request, 'task_manager_app/register.html', {'form': form})



@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_manager_app:task_list')  # Redirige al listado de tareas
    else:
        form = TaskForm()
    return render(request, 'task_manager_app/task_create.html', {'form': form})

@login_required
def task_delete_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_manager_app:task_list')  # Redirige al listado de tareas
    return render(request, 'task_manager_app/task_delete.html', {'task': task})

@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(Task, pk=pk)

    priority = None
    try:
        priority = Priority.objects.get(task=task)
    except Priority.DoesNotExist:
        pass

    if request.method == 'POST':
        observations = request.POST.get('observations', '')
        task.observations = observations
        task.save()

        priority_choice = request.POST.get('priority', '')
        if priority_choice in [choice[0] for choice in Priority.PRIORITY_CHOICES]:
            if priority:
                priority.priority = priority_choice
                priority.save()
            else:
                Priority.objects.create(task=task, priority=priority_choice)

        return redirect('task_manager_app:assigned_tasks')

    context = {'task': task, 'priority': priority}
    return render(request, 'task_manager_app/task_detail.html', context)

@login_required
def task_edit_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_manager_app:task_list')  # Redirige al listado de tareas
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_manager_app/task_edit.html', {'form': form, 'task': task})

@login_required
def task_complete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.state = 'completada'
    task.save()
    return redirect('task_manager_app:task_list')  # Redirige al listado de tareas


@user_passes_test(lambda u: u.is_superuser)
def assign_task_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = User.objects.get(pk=user_id)
            task.user = request.user  # El superusuario también será el creador
            task.save()
            return redirect('task_manager_app:task_list')  # Redirige al listado de tareas
    else:
        form = TaskForm()
    users = User.objects.all()
    return render(request, 'task_manager_app/assign_task.html', {'form': form, 'users': users})

@user_passes_test(lambda u: u.is_superuser)
def assigned_tasks_view(request):
    assigned_tasks = Task.objects.exclude(assigned_to=None).order_by('due_date')
    return render(request, 'task_manager_app/assigned_tasks.html', {'assigned_tasks': assigned_tasks})
