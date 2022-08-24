
from admin_tools.dashboard import modules
from mainapp.models import BlogPost, Comment
from adminapp.admin import MessageAdmin
from authapp.models import MyHabrUser


class ToolsModule(modules.DashboardModule):

    def is_empty(self):
        return  ''

    def __init__(self, title, data):
        super(ToolsModule, self).__init__()
        self.template = '../templates/admin_tools_module.html'
        self.title = title
        self.header_lst = ['Автор','Текст обращения','Тип обращения','Дата создания обращения', 'Активно']
        self.data = data

        # self.headers = list(data[0].keys())


    # def init_with_context(self, context):
    #     pass