
from django.urls import path
from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('<int:id_profile>/<int:user>/', views.profile, name='profile'),
    # path('create_profile/<int:id>/', views.create_profile, name='create'),
    path('create_update_profile/<int:id>/', views.update_profile, name='update'),
    # path('like/<int:id>/', views.like, name='like')
    path('like/<int:who_id>/<int:whom_id>/', views.profile_like, name='like'),
    path('dislike/<int:who_id>/<int:whom_id>/', views.profile_dislike, name='dislike'),
]
