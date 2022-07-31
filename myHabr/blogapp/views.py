from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Blogs
from mainapp.models import BlogPost


def mainmyblogs(request):
    postList = BlogPost.objects.filter(author='1')
    # postList = Blogs.objects.filter(user='1')
    paginator = Paginator(postList, 1)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    content = {
        "posts": posts,
        "title": "Мой блог",
        "desc": "Описание страницы",
    }
    return render(request, "blogapp/index.html", content)
