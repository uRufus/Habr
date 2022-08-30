from mainapp.models import CommentsLink


def find_article_by_comment(comment_id):
    link = CommentsLink.objects.get(comment_id=comment_id)
    if link.type == 'article':
        return link.assigned_id
    else:
        return find_article_by_comment(link.assigned_id)
