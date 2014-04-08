from tg import expose, flash, require, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates
from tg.predicates import has_permission
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from trine import model
from trine.model import DBSession
from trine.controllers.FundController import FundController
from trine.lib.utils import exposeForThisName
from trine.lib.base import BaseController


__author__ = 'Marek'


class MyAdminController(AdminController):
    allow_only = has_permission('all')

class TGRootController(BaseController):
    admin = MyAdminController(model, DBSession, config_type=TGAdminConfig)

    fund = FundController(DBSession)

    @exposeForThisName
    def index(self):
        return dict(page='index')

    @exposeForThisName
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @exposeForThisName
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @exposeForThisName
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(page='data', params=kw)

    @exposeForThisName
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @exposeForThisName
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @exposeForThisName
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ.get('repoze.who.logins', 0)
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login', params=dict(came_from=came_from, __logins=login_counter))
            return
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)

