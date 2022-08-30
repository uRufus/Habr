from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from mainapp.models import BlogPost, Comment, CommentsLink
from adminapp.models import Message
from mainapp.utils import find_article_by_comment
from django.urls import reverse


@receiver(post_save, sender=CommentsLink)
def post_save_comment(created, **kwargs):
    comment = kwargs['instance'].comment
    call_moderator = '@moderator' in comment.parse_tags()
    if call_moderator:
        article_id = find_article_by_comment(comment.id)
        article_url = reverse('blogpost_detail', args=[article_id])
        message_text = f'Article url: {article_url}\n' \
                       f'Comment text: {comment.text}'
        Message.objects.get_or_create(
            from_user=comment.user,
            to_group=Group.objects.get(name='moderator'),
            text=message_text,
            type_message='1',
            url=article_url
        )
