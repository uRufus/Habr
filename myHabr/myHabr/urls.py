"""myHabr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import blogapp
from blogapp.views import Category, AllBlogsListView
from mainapp import views as mainapp
from mainapp.views import BlogAddCommentLike, BlogAddLike, BlogAddDislike, BlogAddCommentDislike
from feeds import LatestPostsFeed

urlpatterns = [
    path(r'admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('', mainapp.BlogListView.as_view(), name='index'),
    path('faq/', include('faq.urls')),
    path('myblogs/', include('blogapp.urls', namespace='blogapp')),
    path('allblogs/', AllBlogsListView.as_view(), name='allblogs'),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('blog/', mainapp.BlogPostView.as_view(), name='blogpost'),
    path('blog/<int:pk>', mainapp.BlogPostDetail.as_view(), name='blogpost_detail'),
    path('blog/<int:pk>/edit/', mainapp.BlogPostUpdate.as_view(), name='blogpost_update'),
    path('blog/create/new/', mainapp.BlogPostCreate.as_view(), name='blogpost_create'),
    path('blog/<int:pk>/delete/', mainapp.BlogPostDelete.as_view(), name='blogpost_delete'),
    path('blog/<int:pk>/verify/', mainapp.send_under_review, name='send_under_review'),
    path('blog/<int:pk>/private/', mainapp.BlogPostPrivateDetail.as_view(), name='blogpost_detail-private'),
    path('blog/comment/', mainapp.blog_comment, name='blog_comment'),
    path('blog/sub_comment/', mainapp.blog_sub_comment, name='blog_sub_comment'),
    path('blog/comment_edit/', mainapp.blog_comment_edit, name='blog_comment_edit'),
    path('delete_comment/', mainapp.delete_comment, name='delete_comment'),
    path('blog/comment/<int:pk>/like/', BlogAddCommentLike.as_view(), name='comment-like'),
    path('blog/comment/<int:pk>/dislike/', BlogAddCommentDislike.as_view(), name='comment-dislike'),
    path('blog/<int:pk>/like/', BlogAddLike.as_view(), name='like'),
    path('blog/<int:pk>/dislike/', BlogAddDislike.as_view(), name='dislike'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('notify/', mainapp.NotifyListView.as_view(), name='notify'),
    path('notify/', mainapp.NotifyListView.as_view(), name='notify'),
    path('mark_read/', mainapp.mark_read, name='mark_read'),
    path('message_count/', mainapp.message_count, name='message_count'),
    path('category/<int:pk>/', Category.as_view(), name='category'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('call_moderator/', mainapp.call_moderator, name='cal_moderator'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
