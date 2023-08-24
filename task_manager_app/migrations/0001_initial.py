# Generated by Django 4.1 on 2023-08-24 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("due_date", models.DateField()),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("pendiente", "Pendiente"),
                            ("en_progreso", "En Progreso"),
                            ("completada", "Completada"),
                        ],
                        default="pendiente",
                        max_length=20,
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        choices=[
                            ("trabajo", "Trabajo"),
                            ("hogar", "Hogar"),
                            ("estudio", "Estudio"),
                        ],
                        default="trabajo",
                        max_length=20,
                    ),
                ),
                ("observations", models.TextField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
