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

from mainapp import views as mainapp
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('admin/', admin.site.urls),
    path('faq/', include('faq.urls')),
    path('myblog/', include('blogapp.urls')),
     # path('', mainapp.main, name='main'),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('blog/', mainapp.BlogPostView.as_view(), name='blogpost'),
    path('blog/<int:pk>', mainapp.BlogPostDetail.as_view(), name='blogpost_detail'),
    path('blog/<int:pk>/edit/', mainapp.BlogPostUpdate.as_view(), name='blogpost_update'),
    path('blog/create/', login_required(mainapp.BlogPostCreate.as_view()), name='blogpost_create'),
    path('blog/<int:pk>/delete/', mainapp.BlogPostDelete.as_view(), name='blogpost_delete'),
    path('blog/<int:pk>/verify/', mainapp.send_under_review, name='send_under_review'),
    path('blog/<int:pk>/private/', mainapp.BlogPostPrivateDetail.as_view(), name='blogpost_detail-private'),
    path('blog/comment/', mainapp.blog_comment, name='blog_comment'),
    path('blog/sub_comment/', mainapp.blog_sub_comment, name='blog_sub_comment'),
    path('blog/comment_edit/', mainapp.blog_comment_edit, name='blog_comment_edit'),
    path('profiles/', include('authapp.urls', namespace='authapp')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
