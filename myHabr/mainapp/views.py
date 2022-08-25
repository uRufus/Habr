import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from adminapp.models import Message
from mainapp.models import BlogPost, Comment
from mainapp.utils import find_article_by_comment
from .forms import BlogPostForm
from .models import CommentsLink


class BlogListView(ListView):
    """[M] На главной странице должны подряд отображаться последние
    публикации, вне зависимости от тематики, отсортированные по дате
    (сначала самые свежие)"""
    model = BlogPost
    template_name = 'mainapp/index.html'
    paginate_by = 3

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
    info = (obj._meta.app_label, obj._meta.model_name)
    admin_url = reverse('admin:%s_%s_change' % info, args=(obj.pk,))
    # исключение для того, чтобы работало fill_db
    try:
        Message.objects.get_or_create(
            from_user=obj.author,
            to_group=Group.objects.get(name='moderator'),
            text=admin_url,
            type_message='1'
        )
    except:
        pass
    return redirect(request.META['HTTP_REFERER'])


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

        return HttpResponse(
            json.dumps({
                'like_count': post.likes.all().count(),
                'dislike_count': post.dislikes.all().count(),
                # 'sum_rating': post.votes.sum_rating()
            }),
            content_type='application/json'
        )


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

        return HttpResponse(
            json.dumps({
                'like_count': post.likes.all().count(),
                'dislike_count': post.dislikes.all().count(),
                # 'sum_rating': post.votes.sum_rating()
            }),
            content_type='application/json'
        )


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
            article_id = find_article_by_comment(comment.id)
            article_url = reverse('blogpost_detail', args=[article_id])
            article_url = request.build_absolute_uri(article_url)
            url = f'{article_url}#{comment.id}'
            com_len = 15 if len(comment.text) >= 15 else len(comment.text)
            text = comment.text[:com_len]
            Message.objects.get_or_create(
                from_user=request.user,
                to_user=comment.user,
                type_message='0',
                text=f'Пользователь {request.user.username} поставил Вашему'
                     f' <a href={url}>комментарию ({text})</a> лайк.'
            )

        if is_like:
            comment.likes.remove(request.user)

        # next = request.POST.get('next')
        # if next is not None and not re.search(r'blog/\d+$', next):
        #     next = request.META.get('HTTP_REFERER')
        # return HttpResponseRedirect(next)

        return HttpResponse(
            json.dumps({
                'comment_like_count': comment.likes.all().count(),
                'comment_dislike_count': comment.dislikes.all().count(),
                # 'sum_rating': post.votes.sum_rating()
            }),
            content_type='application/json'
        )


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

        # next = request.POST.get('next')
        # if next is not None and not re.search(r'blog/\d+$', next):
        #     next = request.META.get('HTTP_REFERER')
        # return HttpResponseRedirect(next)

        return HttpResponse(
            json.dumps({
                'comment_like_count': comment.likes.all().count(),
                'comment_dislike_count': comment.dislikes.all().count(),
                # 'sum_rating': post.votes.sum_rating()
            }),
            content_type='application/json'
        )


class NotifyListView(ListView):
    """[M] Как зарегистрированный пользователь
    я хочу получать уведомления"""
    model = Message
    template_name = 'mainapp/notify.html'
    paginate_by = 10

    def get_queryset(self):
        return Message.objects.filter(to_user=self.request.user)\
                              .exclude(from_user=self.request.user)


def mark_read(request):
    message_id = request.POST['message_id']
    Message.objects.filter(id=message_id).update(is_read=True)
    return JsonResponse({'success': True})


def message_count(request):
    count = Message.objects.filter(to_user=request.user, is_read=False).count()
    return JsonResponse({'count': count})


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


def call_moderator(request):
    comment_id = request.POST['comment_id']
    url = request.POST['url']
    message_text = f'Жалоба на комментарий под номером {comment_id}\n{url}'
    Message.objects.create(
        from_user=request.user,
        to_group=Group.objects.get(name='moderator'),
        text=message_text,
        type_message='1'
    )
    return JsonResponse({"success": True})


def similar_blogposts(request):
    pass
