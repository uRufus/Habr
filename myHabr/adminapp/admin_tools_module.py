
from admin_tools.dashboard import modules

from adminapp.models import Message


class ToolsModule(modules.DashboardModule):

    def __init__(self, title):
        super(ToolsModule, self).__init__()
        self.template = '../templates/admin_tools_module.html'
        self.title = title
        # self.header_lst = ['Автор', 'Текст обращения', 'Тип обращения', 'Дата создания обращения', 'Активно']
        self.header_lst = ['Автор', 'Текст обращения', 'Тип обращения', 'Дата создания обращения']
        self.data = None
        self.get_data()


    def is_empty(self):
        return ''

    def get_data(self):
        self.data = list(Message.objects.filter(type_message=1).filter(is_active=True).values() |
                         Message.objects.filter(type_message=3).filter(is_active=True).values())

    def save_message(self, id):
        message = Message.objects.det(id=id)
        message['is_active'] = False
        message.save()

    def reload(self, id):
        self.save_message(id)
        self.get_data()



    # def get_blogpost_id_from_url(self, url):
    #     try:
    #         return int(url.split('blog/')[1])
    #     except ValueError as err:
    #         return f'{err}'
