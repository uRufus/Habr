# Create your views here.
import time

from authapp.forms import MyHabrUserRegisterForm, MyHabrUserLoginForm
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from profiles.models import Profile
from .models import MyHabrUser

# Регистрация пользователя
def register(request):
    title = 'регистрация'
    from_page = request.GET.get('next')
    if request.method == 'POST':
        register_form = MyHabrUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            time.sleep(0.1)
            get_user = MyHabrUser.objects.get(username=request.POST.get('username'),
                                              first_name=request.POST.get('first_name'), email=request.POST.get('email'))
            new_profile = Profile.objects.create(user_id=get_user, first_name=request.POST.get('first_name'))
            if from_page := request.POST.get('from_page'):
                return HttpResponseRedirect(
                    reverse('authapp:login') + '?next=' + from_page)
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = MyHabrUserRegisterForm()

    content = {
        'title': title,
        'register_form': register_form,
        'from_page': from_page
    }

    return render(request, 'authapp/register.html', content)


# Аутентификация пользователя
def login(request):
    from_page = request.GET.get('next')
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
                #return render(request, 'mainapp/index.html', {})

    content = {
        'title': title,
        'login_form': login_form,
        'next': next,
        'from_page': from_page
    }

    return render(request, 'authapp/login.html', content)


# Завершение сессии
def logout(request):
    auth.logout(request)
    #return HttpResponseRedirect(reverse('main'))
    return HttpResponseRedirect('/')

