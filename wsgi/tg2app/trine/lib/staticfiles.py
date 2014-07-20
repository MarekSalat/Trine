# -*- coding: utf-8 -*-
"""This module contains a controller class ``StaticFiles`` to serve static files
from below a given directory, which supports protecting these files via the
identity permission system.

Use this controller by mounting it somewhere in your controller tree, for
example on your root controller, like this::

    class Root(controller.RootController)
        private = StaticFiles('/private')

.. note::
    The URL path passed to the constructor should match the location where the
    controller is mounted! It is used as the section name to look up the
    configuration for this controller instance.

To set the configuration for a ``StaticFiles`` controller for a particular URL
path, you can either use the ``config.update`` function in your Python code::

    config.update({
        '/private': {
            # The filesystem directory under which the static files are located
            'static_files.basedir': join(os.getcwd(), 'private'),
            # Give a list of permission names either as a comma-separated
            # string or a tuple/list of strings.
            'static_files.permissions': 'static_files',
        }
    })

Or put the following in one of your configuration files::

    [/private]
    static_files.basedir = "%(current_dir_uri)s/private"
    static_files.permissions = 'static_files'

With this configuration you can now put static files to be served by this
controller in a directory named ``private`` below the directory where the
application was started. For example, if you put a file ``test.html`` in
the ``private`` directory, it can now accessed by the following URL in your
application (provided the user has the ``static_files`` permission)::

    http://yourserver/private/test.html

You can have a hierarchy of sub-directories below the ``private`` directory and
they will map to URL patsh as expected, e.g.::

    http://yourserver/private/foo/bar/test.html

Use the following commands (e.g. using ``'tg-admin shell'``) to set up a user
with the appropriate permission to view the files served by the example
``StaticFiles`` instance:

    from yourpkg import model

    model.create_tables()
    u = model.User.by_user_name(u'test')
    if not u:
        model.create_default_user(u'test', password=u'test')
        g = model.Group()
        g.group_name(u'users')
        g.display_name(u'All users')
        model.session.add(g)
        p = model.Permission()
        p.permission_name = u'static_files'
        p.description = u'Can access static files'
        model.session.add(p)
        p.groups.append(g)
        g.users.append(u)
        model.session.flush()
"""
from paste.deploy.compat import basestring
from tg import TGController, config, expose, abort, request, response
from tg.predicates import has_any_permission
from trine.lib.base import BaseController

__all__ = ['StaticFilesController']

# standard library imports
import os

from mimetypes import guess_type
from os.path import abspath, basename, commonprefix, exists, join


class StaticFilesController(BaseController):
    """A controller serving static files from below a configured directory."""

    def __init__(self, baseurl):
        super().__init__()
        basedir = '/private'  # config.get('static_files.basedir')
        if not basedir:
            raise ValueError("'static_files.basedir' not configured for URL "
                             "path '%s'." % baseurl)
        self.basedir = abspath(basedir)
        self.baseurl = baseurl

        # get permissions from configuration and apply them
        # perms = 'trine' # config.get('static_files.permissions', path=baseurl)
        # if perms:
        # if isinstance(perms, basestring):
        #         perms = [p.strip() for p in perms.split(',') if p.strip()]
        #     if isinstance(perms, (tuple, list)):
        #         self.require = has_any_permission(*perms)

    @expose()
    def default(self, *args, **kwargs):
        """Serve file given in positional URL params from below self.basedir."""

        if not args:
            abort(404)
        fullpath = abspath(join(self.basedir, *args))

        # check if fullpath exists and is below basedir
        if commonprefix([self.basedir, fullpath]) != self.basedir or \
                not exists(fullpath):
            abort(404)

        mimetype, enc = guess_type(fullpath)
        response.headers["Content-Type"] = mimetype
        try:
            return fullpath + ', ' + mimetype
        except (IOError, OSError):
            abort(404)
