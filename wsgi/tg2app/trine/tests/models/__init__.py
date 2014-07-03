# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""
from unittest import TestCase

from nose.tools import eq_

from trine.model import DBSession
from trine.tests import load_app, setup_db, teardown_db


__all__ = ['ModelTest']


class ModelTest(TestCase):
    """Base unit test case for the models."""

    klass = None
    attrs = {}

    def setUp(self):
        super().setUp()
        load_app()
        setup_db()

        """Setup test fixture for each model test method."""
        try:
            new_attrs = {}
            new_attrs.update(self.attrs)
            new_attrs.update(self.do_get_dependencies())
            self.obj = self.klass(**new_attrs)
            DBSession.add(self.obj)
            DBSession.flush()
            return self.obj
        except:
            DBSession.rollback()
            raise

    def tearDown(self):
        """Tear down test fixture for each model test method."""
        DBSession.rollback()
        teardown_db()
        super().tearDown()

    def do_get_dependencies(self):
        """Get model test dependencies.

        Use this method to pull in other objects that need to be created
        for this object to be build properly.

        """
        return {}

    def test_create_obj(self):
        """Model objects can be created"""
        pass

    def test_query_obj(self):
        """Model objects can be queried"""
        obj = DBSession.query(self.klass).one()
        for key, value in self.attrs.items():
            eq_(getattr(obj, key), value)
