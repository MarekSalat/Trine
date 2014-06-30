# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in trine.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""
from repoze.who.classifiers import default_request_classifier
from repoze.who.interfaces import IIdentifier, IChallenger
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.basicauth import BasicAuthPlugin
from tg import AppConfig
import tg

from trine.config.TrineAppConfig import TrineAppConfig

import trine
from trine import model
from trine.controllers.Api.ApiController import ApiErrorController, ApiCrudRestController, TagRestController
from trine.lib import helpers

base_config = AppConfig()
base_config.renderers = []

# True to prevent dispatcher from striping extensions
# For example /socket.io would be served by "socket_io" method instead of "socket"
base_config.disable_request_extensions = False

# Set None to disable escaping punctuation characters to "_" when dispatching methods.
# Set to a function to provide custom escaping.
base_config.dispatch_path_translator = True
base_config.prefer_toscawidgets2 = True

base_config.package = trine

#Enable json in expose
base_config.renderers.append('json')
#Enable genshi in expose to have a lingua franca for extensions and pluggable apps
#you can remove this if you don't plan to use it.
base_config.renderers.append('genshi')

#Set the default renderer
base_config.default_renderer = 'jinja'
base_config.renderers.append('jinja')
base_config.jinja_extensions = ['jinja2.ext.with_']
#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = trine.model
base_config.DBSession = trine.model.DBSession
# Configure the authentication backend

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP
base_config.sa_auth.cookie_secret = "c70561d4-5099-4e75-a140-18ed32907db3"

base_config.auth_backend = 'sqlalchemy'

# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class = model.User

from tg.configuration.auth import TGAuthMetadata

#This tells to TurboGears how to retrieve the data for your user
class ApplicationAuthMetadata(TGAuthMetadata):
    def __init__(self, sa_auth):
        self.sa_auth = sa_auth

    def authenticate(self, environ, identity):
        user = self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(name=identity['login']).first()

        if user and user.validate_password(identity['password']):
            return identity['login']

    def get_user(self, identity, userid):
        return self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(name=userid).first()

    def get_groups(self, identity, userid):
        return [g.name for g in identity['user'].groups]

    def get_permissions(self, identity, userid):
        return [p.name for p in identity['user'].permissions]

base_config.sa_auth.dbsession = model.DBSession

base_config.sa_auth.authmetadata = ApplicationAuthMetadata(base_config.sa_auth)

# authtkt = AuthTktCookiePlugin(base_config.sa_auth.cookie_secret, 'authtkt')
# basicauth = BasicAuthPlugin("Secure Area")
# classifications = {
#     IIdentifier: ["basicauth"],
#     IChallenger: ["basicauth"],
# }
#
# def my_custom_classifier(environ):
#     if environ.get('HTTP_AUTHORIZATION', ''):
#         return "basicauth"
#     return default_request_classifier(environ)
#
# def setup_auth(
#               form_plugin=None, form_identifies=True,
#               cookie_secret='secret', cookie_name='authtkt',
#               login_url='/login', login_handler='/login_handler',
#               post_login_url=None, logout_handler='/logout_handler',
#               post_logout_url=None, login_counter_name=None,
#               cookie_timeout=None, cookie_reissue_time=None,
#               **who_args):
#
#     cookie_timeout = 60*60*24*30
#     cookie_reissue_time = cookie_timeout//2
#
#     from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
#     cookie = AuthTktCookiePlugin(cookie_secret, cookie_name,
#                                  timeout=cookie_timeout,
#                                  reissue_time=cookie_reissue_time)
#     who_args['identifiers'] = [('cookie', cookie)]
#     if not 'authenticators' in who_args.keys():
#         who_args['authenticators'] = []
#     who_args['authenticators'].insert(0, ('cookie', cookie))
#
#     # If no form plugin is provided then create a default
#     # one using the provided options.
#     if form_plugin is None:
#         from tg.configuration.auth.fastform import FastFormPlugin
#         form = FastFormPlugin(login_url, login_handler, post_login_url,
#                               logout_handler, post_logout_url,
#                               rememberer_name='cookie',
#                               login_counter_name=login_counter_name)
#     else:
#         form = form_plugin
#
#     if form_identifies:
#         who_args['identifiers'].insert(0, ('main_identifier', form))
#
#     if not 'challengers' in who_args.keys():
#         who_args['challengers'] = []
#
#     who_args['challengers'].insert(0, ('form', form))
#     who_args['challengers'].insert(0, ('basicauth', basicauth))
#     who_args['identifiers'].insert(0, ('basicauth', basicauth ))
#     who_args["request_classifier"] = my_custom_classifier
#


# setup_auth(base_config.sa_auth)
# base_config.sa_auth.form_identifies = False

# You can use a different repoze.who Authenticator if you want to
# change the way users can login
# base_config.sa_auth.authenticators = [('cookie', authtkt)]

# base_config.sa_auth.identifiers = [ ('repoze.whoplugins.auth_tkt', authtkt) ]#, ('repoze.whoplugins.basicauth', basicauth )]

# You can add more repoze.who metadata providers to fetch
# user metadata.
# Remember to set base_config.sa_auth.authmetadata to None
# to disable authmetadata and use only your own metadata providers
#base_config.sa_auth.mdproviders = [('myprovider', SomeMDProvider()]

# override this if you would like to provide a different who plugin for
# managing login and logout of your application
# base_config.sa_auth.form_plugin = None

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url = '/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url = '/post_logout'

try:
    # Enable DebugBar if available, install tgext.debugbar to turn it on
    from tgext.debugbar import enable_debugbar
    enable_debugbar(base_config)
except ImportError:
    pass



