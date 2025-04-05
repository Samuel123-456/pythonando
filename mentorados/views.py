from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from mentorados.models import (
    DisponibilidadeHorarios,
    Mentorados,
    Navegator,
    Reuniao,
    Tarefa,
    Upload,
)

from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from mentorados.auth import valida_token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


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

        messages.add_message(request, constants.SUCCESS, 'Mentorado Cadastrado com sucesso!')

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
        ctx['labels'] = labels
        ctx['values'] = values
        ctx['data'] = data


        return render(request, template_name, ctx)

@login_required 
def reunioes(request):
    template_name = 'mentorados/reunioes.html'
    ctx = {}

    if request.method == 'GET':
        reunioes = Reuniao.objects.filter(
            data__mentor=request.user
        )

        ctx['reunioes'] = reunioes

        return render(request, template_name, ctx)

    if request.method == 'POST':
        date_string = request.POST.get('data')
        mentor = request.user
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M")

        disponibilidade = DisponibilidadeHorarios.objects.filter(mentor=mentor).filter(
            data_inicial__gte=(date - timedelta(minutes=50)),
            data_inicial__lte=(date + timedelta(minutes=50)),
        )

        if disponibilidade.exists():
            messages.add_message(request, constants.ERROR, 'Você já possui uma reunião em aberto')
            return redirect('reunioes')


        disponibilidade = DisponibilidadeHorarios(
            data_inicial=date,
            mentor=mentor
        ) 
        disponibilidade.save()

        messages.add_message(request, constants.SUCCESS, 'Horário Marcado com Sucesso!')
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
            messages.add_message(request, constants.ERROR, 'Não encontrado, verifique o token!')
            return redirect('auth_mentorado')
        

        response = redirect('tarefa_mentorado')
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
    mentorado = valida_token(request.COOKIES.get('auth_token'))

    if request.method == 'GET':
        date = request.GET.get("date")
        date = datetime.strptime(date, '%d-%m-%Y')

        horarios = DisponibilidadeHorarios.objects.filter(
            data_inicial__gte=date,
            data_inicial__lt=date + timedelta(days=1),
            agendado=False
        )

        #TODO: verificar se o horario que estão acessar é do mentor deste mentorado
        

        ctx['horarios'] = horarios
        ctx['tags'] = Reuniao.tag_choices
        return render(request, template_name, ctx)

    if request.method == 'POST':
        horario_id = request.POST.get('horario')
        tag = request.POST.get('tag')
        descricao = request.POST.get("descricao")

        #TODO: Realizar validações

        reuniao = Reuniao(
            mentorado=mentorado,
            descricao=descricao,
            data_id=horario_id,
            tag=tag,
        )
        reuniao.save()

        horario = DisponibilidadeHorarios.objects.get(id=horario_id)
        horario.agendado = True
        horario.save()

        messages.add_message(request, constants.SUCCESS, 'Reunião agendada com sucesso.')
        return redirect('escolher_dia')

def tarefa(request, id):
    mentorado = Mentorados.objects.get(id=id)
    if mentorado.mentor != request.user:
        raise Http404('Mentorado não partence a este mentor')

    template_name = 'mentorados/tarefa.html'
    ctx = {}

    if request.method == 'POST':
        _tarefa = request.POST.get('tarefa')

        tarefa = Tarefa(mentorado=mentorado, tarefa=_tarefa)
        tarefa.save()

        return redirect(f'/mentorados/tarefa/{mentorado.id}')
    
    if request.method == 'GET':
        tarefas = Tarefa.objects.filter(mentorado=mentorado)
        videos = Upload.objects.filter(mentorado=mentorado)

        ctx['mentorado'] = mentorado
        ctx['tarefas'] = tarefas
        ctx['videos'] = videos
        
        return render(request, template_name, ctx)
    
def upload(request, id):
    mentorado = Mentorados.objects.get(id=id)
    if mentorado.mentor != request.user:
        raise Http404()
    
    video = request.FILES.get('video')
    upload = Upload(
        mentorado=mentorado,
        video=video
    )
    upload.save()
    return redirect(f'/mentorados/tarefa/{mentorado.id}')

def tarefa_mentorado(request):
    mentorado = valida_token(request.COOKIES.get('auth_token'))
    if not mentorado:
        return redirect('auth_mentorado')
    
    template_name = 'mentorados/tarefa_mentorado.html'
    ctx = {}
    if request.method == 'GET':
        videos = Upload.objects.filter(mentorado=mentorado)
        tarefas = Tarefa.objects.filter(mentorado=mentorado)

        ctx['mentorado'] = mentorado
        ctx['tarefas'] = tarefas
        ctx['videos'] = videos

        return render(request, template_name, ctx)

@csrf_exempt
def tarefa_alterar(request, id):
    mentorado = valida_token(request.COOKIES.get('auth_token'))
    if not mentorado:
        return redirect('auth_mentorado')

    tarefa = Tarefa.objects.get(id=id)
    if mentorado != tarefa.mentorado:
        raise Http404()
    tarefa.realizada = not tarefa.realizada
    tarefa.save()

    return HttpResponse('teste')

@login_required
def navegator(request):
    template_name = 'mentorados/navegator.html'
    ctx = {}
    if request.method == 'GET':
        return render(request, template_name, ctx)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        name = name.strip()
        if not name:
            messages.add_message(request, constants.ERROR, 'Nome não informado')
            return redirect('navegator')
        
        if Navegator.objects.filter(name=name).exists():
            messages.add_message(request, constants.ERROR, 'Navegator já existe')
            return redirect('navegator')
        
        navegator = Navegator(
            name=name,
            mentor=request.user
        )
        navegator.save()
        
        messages.add_message(request, constants.SUCCESS, 'Navegator cadastrado com sucesso!')
        return redirect('navegator') 