

# Create your views here.
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post


def home(request):
    postList = Post.objects.filter(visible='1')
    paginator = Paginator(postList, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        "posts": posts,
        "title": "Главная страница блога",
        "desc": "Описание для главной страницы",
        "key": "ключевые, слова",
    }
    return render(request, "index.html", context)

def single(request, id=None):
    post = get_object_or_404(Post, id=id)

    context = {
        "post": post,
    }
    return render(request, "single.html", context)