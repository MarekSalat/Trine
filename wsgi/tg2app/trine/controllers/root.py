# -*- coding: utf-8 -*-
"""Main Controller"""
#from routes import Mapper

from tg import expose, flash, request, tmpl_context
from tg.i18n import ugettext as _
from trine.controllers.tgroot import TGRootController

from trine.lib.base import BaseController
from trine.controllers.error import ErrorController
from trine.controllers.FundController import FundController

__all__ = ['RootController']


# noinspection PyCallingNonCallable
class RootController(BaseController):
    """
    The root controller for the trine application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tgroot.controllers.WSGIAppController`.

    """

    error = ErrorController()

    def __init__(self):
        self._fund = FundController(DBSession)
        self._root = TGRootController()
        # 
        # map = Mapper()
        # map.connect(None, "/error/{action}/{id}", controller="error")
        # map.connect("home", "/", controller="main", action="index")
        # # ADD CUSTOM ROUTES HERE
        # map.connect(None, "/{controller}/{action}")
        # map.connect(None, "/{controller}/{action}/{id}")
        # 
        # self.map = map


    @expose()
    def _lookup(self, *args):
        path = request.environ['PATH_INFO']
        flash(_(r'%s - %s  - %r') % (args, path, self.map.routematch(path)))
        return self._root, args

    def _before(self, *args, **kw):
        tmpl_context.project_name = "Trine"
