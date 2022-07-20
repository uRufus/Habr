from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import BlogPost
from .forms import BlogPostForm
# Create your views here.


def index(request):
    context = {
        'title': 'Habr',
    }
    return render(request, 'index.html', context)


class BlogPostView(ListView):
    model = BlogPost
    template_name = "blogpost.html"


class BlogPostDetail(DetailView):
    model = BlogPost
    template_name = "blogpost/blogpost-detail.html"


class BlogPostCreate(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_form.html"
    success_url = reverse_lazy("blogpost")


class BlogPostUpdate(UpdateView):

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_update.html"
    success_url = reverse_lazy("blogpost")

