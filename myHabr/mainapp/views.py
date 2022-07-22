from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .models import BlogPost, Comment, CommentsLink
from .forms import BlogPostForm


def index(request):
    context = {
        'title': 'Habr',
    }
    return render(request, 'mainapp/index.html', context)
    # return render(request, 'index.html', context)


class BlogPostView(ListView):
    model = BlogPost
    template_name = "blogpost.html"
    ordering = ['-create_date']

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class BlogPostDetail(DetailView):
    model = BlogPost
    template_name = "blogpost/blogpost-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(type(self.object))
        print(self.object.id)
        comments = Comment.objects\
                          .filter(commentslink__type='post',
                                  commentslink__assigned_id=self.object.id)\
                         .prefetch_related('user')
        context['comments'] = comments
        return context


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


def blog_comment(request):
    text = request.POST['comment_text']
    blog_id = request.POST['blog_id']
    user = request.user if request.user.is_authenticated else None
    comment = Comment.objects.create(user=user, text=text)
    CommentsLink.objects.create(comment=comment, type='post',
                                assigned_id=blog_id)
    comments = Comment.objects\
                      .filter(commentslink__type='post',
                              commentslink__assigned_id=blog_id) \
                      .prefetch_related('user')
    comments[0].text = 'REPLACEMENT'
    comments = render_to_string('comments/comments.html',
                                {'comments': comments})
    return JsonResponse({'comments': comments})