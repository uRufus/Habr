from django.urls import path

import blogapp.views as myblogs

app_name = 'blogapp'

urlpatterns = [
    path('', myblogs.MainMyBlogs.as_view(), name='myblogs'),
    path('create/new/', myblogs.MyBlogCreate.as_view(), name='myblog_create'),
    path('<int:pk>/delete/', myblogs.MyBlogDelete.as_view(), name='myblog_delete'),
    path('<int:pk>/edit/', myblogs.MyBlogUpdate.as_view(), name='myblog_update'),
    path('<int:pk>/list/', myblogs.ListHabrOfMyBlog.as_view(), name='habrinmyblog'),
]
