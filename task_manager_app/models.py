from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATE_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    )

    LABEL_CHOICES = (
        ('trabajo', 'Trabajo'),
        ('hogar', 'Hogar'),
        ('estudio', 'Estudio'),
        # Agrega más etiquetas según tus necesidades
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pendiente')
    label = models.CharField(max_length=20, choices=LABEL_CHOICES, default='trabajo')
    observations = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    def __str__(self):
        return self.title

class Priority(models.Model):
    PRIORITY_CHOICES = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    )

    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='priority')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='baja')

    def __str__(self):
        return f"{self.task.title} - {self.priority}"