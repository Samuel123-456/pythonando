from django.contrib import admin
from mentorados.models import (
    Mentorados, 
    Navegator,
    DisponibilidadeHorarios,
    Reuniao
)

# Register your models here.
admin.site.register((
      Mentorados,
      Navegator,
      DisponibilidadeHorarios,
      Reuniao
))