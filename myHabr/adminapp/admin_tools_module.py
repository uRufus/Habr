
from admin_tools.dashboard import modules


class ToolsModule(modules.DashboardModule):
    def is_empty(self):
        return self.message == ''

    def __init__(self, **kwargs):
        super(ToolsModule, self).__init__(**kwargs)
        self.template = '../templates/admin_tools_module.html'
        self.message = kwargs.get('message', '')