import sys

sys.path.append('..')

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from authapp.models import MyHabrUser


# Create your views here.

def profile(request, id):
    # Получаем объект пользователя
    user = MyHabrUser.objects.get(id=id)
    # Получаем из БД данные профиля
    profile = Profile.objects.get(user_id=user)
    # Условие если хоть какие то данные заполнены то мы передаем заполненные данные
    # Если имеется имя или фамилия
    if profile.first_name or profile.last_name:
        # Создаем переменную name, которая отразит в тэге title данные.
        name = f'{profile.first_name} {profile.last_name}'
    else:
        # Если таких данных нет то передает False
        name = False

    context = {
        'profile': profile, 'name': name,
    }
    return render(request=request, template_name='profile.html', context=context)


def create_profile(request, id):
    if request.method == 'POST':
        new_profile_for_user = MyHabrUser.objects.get(id=id)

        # При пост запросе получвем данные из формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        text = request.POST.get('text')

        # Применяем данные к объекту
        new_profile = Profile(user_id=new_profile_for_user, first_name=first_name,
                              last_name=last_name, age=age, text=text)
        new_profile.save()

    else:
        return render(request=request, template_name='create_update_profile.html', )


def update_profile(request, id):
    # Получаем объект пользователя
    user = MyHabrUser.objects.get(id=id)
    # Получаем из БД данные профиля
    profile = Profile.objects.get(user_id=user)

    if request.method == 'POST':
        # При пост запросе получвем данные из формы
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        text = request.POST.get('text')

        # Применяем данные к объекту
        profile.first_name = first_name
        profile.last_name = last_name
        profile.age = age
        profile.text = text
        if request.FILES:
            profile.image = request.FILES['image']
        profile.save()

        # Возвращаемся на страницу пользователя
        return HttpResponseRedirect(reverse('profiles:update', args=[id]))

    else:
        # Если имеем Гет запрос загружаем форму
        profile_form = ProfileForm()
        # Устанавливаем имеющиеся значенрия из каждой формы
        profile_form['first_name'].initial = profile.first_name
        profile_form['last_name'].initial = profile.last_name
        profile_form['age'].initial = profile.age
        profile_form['text'].initial = profile.text
        profile_form['image'].initial = profile.image
        context = {
            'profile_form': profile_form,
            'profile_form_url': profile.image
        }
        print(profile_form)
        return render(request=request, template_name='create_update_profile.html', context=context)
