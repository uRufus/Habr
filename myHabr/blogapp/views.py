from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Blogs
from mainapp.models import BlogPost
from .forms import MyBlogForm

class Mainmyblogs(ListView):
    model = Blogs
    template_name = 'blogapp/index.html'
    # paginate_by = 1

    def get_queryset(self):
        # obj = BlogPost.objects.filter(author=self.request.user).order_by('-create_date')
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


def category(request, pk):
    blogs = BlogPost.objects.order_by('-create_date').filter(status__in=BlogPost.PUBLISHED, blog=pk)
    context = {
        'blogs': blogs
    }
    return render(request=request, template_name='categories/category.html', context=context)
