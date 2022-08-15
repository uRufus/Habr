from django.contrib import admin

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

class MyHabrUserInline(admin.TabularInline):
    model = BlogPost

class MyHabrUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "first_name", "last_name", "email", "is_active"]
    list_display_links = ["username"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["username", "email", "is_active"]
    inlines = [MyHabrUserInline]

    def get_form(self, request, obj=None, **kwargs):
        # Ограничения для действий в форме
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        # Переменная для отключаемых полей
        disabled_fields = set()  # type Set[str]

        # if not is_superuser:
        #     form.base_fields['username'].disabled = True

        # Запрет изменения полей
        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

            # Запретить пользователям, не являющимся суперпользователями,
            # редактировать свои собственные разрешения
        if (
                not is_superuser
                and obj is not None
                and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    class Meta:
        model = MyHabrUser

class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "from_user", "to_user", "type_message", "text", "created_at", "is_active"]
    list_display_links = ["from_user", "to_user"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at", "type_message"]
    search_fields = ["from_user", "to_user", "is_active"]
    exclude = ["from_user"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'from_user', None) is None:
            obj.from_user = request.user
        obj.save()

    class Meta:
        model = Message

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "blog", "status", "create_date", "update_date"]
    list_display_links = ["title"]
    list_filter = ["blog", "status"]
    search_fields = ["title", "tag", "blog", "status"]

    class Meta:
        model = BlogPost


class BlogsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "user"]
    list_display_links = ["name"]
    # list_editable = ["is_active"]
    list_filter = ["category", "user"]
    search_fields = ["category", "user"]

    class Meta:
        model = Blogs

class BlogCategoriesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]
    # list_editable = ["is_active"]

    class Meta:
        model = BlogCategories

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "age", "update_profile", "text"]
    list_display_links = ["first_name", "last_name"]

    class Meta:
        model = Profile

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "created_at", "updated_at", "has_children"]
    list_display_links = ["id", "text"]

    class Meta:
        model = Comment

admin.site.register(MyHabrUser, MyHabrUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(BlogCategories, BlogCategoriesAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentsLink)
admin.site.register(Profile, ProfileAdmin)
