from django.urls import path

from .views import home, single
urlpatterns = [
    path('', home, name='home'),
    path('<int:id>/', single, name='single'),
]
