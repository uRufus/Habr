
from django.urls import path
from profiles import views
app_name = 'profiles'

urlpatterns = [
    path('<int:id>/', views.profile, name='Profile'),
    path('create_update_profile/<int:id>/<str:action>/', views.create_update_profile, name='CUProfile')
]
