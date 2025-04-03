from django.http import HttpResponse
from django.shortcuts import render, redirect
from controls.forms import (
    FormSignup,
    FormSignin
)
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

# Create your views here.
def signin(request):
    template_name = 'controls/signin.html'
    ctx = {}

    if request.method == 'GET':
        formset = FormSignin()
        ctx['formset'] = formset
        return render(request, template_name, ctx)
    
    if request.method == 'POST':
        formset = FormSignin(request=request, data=request.POST)

        if formset.is_valid():

            username = formset.data.get('username')
            password = formset.data.get('password')

            user = authenticate(request, username=username, password=password)

            if not user:
                messages.error(request, 'User not found!')
                return redirect('signin')
            
            login(request, user)            
            return redirect('mentorados')
        
        return redirect('signin')


def signup(request):
    template_name = 'controls/signup.html'
    ctx = {}

    if request.method == 'GET':
        formset = FormSignup()
        
        ctx['formset'] = formset
        return render(request, template_name, ctx)
    
    if request.method == 'POST':
        formset = FormSignup(request=request, data=request.POST)
        
        if formset.is_valid():
            formset.save()
            return redirect('signin')
        return redirect('signup')
        
def signout(request):
    logout(request)

    if request.user.is_authenticated:
        return HttpResponse()
    
    return redirect('signin')