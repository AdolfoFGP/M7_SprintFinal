# Modulo 7: Acceso a Datos en Aplicaciones Python Django - Individual - Sprint Final
Tomando como base el proyecto que ha desarrollado como ABP individual, considere agregar la siguientes
funcionalidades:
− Asignar tareas a otros usuarios, para lo que deberá realizar las siguientes modificaciones:
− En vista Creación, permitir que el usuario seleccione el usuario al que se le asignará la
tarea.
− Al guardar la nueva Tarea, deberá almacenar el usuario seleccionado y no el usuario actual.
− Priorización de Tareas, para lo que deberás realizar lo siguiente:
− Crear el modelo correspondiente de Prioridades, para permitir que éstas sean dinámicas.
− Realizar la migración correspondiente.
− Agregar el modelo a la gestión de entidades de la administración de Django, para que,
desde ahí, los superuser puedan realizar las modificaciones que se estimen necesarias.
− En vista Creación, permitir que los usuarios seleccionen la prioridad, la que deberá
guardarse junto con los otros datos.
− En vista Visualización, desplegar cuál es la prioridad de la tarea, ojalá de forma destacada.
− En vista Edición, permitir que los usuarios puedan cambiar la prioridad. Se debe guardar
el valor junto con los otros datos del registro.
− En vista Listado, agregar la columna prioridad a la tabla de despliegue.
