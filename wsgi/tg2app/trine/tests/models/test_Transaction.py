from unittest import TestCase
from sqlalchemy import func
from sqlalchemy.orm import make_transient
from trine.model import DBSession as db, Transaction, UserGroup, User, Tag, TagGroup
from trine.tests.models import ModelTest

__author__ = 'Marek'


class TestTransaction(ModelTest):
    klass = Transaction

    def setUp(self):
        super().setUp()
        group = UserGroup(name="test group 0")
        self.users = [
            User(name="user 0", email="user0@localhost.host", password="test", groups=[group]),
        ]

        db.add_all(self.users)
        db.flush()

    def test_new_transfer(self):
        template = Transaction(user=self.users[0], amount=42, foreignCurrencyAmount=1, description="Something ...")
        # make_transient(template)

        source_group = TagGroup(user=self.users[0], tags=[Tag(user=self.users[0], name="account")])
        target_group = TagGroup(user=self.users[0], tags=[Tag(user=self.users[0], name="cache")])

        source_trans, target_trans = Transaction.new_transfer(template, source_group, target_group)

        self.assertNotEqual(source_trans.id, target_trans.id)
        self.assertEquals(source_trans.transferKey, target_trans.transferKey)
        self.assertEquals(source_trans.amount, -target_trans.amount)
        self.assertEquals(source_trans.foreignCurrencyAmount, -target_trans.foreignCurrencyAmount)
        self.assertEquals(source_trans.foreignCurrency, target_trans.foreignCurrency)
        self.assertEquals(source_trans.description, target_trans.description)
        self.assertEquals(source_trans.user.id, target_trans.user.id)
        self.assertEquals(source_trans.date, target_trans.date)

        trans = db.query(Transaction).all()
        self.assertEquals(len(trans), 2)
