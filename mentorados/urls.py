from django.urls import path
from mentorados.views import (
    tarefa_mentorado,
    agendar_reuniao,
    tarefa_alterar,
    escolher_dia,
    mentorados,
    navegator,
    reunioes,
    tarefa,
    upload,
    auth,
)

urlpatterns = [
    path('tarefa_alterar/<int:id>', view=tarefa_alterar, name="tarefa_alterar"),
    path('tarefa_mentorado/', view=tarefa_mentorado, name='tarefa_mentorado'),
    path('agendar_reuniao/', view=agendar_reuniao, name='agendar_reuniao'),
    path('escolher_dia/', view=escolher_dia, name='escolher_dia'),
    path('navegator/', view=navegator, name='navegator'),
    path('upload/<int:id>', view=upload, name='upload'),
    path('tarefa/<int:id>', view=tarefa, name='tarefa'),
    path('reunioes/', view=reunioes, name='reunioes'),
    path('auth/', view=auth, name='auth_mentorado'),
    path('', view=mentorados, name='mentorados'),
]
