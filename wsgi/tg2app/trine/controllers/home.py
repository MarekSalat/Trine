from tg import expose
from trine.lib.base import BaseController

__author__ = 'Marek'


class HomeController(BaseController):
    def __init__(self):
        print("\n\n\n\n\nsdfsdf\n\n\n\n\n")

    @expose()
    def index(self):
        return "asdfdsf"