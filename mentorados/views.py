from django.shortcuts import render

# Create your views here.
def mentorados(request):
    template_name = 'mentorados/mentorados.html'
    ctx = {}

    if request.method == 'POST':
        ...

    if request.method == 'GET':
        return render(request, template_name, ctx)