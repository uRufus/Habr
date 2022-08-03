from django.contrib import admin

# Register your models here.
from adminapp.models import Message
from authapp.models import MyHabrUser
from blogapp.models import Blogs, BlogCategories
from faq.models import Post
from mainapp.models import BlogPost



class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "updated", "timestamp"]
    list_display_links = ["id", "updated"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post

class MyHabrUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "first_name", "last_name", "email", "is_active"]
    list_display_links = ["username"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["username", "email", "is_active"]

    class Meta:
        model = MyHabrUser

class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "from_user", "to_user", "type_message", "text", "created_at", "is_active"]
    list_display_links = ["from_user", "to_user"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at", "type_message"]
    search_fields = ["from_user", "to_user", "is_active"]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'from_user', None) is None:
            obj.from_user = request.user
        obj.save()

    class Meta:
        model = Message

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "tag", "category", "status", "create_date", "update_date"]
    list_display_links = ["title"]
    list_filter = ["tag", "category", "status"]
    search_fields = ["title", "tag", "category", "status"]

    class Meta:
        model = BlogPost


class BlogsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category_id", "user_id"]
    list_display_links = ["name"]
    # list_editable = ["is_active"]
    list_filter = ["category_id", "user_id"]
    search_fields = ["category_id", "user_id"]

    class Meta:
        model = Blogs

class BlogCategoriesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]
    # list_editable = ["is_active"]

    class Meta:
        model = BlogCategories

admin.site.register(MyHabrUser, MyHabrUserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(BlogCategories, BlogCategoriesAdmin)
admin.site.register(Post, PostModelAdmin)
admin.site.register(BlogPost, BlogPostAdmin)