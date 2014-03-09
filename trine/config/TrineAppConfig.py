from tg import AppConfig

__author__ = 'Marek'


class TrineAppConfig(AppConfig):
    def __init__(self, minimal=False, root_controller=None):
        super().__init__(minimal, root_controller)