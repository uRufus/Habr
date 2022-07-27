# Create your views here.
from authapp.forms import MyHabrUserRegisterForm, MyHabrUserLoginForm
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Регистрация пользователя
def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = MyHabrUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = MyHabrUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', content)


# Аутентификация пользователя
def login(request):
    title = 'вход'

    login_form = MyHabrUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect('/')
                #return render(request, 'mainapp/base.html', {})

    content = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }

    return render(request, 'authapp/login.html', content)


# Завершение сессии
def logout(request):
    auth.logout(request)
    #return HttpResponseRedirect(reverse('main'))
    return HttpResponseRedirect('/')

