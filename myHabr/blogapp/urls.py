from django.urls import path

from .views import mainmyblogs

urlpatterns = [
    path('', mainmyblogs, name='mainmyblogs'),
]
