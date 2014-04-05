# -*- coding: utf-8 -*-
"""Setup the trine application"""
from __future__ import print_function

import transaction

from trine import model
from trine.model import seedSchema


def bootstrap(command, conf, vars):
    """Place any commands to setup trine here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError

    try:
        u = model.User()
        u.name = 'manager'
        u.display_name = 'Example manager'
        u.email = 'manager@somedomain.com'
        u.password = 'managepass'

        model.DBSession.add(u)

        g = model.UserGroup()
        g.name = 'managers'
        g.display_name = 'Managers Group'

        g.users.append(u)

        model.DBSession.add(g)

        p = model.Permission()
        p.name = 'manage'
        p.description = 'This permission give an administrative right to the bearer'
        p.groups.append(g)

        model.DBSession.add(p)

        u1 = model.User()
        u1.name = 'editor'
        u1.display_name = 'Example editor'
        u1.email = 'editor@somedomain.com'
        u1.password = 'editpass'

        model.DBSession.add(u1)
        model.DBSession.flush()

        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, it may have already been added:')
        import traceback

        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    seedSchema(model.DBSession)
    model.DBSession.flush()
    transaction.commit()
    # <websetup.bootstrap.after.auth>
