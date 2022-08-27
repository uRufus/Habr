from django.urls import reverse
from adminapp.models import Message
from mainapp.models import BlogPost, Comment, CommentsLink


def find_article_by_comment(comment_id):
    link = CommentsLink.objects.get(comment_id=comment_id)
    if link.type == 'article':
        return link.assigned_id
    else:
        return find_article_by_comment(link.assigned_id)


def create_comment_like_message(comment: Comment, request, is_like=True):
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
             f' <a href={url}>комментарию ({text})</a> '
             f'{"диз" if not is_like else ""}лайк.'
    )


def create_post_like_message(post: BlogPost, request, is_like=True):
    article_url = reverse('blogpost_detail', args=[post.id])
    article_url = request.build_absolute_uri(article_url)
    url = f'{article_url}'
    text = post.title
    Message.objects.get_or_create(
        from_user=request.user,
        to_user=post.author,
        type_message='0',
        text=f'Пользователь {request.user.username} поставил Вашему'
             f' посту <a href={url}>{text}</a> '
             f'{"диз" if not is_like else ""}лайк.'
    )
