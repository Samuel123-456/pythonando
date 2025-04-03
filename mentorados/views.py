from django.shortcuts import render, redirect
from mentorados.models import (
    Mentorados,
    Navegator
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def mentorados(request):
    template_name = 'mentorados/mentorados.html'
    ctx = {}

    if request.method == 'POST': # Make it on django forms
        name = request.POST.get('nome')
        photo = request.FILES.get('foto')
        estagio = request.POST.get('estagio')
        navegator_id = request.POST.get('navigator')

        navegator = Navegator.objects.get(id=int(navegator_id))
        
        mentorado = Mentorados(
            name=name,
            foto=photo,
            estagio=estagio,
            navegator=navegator,
            mentor=request.user
        )
        mentorado.save()

        messages.success(request, 'Mentorado Cadastrado com sucesso!')

        return redirect('mentorados')

    if request.method == 'GET':
        mentor = request.user

        mentorados = Mentorados.objects.filter(mentor=mentor)
        navegators = Navegator.objects.filter(mentor=mentor)
        estagios = Mentorados.estagio_choices


        ctx['mentorados'] = mentorados
        ctx['navegators'] = navegators
        ctx['estagios'] = estagios

        return render(request, template_name, ctx)