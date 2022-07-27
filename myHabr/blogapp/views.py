from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Blogs


def mainmyblogs(request):
    postList = Blogs.objects.filter(user='1')
    paginator = Paginator(postList, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        "posts": posts,
        "title": "Главная страница блога",
        "desc": "Описание главной страницы",
        "key": "ключевые, слова",
    }
    return render(request, "index1.html", context)
