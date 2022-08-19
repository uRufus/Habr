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

class BlogPostInlineAdmin(admin.TabularInline):
    model = BlogPost

    fields = ['title', 'tag_list', 'status', 'blog', 'update_date']
    readonly_fields = ['update_date', 'tag_list']
    # list_filter = ["blog", "status"]
    # extra = 0

class CommentInlineAdmin(admin.TabularInline):
    model = Comment


class MyHabrUserAdmin(admin.ModelAdmin):
    fields = (("username", "first_name", "last_name"), "email", ("last_login", "date_joined", "is_active"),
              ('is_superuser', 'is_staff'),'custom_group')
    list_display = ["id", "username", "first_name", "last_name", "email", "is_active"]
    list_display_links = ["username"]
    readonly_fields = ["username", "first_name", "last_name", "email", "last_login", "date_joined"]
    exclude = ['password']
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["username", "email", "is_active"]
    inlines = [BlogPostInlineAdmin, CommentInlineAdmin]

    def custom_group(self, obj):
        # Добавить проверку на суперпользователя
        """
        get group, separate by comma, and display empty string if user has no group
        """
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''


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
    list_display = ["id", "title", "blog", "status", "tag_list", "create_date", "update_date"]
    list_display_links = ["title"]
    list_editable = ["status"]
    list_filter = ["blog", "status", "tag_list"]
    search_fields = ["title", "tag_list", "blog", "status"]
    readonly_fields = ["tag_list", "create_date", "update_date"]


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

admin.site.register(MyHabrUser, MyHabrUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(BlogCategories, BlogCategoriesAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment)
admin.site.register(CommentsLink)
admin.site.register(Profile, ProfileAdmin)
