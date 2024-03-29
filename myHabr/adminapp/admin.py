from django.contrib import admin
from django.urls import reverse

# Register your models here.
from adminapp.models import Message
from authapp.models import MyHabrUser
from blogapp.models import Blogs, BlogCategories
from faq.models import Post
from mainapp.models import BlogPost, Comment, CommentsLink
from profiles.models import Profile


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "updated", "timestamp"]
    list_display_links = ["id", "updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post

class BlogPostInlineAdmin(admin.TabularInline):
    model = BlogPost

    fields = ['title', 'tag_list', 'status', 'blog', 'update_date', 'like', 'dislike']
    readonly_fields = ['update_date', 'tag_list', 'like', 'dislike']

    def like(self, obj):
        return obj.likes.count()

    def dislike(self, obj):
        return obj.dislikes.count()


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    fields = ['user', 'parent', 'text', 'updated_at', 'like', 'dislike']
    readonly_fields = ['updated_at', 'like', 'dislike']

    def like(self, obj):
        return obj.likes.count()

    def dislike(self, obj):
        return obj.dislikes.count()


class MyHabrUserAdmin(admin.ModelAdmin):

    fields = (("username", "first_name", "last_name"), "email", ("last_login", "date_joined", "is_active"),
              ('is_superuser', 'is_staff'), 'groups')
    list_display = ["id", "username", "first_name", "last_name", "email", "is_active"]
    list_display_links = ["username"]
    exclude = ['password']
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["username", "email", "is_active"]
    inlines = [BlogPostInlineAdmin, CommentInlineAdmin]

    def get_form(self, request, obj=None, **kwargs):
        # Ограничения для действий в форме
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        # Переменная для отключаемых полей
        disabled_fields = set()  # type Set[str]

        # Запрет изменения полей
        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'is_staff',
                'groups',
                'user_permissions',
                "last_login",
                "date_joined",
            }

            # Запретить пользователям, не являющимся суперпользователями,
            # редактировать свои собственные разрешения
        if (
            not is_superuser
            and obj is not None
            and obj != request.user
        ):
            disabled_fields |= {
                "username",
                "first_name",
                "last_name",
                "email",
            }

        if (not is_superuser
            and obj is not None
            and obj == request.user) \
            or (not is_superuser
            and obj is not None
            and obj.is_superuser is True):
            disabled_fields |= {
                "is_active",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    class Meta:
        model = MyHabrUser

class MessageAdmin(admin.ModelAdmin):
    fields = (("type_message", "is_active"),
              ("to_user", "to_group"),
               "text", "url",
              ("created_at", "updated_at"))
    list_display = ["id", "from_user", "to_user", "type_message", "text", "clickable_url", "created_at", "is_active"]
    readonly_fields = ["created_at", "updated_at"]
    list_display_links = ["from_user", "to_user", "text"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at", "type_message"]
    search_fields = ["type_message", "text", "from_user"]
    exclude = ["from_user"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'from_user', None) is None:
            obj.from_user = request.user
        obj.save()

    def clickable_url(self, obj):
        url = obj.url
        from django.utils.html import format_html
        return format_html(f"<a href='{url}'>{url}</a>")

    def get_form(self, request, obj=None, **kwargs):
        # Ограничения для действий в форме
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        # Переменная для отключаемых полей
        disabled_fields = set()  # type Set[str]

        # Запрет изменения полей
        if not is_superuser:
            disabled_fields |= {
                "from_user",
                "to_user",
                "to_group",
                "type_message",
                "text",
                "url",
                "created_at",
                "updated_at"
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    class Meta:
        model = Message

class BlogPostAdmin(admin.ModelAdmin):

    fields = (("author", "blog", "status"), "title","image_header", "body", "tag_list", ("create_date", "update_date"))
    list_display = ("id", "author", "title", "blog", "status", "tag_list", "create_date", "like", "dislike")
    list_display_links = ["title"]
    list_editable = ["status"]
    list_filter = ["blog", "status", "tag_list"]
    search_fields = ["body", "title", "create_date"]
    # readonly_fields = ["tag_list", "create_date", "tag_list", "author", "blog", "update_date"]
    readonly_fields = ["create_date","author", "update_date"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if change:
            message = ''
            author = obj.author
            article_url = reverse('blogpost_detail', args=[obj.id])
            article_url = request.build_absolute_uri(article_url)
            new_status = obj.status
            old_status = BlogPost.objects.get(id=obj.id).status
            if old_status == '1' and new_status == '3':
                message = f'Ваша статья <a href={article_url}>{obj.title}</a>'\
                          f' одобрена'
            elif new_status == '0' and old_status != new_status:
                message = f'Ваша статья <a href={article_url}>{obj.title}</a>'\
                          f' удалена'
            elif new_status == '4' and old_status != new_status:
                message = f'Ваша статья <a href={article_url}>{obj.title}</a>'\
                          f' заблокирована'
            if message:
                Message.objects.get_or_create(
                    to_user=author,
                    text=message,
                    type_message='2',
                    url=article_url
                )
        super().save_model(request, obj, form, change)

    class Meta:
        model = BlogPost

    def like(self, obj):
        return obj.likes.count()

    def dislike(self, obj):
        return obj.dislikes.count()

    def save_model(self, request, obj, form, change):
        if getattr(obj, "author", None) is None:
            obj.author = request.user
        obj.save()


class BlogsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "user"]
    list_display_links = ["name"]
    list_filter = ["category", "user"]
    search_fields = ["category", "user"]

    class Meta:
        model = Blogs

class BlogCategoriesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]

    class Meta:
        model = BlogCategories

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "age", "update_profile", "text"]
    list_display_links = ["first_name", "last_name"]

    class Meta:
        model = Profile

class CommentAdmin(admin.ModelAdmin):
    fields = ("user", "text", ("created_at", "updated_at"), ("has_children", "parent", "is_active"))
    list_display = ["user", "parent", "text", "created_at", "is_active", "like", "dislike"]
    list_display_links = ["user", "text"]
    list_editable = ["is_active"]
    readonly_fields = ["created_at", "updated_at","user", "text",]

    class Meta:
        model = Comment

    def like(self, obj):
        return obj.likes.count()

    def dislike(self, obj):
        return obj.dislikes.count()


admin.site.register(MyHabrUser, MyHabrUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(BlogCategories, BlogCategoriesAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentsLink)
admin.site.register(Profile, ProfileAdmin)
