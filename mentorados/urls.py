from django.urls import path
from mentorados.views import (
    mentorados
)

urlpatterns = [
    path('', view=mentorados, name='mentorados')
]
