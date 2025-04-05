from django.http import HttpResponse
from django.shortcuts import render, redirect
from mentorados.models import (
    Mentorados,
    Navegator,
    DisponibilidadeHorarios,
    Reuniao,
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from mentorados.auth import valida_token

# Create your views here.
def _total_mentorados():
    st = Mentorados.estagio_choices
    print(st)

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

        # pegando os dados
        data = { v:Mentorados.objects.filter(estagio=k, mentor=request.user).count() for k, v in estagios.items()  }
        
        labels = list(data.keys())
        values = list(data.values())

        ctx['mentorados'] = mentorados
        ctx['navegators'] = navegators
        ctx['estagios'] = estagios
        ctx['data'] = data
        ctx['labels'] = labels
        ctx['values'] = values


        return render(request, template_name, ctx)

def reunioes(request):
    template_name = 'mentorados/reunioes.html'
    ctx = {}

    if request.method == 'POST':
        date_string = request.POST.get('data')
        mentor = request.user
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M")

        disponibilidade = DisponibilidadeHorarios.objects.filter(mentor=mentor).filter(
            data_inicial__gte=(date - timedelta(minutes=50)),
            data_inicial__lte=(date + timedelta(minutes=50)),
        )

        if disponibilidade.exists():
            messages.success(request, 'Você já possui uma reunião em aberto')
            return redirect('reunioes')


        disponibilidade = DisponibilidadeHorarios(
            data_inicial=date,
            mentor=mentor
        )
        disponibilidade.save()


        return redirect('reunioes')
    
    if request.method == 'GET':
        return render(request, template_name, ctx)

def auth(request):
    template_name = 'mentorados/auth_mentorado.html'
    ctx = {}

    if request.method == 'GET':
        return render(request, template_name, ctx)
    if request.method == 'POST':
        token = request.POST.get('token')
        
        if not Mentorados.objects.filter(token=token).exists():
            messages.error(request, 'Não encontrado, verifique o token!')
            return redirect('auth_mentorado')
        

        response = redirect('escolher_dia')
        response.set_cookie('auth_token', token, max_age=3600)

        return response

def escolher_dia(request):
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')
    
    template_name = 'mentorados/escolher_dia.html'
    ctx = {}

    if request.method == 'GET':
        token = request.COOKIES.get('auth_token')
        mentorado = Mentorados.objects.get(token=token)

        disponibilidades = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=datetime.now(),
            agendado=False,
            mentor=mentorado.mentor
        ).values_list('data_inicial', flat=True)

        horarios = []
        for i in disponibilidades:
            month = i.date().strftime('%B')
            week = i.date().strftime('%A')
            date = i.date().strftime('%d-%m-%Y')

            horarios.append( (month, week, date) )

        ctx['horarios'] = list(set(horarios))
        ctx['mentorado'] = mentorado

        return render(request, template_name, ctx)

def agendar_reuniao(request):
    if not valida_token(request.COOKIES.get('auth_token')):
        return redirect('auth_mentorado')
    
    template_name = 'mentorados/agendar_reuniao.html'
    ctx = {}

    if request.method == 'GET':
        date = request.GET.get("date")
        date = datetime.strptime(date, '%d-%m-%Y')
        horarios = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=date,
            data_inicial__lt=date + timedelta(days=1),
            agendado=False
        )

        #{'horarios': horarios, 'tags': Reuniao.tag_choices}
        ctx['horarios'] = horarios
        ctx['tags'] = Reuniao.tag_choices
        return render(request, template_name, ctx)

    if request.method == 'POST':
        ...