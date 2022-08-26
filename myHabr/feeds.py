from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse

from mainapp.models import BlogPost


class LatestPostsFeed(Feed):
    title = 'Последние статьи'


    link = '/blog/'
    description = 'Новые статьи на MyHabr'


    def items(self):
        return BlogPost.objects.all()[:5]


    def item_title(self, item):
        return item.title


    def item_description(self, item):
        return truncatewords(item.body, 30)

    def item_link(self, item):
        return reverse('blogpost_detail', args=[item.pk])