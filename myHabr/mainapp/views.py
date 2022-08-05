from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
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
        obj = BlogPost.objects.order_by('-create_date')
        return obj


class BlogPostView(ListView):
    model = BlogPost
    template_name = "blogpost.html"
    ordering = ['-create_date']

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user)


class BlogPostDetail(DetailView):
    """Для отображения всем пользователям"""
    model = BlogPost
    template_name = "blogpost/blogpost-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects \
            .filter(commentslink__type='post',
                    commentslink__assigned_id=self.object.id) \
            .prefetch_related('user')
        for comment in comments:
            comment.find_children()

        context['comments'] = comments
        return context


class BlogPostPrivateDetail(DetailView):
    """Для отображения в личном кабинете пользователя"""
    model = BlogPost
    template_name = "blogpost/blogpost-detail-private.html"


def send_under_review(request, pk):
    """функция для перевода блога статуса блога из 'черновик' в 'статья на проверке' """
    obj = get_object_or_404(BlogPost, pk=pk)
    obj.status = BlogPost.UNDER_REVIEW
    obj.save()
    return HttpResponseRedirect(reverse('blogpost'))


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


class BlogPostDelete(DeleteView):
    model = BlogPost
    template_name = "blogpost/blogpost_delete.html"
    success_url = reverse_lazy("blogpost")


def blog_comment(request):
    text = request.POST['comment_text']
    blog_id = request.POST['blog_id']
    user = request.user if request.user.is_authenticated else None
    comment = Comment.objects.create(user=user, text=text)
    CommentsLink.objects.create(comment=comment, type='post',
                                assigned_id=blog_id)
    comments = Comment.objects \
        .filter(commentslink__type='post',
                commentslink__assigned_id=blog_id) \
        .prefetch_related('user')
    for comment in comments:
        comment.find_children()
    comments = render_to_string('comments/comments.html',
                                {'comments': comments})
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
                               {'children': parent_comment.children})
    return JsonResponse({'comment': comment})


class BlogAddLike(LoginRequiredMixin, View):
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


class BlogAddCommentLike(LoginRequiredMixin, View):
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

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class BlogAddCommentDislike(LoginRequiredMixin, View):
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

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
