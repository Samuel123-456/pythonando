from django.urls import path
from mentorados.views import (
    agendar_reuniao,
    escolher_dia,
    mentorados,
    reunioes,
    auth,
)

urlpatterns = [
    path('agendar_reuniao/', view=agendar_reuniao, name='agendar_reuniao'),
    path('escolher_dia/', view=escolher_dia, name='escolher_dia'),
    path('reunioes/', view=reunioes, name='reunioes'),
    path('auth/', view=auth, name='auth_mentorado'),
    path('', view=mentorados, name='mentorados'),
]
