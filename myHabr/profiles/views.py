import sys
sys.path.append('..')

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
# Create your views here.

def profile(request, id):
    # Получаем по ID профиль
    profile = Profile.objects.get(id=id)
    # Условие если хоть какие то данные заполнены то мы передаем заполненные данные
    if profile.first_name or profile.last_name or profile.age or profile.text:
        # Если имеется имя или фамилия
        if profile.first_name or profile.last_name:
            # Создаем переменную name, которая отразит в тэге title данные.
            name = f'{profile.first_name} {profile.last_name}'
        else:
            # Если таких данных нет то передает False
            name = False
        # Обозначает что какие то данные у нас имеються и за место кнопки Внести данные
        # Будет отражаться кнопка Изменить
        fill = True
        context = {
            'profile': profile, 'name': name, 'fill': fill,
        }
    else:
        # Если данные профиля были изменены то мы указываем кнопку Изменить
        if profile.update_profile == True:
            fill = True
        # Будет выводиться кнопка Сохранить новые данные
        else:
            fill = False
        name = False
        context = {
            'profile': profile, 'name': name, 'fill': fill,
        }
    return render(request=request, template_name='profile.html', context=context)

def create_update_profile(request, id, action):
    # Получаем из БД данные профиля
    profile = Profile.objects.get(id=id)
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
        profile.save()

        # Если данные ни разу не сохранялись то мы меняем в столбце update_profile значение с False на True что данные были обновлены
        if profile.update_profile == False:
            profile.update_profile = True
        # Возвращаемся на страницу порльзователя
        return HttpResponseRedirect(reverse('Profile', kwargs={'id': id}))

    else:
        # Если имеем Гет запрос загружаем форму
        profile_form = ProfileForm()
        # profile_form.form_initial(id)
        # Устанавливаем имеющиеся значенрия из каждой формы
        profile_form['first_name'].initial = profile.first_name
        profile_form['last_name'].initial = profile.last_name
        profile_form['age'].initial = profile.age
        profile_form['text'].initial = profile.text

        # Определяем название какой кнопки будет отображатся
        submit = 'update' if action == 'update' else submit = 'create'
        # if action == 'update':
        #     submit = 'update'
        # else:
        #     submit = 'create'

        context = {
            'profile_form': profile_form, 'submit': submit
        }
        return render(request=request, template_name='create_update_profile.html', context=context)


