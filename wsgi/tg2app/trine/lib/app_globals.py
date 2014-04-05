# -*- coding: utf-8 -*-

"""The application's Globals object"""
from routes import Mapper
from tg import config

__all__ = ['Globals']


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):
        """Do nothing, by default."""
        # pass

        map = Mapper(directory=config['paths']['controllers'],
                     always_scan=config['debug'])

        # Setup a default route for the root of object dispatch
        # map.connect('*url', controller='root', action='routes_placeholder')

        map.connect('common', '/{controller}/{action}', controller='routes_placeholder', action='routes_placeholder', )
        map.connect('homeAction', '/{action}', controller='root', action='routes_placeholder', )
        map.connect('home', '/', controller='root', action='index', )

        # config['routes.map'] = map

