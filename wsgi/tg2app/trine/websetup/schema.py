# -*- coding: utf-8 -*-
"""Setup the trine application"""
from __future__ import print_function
import os

from tg import config
import transaction


def setup_schema(command, conf, vars):
    """Place any commands to setup trine here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from trine import model
    # <websetup.websetup.schema.after.model.import>

    # <websetup.websetup.schema.before.metadata.create_all>
    print("Creating tables")
    model.metadata.create_all(bind=config['tg.app_globals'].sa_engine)
    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()
    print('Initializing Migrations')
    import alembic.config, alembic.command

    alembic_cfg = alembic.config.Config()
    here = os.path.dirname(os.path.abspath(__file__))
    migrationpath = os.path.join(here, '../../migration')
    alembic_cfg.set_main_option("script_location", migrationpath)
    alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.url'])
    alembic.command.stamp(alembic_cfg, "head")
