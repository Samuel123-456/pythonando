from django.contrib import admin
from mentorados.models import (
    Mentorados, 
    Navegator
)

# Register your models here.
admin.site.register((Mentorados, Navegator))