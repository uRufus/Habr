import re
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mainapp.models import BlogPost, Comment
from .forms import BlogPostForm
from .models import CommentsLink


class BlogListView(ListView):
    """[M] На главной странице должны подряд отображаться последние
    публикации, вне зависимости от тематики, отсортированные по дате
    (сначала самые свежие)"""
    model = BlogPost
    template_name = 'mainapp/index.html'
    paginate_by = 2

    def get_queryset(self):
        return BlogPost.objects.order_by('-create_date').filter(status__in=BlogPost.PUBLISHED)


class BlogPostView(ListView):
    model = BlogPost
    template_name = "blogpost.html"
    ordering = ['-create_date']

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user).exclude(status="0")


class BlogPostDetail(DetailView):
    """Для отображения всем пользователям"""
    model = BlogPost
    template_name = "blogpost/blogpost-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_related = BlogPost.objects.filter(blog=self.object.blog, status='3').exclude(pk=self.object.pk)[:3]
        print(context_related)

        comments = Comment.objects \
            .filter(commentslink__type='article',
                    commentslink__assigned_id=self.object.id) \
            .prefetch_related('user')

        for comment in comments:
            comment.find_children()

        context['related'] = context_related
        context['comments'] = comments
        context['post'] = BlogPost.objects.filter(pk=self.object.pk)

        return context


class BlogPostPrivateDetail(DetailView):
    """Для отображения в личном кабинете пользователя"""
    model = BlogPost
    template_name = "blogpost/blogpost-detail-private.html"


def send_under_review(request, pk):
    """функция для перевода статуса блога из 'черновик' в 'статья на проверке' """
    obj = get_object_or_404(BlogPost, pk=pk)
    obj.status = BlogPost.UNDER_REVIEW
    obj.save()
    return HttpResponseRedirect(reverse('blogpost'))


class BlogPostCreate(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_form.html"
    success_url = reverse_lazy("blogpost")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_update.html"
    success_url = reverse_lazy("blogpost")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class BlogPostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "blogpost/blogpost_delete.html"
    success_url = reverse_lazy("blogpost")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class BlogAddLike(LoginRequiredMixin, View):
    """
    [M] Как зарегистрированный пользователь
    я хочу ставить один лайк или дизлайк к любой статье,
    чтобы составить свое мнение о статье
    """
    def post(self, request, pk, *args, **kwargs):
        post = BlogPost.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class BlogAddDislike(LoginRequiredMixin, View):
    """
    [M] Как зарегистрированный пользователь
    я хочу ставить один лайк или дизлайк к любой статье,
    чтобы составить свое мнение о статье
    """
    def post(self, request, pk, *args, **kwargs):
        post = BlogPost.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

@method_decorator(csrf_exempt, name='post')
@method_decorator(csrf_exempt, name='dispatch')
class BlogAddCommentLike(LoginRequiredMixin, View):
    """
    [M] Как зарегистрированный пользователь я хочу ставить
    один лайк или дизлайк к любому зарегистрированному пользователю,
    чтобы составить свое мнение о том, что написал пользователь
    """
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next')
        if next is not None and not re.search(r'blog/\d+$', next):
            next = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(next)


@method_decorator(csrf_exempt, name='post')
@method_decorator(csrf_exempt, name='dispatch')
class BlogAddCommentDislike(LoginRequiredMixin, View):
    """
    [M] Как зарегистрированный пользователь я хочу ставить
    один лайк или дизлайк к любому зарегистрированному пользователю,
    чтобы составить свое мнение о том, что написал пользователь
    """
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next')
        if next is not None and not re.search(r'blog/\d+$', next):
            next = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(next)


def blog_comment(request):
    text = request.POST.get('comment_text')
    blog_id = request.POST['blog_id']
    user = request.user if request.user.is_authenticated else None
    comment = Comment.objects.create(user=user, text=text)
    CommentsLink.objects.create(comment=comment, type='article',
                                assigned_id=blog_id)
    comments = Comment.objects \
        .filter(commentslink__type='article',
                commentslink__assigned_id=blog_id) \
        .prefetch_related('user')

    for comment in comments:
        comment.find_children()
    comments = render_to_string('comments/comments.html',
                                {'comments': comments,
                                 'user': request.user})
    return JsonResponse({'comments': comments})


def blog_sub_comment(request):
    text = request.POST['comment_text']
    comment_id = request.POST['comment_id']
    user = request.user if request.user.is_authenticated else None
    comment = Comment.objects.create(user=user, text=text)
    CommentsLink.objects.create(comment=comment, type='comment',
                                assigned_id=comment_id)

    parent_comment = Comment.objects.get(id=comment_id)
    parent_comment.has_children = True
    parent_comment.save()
    parent_comment.find_children()

    comment = render_to_string('comments/subcomment.html',
                               {'children': parent_comment.children,
                                'user': request.user})
    return JsonResponse({'comment': comment})

def blog_comment_edit(request):
    text = request.POST['comment_text']
    comment_id = request.POST['comment_id']
    comment = Comment.objects.get(id=comment_id)
    comment.text = text
    comment.save()
    edited_at = comment.updated_at.strftime("%d-%m-%Y, %H:%M:%S")
    return JsonResponse({'new_text': text,
                         'edited_at': edited_at})

def similar_blogposts(request):
    pass