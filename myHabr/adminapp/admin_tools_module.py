
from admin_tools.dashboard import modules


class ToolsModule(modules.DashboardModule):

    def __init__(self, title, data):
        super(ToolsModule, self).__init__()
        self.template = '../templates/admin_tools_module.html'
        self.title = title
        self.header_lst = ['Автор', 'Текст обращения', 'Тип обращения', 'Дата создания обращения', 'Активно']
        self.data = data

    def is_empty(self):
        return ''
