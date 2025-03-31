from django.shortcuts import render, redirect
from controls.forms import (
    FormSignup,
    FormSignin
)
from django.http import HttpResponse

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
            formset.authenticate_and_log()
            
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
        
