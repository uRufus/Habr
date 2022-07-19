from django.shortcuts import render


# Create your views here.

def index(request):
    context = {
        'title': 'Habr',
    }
    return render(request, 'mainapp/index.html', context)
