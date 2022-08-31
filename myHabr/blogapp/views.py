import logging
from operator import itemgetter

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Blogs
from mainapp.models import BlogPost
from .forms import MyBlogForm

logger = logging.getLogger(__name__)

class AllBlogsListView(ListView):
    """Отображаем список всех блогов для всех пользователей"""
    model = Blogs
    template_name = 'allblogs/allblogs.html'
    paginate_by = 2
    success_url = reverse_lazy('allblogs:allblogs')

    def get_queryset(self, ):
        return Blogs.objects.order_by('name').filter(status__in=Blogs.PUBLISHED)


class ListHabrOfMyBlog(ListView):
    """Просмотр статей в моём блоге"""
    model = BlogPost
    template_name = 'blogapp/habrinmyblog.html'
    paginate_by = 2

    def get_queryset(self):
        return BlogPost.objects.filter(blog=self.kwargs["pk"]).order_by('-create_date')


class MainMyBlogs(ListView):
    model = Blogs
    template_name = 'blogapp/index.html'
    # paginate_by = 1

    def get_queryset(self):
        obj = Blogs.objects.filter(user=self.request.user).order_by('category')
        return obj


class MyBlogCreate(CreateView):
    model = Blogs
    form_class = MyBlogForm
    template_name = "blogapp/myblog_create.html"
    success_url = reverse_lazy('blogapp:myblogs')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class MyBlogDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blogs
    template_name = "blogapp/myblog_delete.html"
    success_url = reverse_lazy("blogapp:myblogs")

    def test_func(self):
        blog = self.get_object()
        if self.request.user.id == blog.user_id:
            return True
        return False


class MyBlogUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blogs
    form_class = MyBlogForm
    template_name = "blogapp/myblog_update.html"
    success_url = reverse_lazy("blogapp:myblogs")

    def test_func(self):
        blog = self.get_object()
        if self.request.user.id == blog.user_id:
            return True
        return False


class Category(ListView):
    model = BlogPost
    template_name = 'mainapp/index.html'
    paginate_by = 3

    def get_queryset(self):
        pk = self.kwargs['pk']
        return BlogPost.objects.order_by('-create_date').filter(status__in=BlogPost.PUBLISHED, blog=pk)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        blogs = BlogPost.objects.order_by('-create_date').filter(status__in=BlogPost.PUBLISHED, blog=pk)
        if self.request.POST.get('pk') == '0':
            new_blogs = [[(blog.likes.count() - blog.dislikes.count()), blog] for blog in blogs]
            new_blogs = sorted(new_blogs, key=itemgetter(0), reverse=True)
            blogs = []
            for i in new_blogs:
                blogs.append(i[1])

        context = {
            'object_list': blogs
        }
        return render(request=request, template_name='categories/category.html', context=context)

