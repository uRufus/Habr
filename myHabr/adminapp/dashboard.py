"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'myHabr.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'myHabr.dashboard.CustomAppIndexDashboard'
"""

try:
    # we use django.urls import as version detection as it will fail on django 1.11 and thus we are safe to use
    # gettext_lazy instead of ugettext_lazy instead
    from django.urls import reverse
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.core.urlresolvers import reverse
    from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name
from adminapp.admin_tools_module import ToolsModule
from mainapp.models import BlogPost, Comment


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for myHabr.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        self.children.append(modules.Group(
            title=u"Данные",
            display="tabs",
            children=[
                modules.ModelList(
                        title = u'Пользователи',
                        models=(
                            'authapp.models.MyHabrUser',
                            'profiles.models.Profile',
                            'django.contrib.auth.models.Group'
                        ),
                ),
                modules.ModelList(
                        title = u'Контент сайта',
                        models=(
                            'mainapp.models.BlogPost',
                            'mainapp.models.Comment',
                            'faq.models.Post',
                        ),
                ),
                modules.ModelList(
                        title = u'Рубрикаторы',
                        models=(
                            'blogapp.models.Blogs',
                            'blogapp.models.BlogCategories',
                        )
                ),
                modules.ModelList(
                        title = u'Коммуникация',
                        models=(
                            'adminapp.models.Message',
                        ),
                ),
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append a feed module
        self.children.append(modules.Feed(
            _('Последние статьи сайта'),
            feed_url="http://127.0.0.1:8000/feed/",
            limit=10
        ))

        self.tools_data = BlogPost.objects.filter(status__gte=3)
        self.children.append(ToolsModule(title=u"Инструменты администратора", message=[[el.author, el.blog, el.title, el.tag_list, el.status] for el in self.tools_data]))

        # append an app list module for "Applications"
        # self.children.append(modules.AppList(
        #     _('Applications'),
        #     exclude=('django.contrib.*',),
        # ))

        # append an app list module for "Administration"
        # self.children.append(modules.AppList(
        #     _('Administration'),
        #     models=('django.contrib.*',),
        # ))

        # append another link list module for "support".
        # self.children.append(modules.LinkList(
        #     _('Support'),
        #     children=[
        #         {
        #             'title': _('Django documentation'),
        #             'url': 'http://docs.djangoproject.com/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Django "django-users" mailing list'),
        #             'url': 'http://groups.google.com/group/django-users',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Django irc channel'),
        #             'url': 'irc://irc.freenode.net/django',
        #             'external': True,
        #         },
        #     ]
        # ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for myHabr.
    """

    # we disable title because its redundant with the model list module
    title = 'Мой Хабр'

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
