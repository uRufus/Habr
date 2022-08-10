import json
from django.core.management.base import BaseCommand
from authapp.models import MyHabrUser
from mainapp.models import BlogPost, Comment, CommentsLink, Tag
from blogapp.models import Blogs, BlogCategories
from profiles.models import Profile


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Users
        users = load_from_json('authapp/fixtures/users.json')

        MyHabrUser.objects.all().delete()
        for user in users:
            usr = user.get('fields')
            usr['id'] = user.get('pk')
            new_user = MyHabrUser(**usr)
            new_user.save()

        # Profiles
        profiles = load_from_json('profiles/fixtures/profiles.json')

        Profile.objects.all().delete()
        for profile in profiles:
            prf = profile.get('fields')
            user = prf.get('user_id')
            _user = MyHabrUser.objects.get(id=user)
            prf['user_id'] = _user
            new_profile = Profile(**prf)
            new_profile.save()

        # Blog Categories
        categories = load_from_json('blogapp/fixtures/categories.json')

        BlogCategories.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = BlogCategories(**cat)
            new_category.save()

        # Blogs
        blogs = load_from_json('blogapp/fixtures/blogs.json')

        Blogs.objects.all().delete()
        for blog in blogs:
            bl = blog.get('fields')
            bl['id'] = blog.get('pk')
            user = bl.get('user')
            _user = MyHabrUser.objects.get(id=user)
            bl['user'] = _user
            category = bl.get('category')
            _category = BlogCategories.objects.get(id=category)
            bl['category'] = _category
            new_blog = Blogs(**bl)
            new_blog.save()

        # Tags
        tags = load_from_json('mainapp/fixtures/tags.json')

        Tag.objects.all().delete()
        for tag in tags:
            Tag.objects.create(pk=tag['pk'], **tag['fields'])

        # Blog post
        blogposts = load_from_json('mainapp/fixtures/blogposts.json')

        BlogPost.objects.all().delete()
        for blogpost in blogposts:
            bl = blogpost.get('fields')
            tags =  bl.pop('tags')
            bl['id'] = blogpost.get('pk')
            user = bl.get('author')
            _user = MyHabrUser.objects.get(id=user)
            bl['author'] = _user
            category = bl.get('blog')
            _category = Blogs.objects.get(id=category)
            bl['blog'] = _category
            new_blogpost = BlogPost(**bl)
            new_blogpost.save()
            for tag_pk in tags:
                new_blogpost.tags.add(Tag.objects.get(pk=tag_pk))

        # Comments
        comments = load_from_json('mainapp/fixtures/comments.json')

        Comment.objects.all().delete()
        for comment in comments:
            com = comment.get('fields')
            com['id'] = comment.get('pk')
            user = com.get('user')
            _user = MyHabrUser.objects.get(id=user)
            com['user'] = _user
            new_comment = Comment(**com)
            new_comment.save()

        # Comment links
        commentlinks = load_from_json('mainapp/fixtures/commentslink.json')

        CommentsLink.objects.all().delete()
        for commentlink in commentlinks:
            com = commentlink.get('fields')
            com['id'] = commentlink.get('pk')
            comment = com.get('comment')
            _comment = Comment.objects.get(id=comment)
            com['comment'] = _comment
            new_commentlink = CommentsLink(**com)
            new_commentlink.save()
