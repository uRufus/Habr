import json
from operator import itemgetter

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from adminapp.models import Message
from mainapp.models import BlogPost, Comment
from mainapp.utils import (create_comment_like_message,
                           create_post_like_message, find_article_by_comment)
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

    def post(self, request, *args, **kwargs):
        blogs = BlogPost.objects.order_by('-create_date').filter(status__in=BlogPost.PUBLISHED)
        if self.request.POST.get('pk') == '0':
            new_blogs = [[(blog.likes.count() - blog.dislikes.count()), blog] for blog in blogs]
            new_blogs = sorted(new_blogs, key=itemgetter(0), reverse=True)
            blogs = []
            for i in new_blogs:
                blogs.append(i[1])

        context = {
            'object_list': blogs
        }
        return render(request=request, template_name='mainapp/index.html', context=context)


class BlogPostView(ListView):
    model = BlogPost
    template_name = "blogpost.html"

    def get_queryset(self):
        user = self.request.user
        return BlogPost.objects.filter(author=user).exclude(status="0").order_by('-create_date')


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
    admin_url = request.build_absolute_uri(admin_url)
    # исключение для того, чтобы работало fill_db
    try:
        Message.objects.get_or_create(
            from_user=obj.author,
            to_group=Group.objects.get(name='moderator'),
            text=admin_url,
            type_message='1',
            url=admin_url
        )
    except:
        pass
    return redirect(request.META['HTTP_REFERER'])


class BlogPostCreate(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_form.html"
    success_url = reverse_lazy("blogpost")

    def get_initial(self):
        user = self.request.user.id
        self.initial = {"user": user}
        return self.initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogpost/blogpost_update.html"
    success_url = reverse_lazy("blogpost")

    def get_initial(self):
        user = self.request.user.id
        self.initial = {"user": user}
        return self.initial

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
            create_post_like_message(post,request, is_like=True)

        if is_like:
            post.likes.remove(request.user)

        sum_rating = post.likes.all().count() - post.dislikes.all().count()

        return HttpResponse(
            json.dumps({
                'like_count': post.likes.all().count(),
                'dislike_count': post.dislikes.all().count(),
                'sum_rating': sum_rating,
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
            create_post_like_message(post, request, is_like=False)

        if is_dislike:
            post.dislikes.remove(request.user)

        sum_rating = post.likes.all().count() - post.dislikes.all().count()

        return HttpResponse(
            json.dumps({
                'like_count': post.likes.all().count(),
                'dislike_count': post.dislikes.all().count(),
                'sum_rating': sum_rating,
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
            create_comment_like_message(comment, request, is_like=True)

        if is_like:
            comment.likes.remove(request.user)

        sum_rating_comments = comment.likes.all().count() - comment.dislikes.all().count()

        return HttpResponse(
            json.dumps({
                'comment_like_count': comment.likes.all().count(),
                'comment_dislike_count': comment.dislikes.all().count(),
                'sum_rating_comments': sum_rating_comments,
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
            create_comment_like_message(comment, request, is_like=False)

        if is_dislike:
            comment.dislikes.remove(request.user)

        sum_rating_comments = comment.likes.all().count() - comment.dislikes.all().count()

        return HttpResponse(
            json.dumps({
                'comment_like_count': comment.likes.all().count(),
                'comment_dislike_count': comment.dislikes.all().count(),
                'sum_rating_comments': sum_rating_comments,
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
                              .exclude(from_user=self.request.user)\
                              .order_by('is_read', '-created_at')


def mark_read(request):
    message_id = request.POST['message_id']
    Message.objects.filter(id=message_id).update(is_read=True)
    return JsonResponse({'success': True})


def message_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(to_user=request.user, is_read=False)\
                               .exclude(from_user=request.user).count()
    else:
        count = 0
    return JsonResponse({'count': count})


def blog_comment(request):
    text = request.POST.get('comment_text')
    blog_id = request.POST['blog_id']
    user = request.user if request.user.is_authenticated else None
    comment = Comment.objects.create(user=user, text=text)
    CommentsLink.objects.create(comment=comment, type='article',
                                assigned_id=blog_id)
    article_id = find_article_by_comment(comment.id)
    article = BlogPost.objects.get(id=article_id)
    comment.send_message(request, article)
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


def delete_comment(request):
    comment_id = request.POST['comment_id']
    Comment.objects.get(id=comment_id).delete()
    return JsonResponse({'success': True})



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
