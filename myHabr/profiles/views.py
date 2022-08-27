import sys

sys.path.append('..')

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Profile, LikeProfile
from .forms import ProfileForm
from authapp.models import MyHabrUser
from django.db.models import F

# Create your views here.

def profile(request, id_profile, user):
    # Получаем объект пользователя к которому заходим в профиль. И его профиль
    reg_user = MyHabrUser.objects.get(id=user)
    reg_profile = Profile.objects.get(user_id=reg_user)

    # Получаем объект пользователя к которому заходим в профиль.
    user = MyHabrUser.objects.get(id=id_profile)
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

    # Находим делал ли лайк зарег профиль профилю к которому зашел
    try:
        like = LikeProfile.objects.get(who_did=user, to_whom_did=id_profile)
    except:
        true_like = False
    # Если зарег пользователь лайкал профиль автора то мы определяем был ли это лайк или нет
    else:
        if like.how == 'L':
            true_like = True
        else:
            true_like = False

    context = {
        'profile': profile, 'name': name, 'profile_id': user, 'reg_profile': reg_profile, 'true_like': true_like,
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
        return render(request=request, template_name='create_update_profile.html', context=context)


def profile_like(request, who_id, whom_id):
    # Получаем объект пользователя кому ставят лайк
    user_whom_id = MyHabrUser.objects.get(id=whom_id)
    # Получаем объект пользователя кто ставит лайк
    user_who_id = MyHabrUser.objects.get(id=who_id)

    # Получаем из БД данные профиля
    profile = Profile.objects.get(user_id=user_whom_id)
    profile_like = profile.likes
    profile_dislike = profile.dislikes

    try:
        like = LikeProfile.objects.get(who_did=user_who_id, to_whom_did=user_whom_id)
    except:
        like = LikeProfile.objects.create(who_did=user_who_id, to_whom_did=user_whom_id, how='N')
    # Если все же пользователь делал лайк автору то мы определяем что он до этого сделал И меняем количество лайков соответственно тому что нажал пользователь.
    if like.how == 'L':

        if profile_like - 1 < 0:
            profile.likes = 0
        else:
            profile.likes = profile_like - 1
        profile.save()

        like.how = 'N'
        like.save()
        print(f'{like.how} сейчас такой статус из L')
        return HttpResponseRedirect(reverse('profiles:profile', args=[whom_id, who_id]))

    if like.how == 'D':

        if profile_dislike - 1 < 0:
            profile.dislikes = 0
        else:
            profile.dislikes = profile_dislike - 1
        profile.likes = profile.likes + 1
        profile.save()

        like.how = 'L'
        like.save()
        print(f'{like.how} сейчас такой статус из D')
        return HttpResponseRedirect(reverse('profiles:profile', args=[whom_id, who_id]))
    if like.how == 'N':

        profile.likes = profile_like + 1
        profile.save()

        like.how = 'L'
        like.save()
        print(f'{like.how} сейчас такой статус из Т')
        return HttpResponseRedirect(reverse('profiles:profile', args=[whom_id, who_id]))

def profile_dislike(request, who_id, whom_id):
    # Получаем объект пользователя кому ставят лайк
    user_whom_id = MyHabrUser.objects.get(id=whom_id)
    # Получаем объект пользователя кто ставит лайк
    user_who_id = MyHabrUser.objects.get(id=who_id)

    # Получаем из БД данные профиля
    profile = Profile.objects.get(user_id=user_whom_id)
    profile_like = profile.likes
    profile_dislike = profile.dislikes

    try:
        like = LikeProfile.objects.get(who_did=user_who_id, to_whom_did=user_whom_id)
    except:
        like = LikeProfile.objects.create(who_did=user_who_id, to_whom_did=user_whom_id, how='N')
    # Если все же пользователь делал лайк автору то мы определяем что он до этого сделал И меняем количество лайков соответственно тому что нажал пользователь.
    if like.how == 'L':

        if profile_like - 1 < 0:
            profile.likes = 0
        else:
            profile.likes = profile_like - 1
        profile.dislikes = profile_dislike + 1
        profile.save()

        like.how = 'D'
        like.save()
        return HttpResponseRedirect(reverse('profiles:profile', args=[whom_id, who_id]))

    if like.how == 'D':

        if profile_dislike - 1 < 0:
            profile.dislikes = 0
        else:
            profile.dislikes = profile_dislike - 1
        profile.save()

        like.how = 'N'
        like.save()
        return HttpResponseRedirect(reverse('profiles:profile', args=[whom_id, who_id]))
    if like.how == 'N':

        profile.dislikes = profile_dislike + 1
        profile.save()

        like.how = 'D'
        like.save()
        return HttpResponseRedirect(reverse('profiles:profile', args=[whom_id, who_id]))