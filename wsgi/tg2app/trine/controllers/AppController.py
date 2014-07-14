from tg import expose, predicates
from trine.lib.utils import exposeForThisName
from trine.lib.base import BaseController

__author__ = 'Marek'


class AppController(BaseController):
    allow_only = predicates.not_anonymous()

    @exposeForThisName
    def index(self, *arg, **kw):
        return dict(*arg, **kw)