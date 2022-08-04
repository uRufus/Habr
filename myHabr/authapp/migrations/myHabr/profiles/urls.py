
from django.urls import path
from profiles import views
app_name = 'profiles'

urlpatterns = [
    path('<int:id>/', views.profile, name='profile'),
    path('create_profile/<int:id>/', views.create_profile, name='create'),
    path('create_update_profile/<int:id>/<str:action>/', views.update_profile, name='update')
]
