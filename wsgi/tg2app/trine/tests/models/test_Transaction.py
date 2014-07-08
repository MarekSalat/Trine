from unittest import TestCase
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
        sourceGroup = TagGroup(user=self.users[0], tags=[Tag(user=self.users[0], name="account")])
        targetGroup = TagGroup(user=self.users[0], tags=[Tag(user=self.users[0], name="cache")])

        sourceTrans, targetTrans = Transaction.new_transfer(template, sourceGroup, targetGroup)

        self.assertNotEqual(sourceTrans.id, targetTrans.id)
        self.assertEquals(sourceTrans.transferKey, targetTrans.transferKey)
        self.assertEquals(sourceTrans.amount, -targetTrans.amount)
        self.assertEquals(sourceTrans.foreignCurrencyAmount, -targetTrans.foreignCurrencyAmount)
        self.assertEquals(sourceTrans.foreignCurrency, targetTrans.foreignCurrency)
        self.assertEquals(sourceTrans.description, targetTrans.description)
        self.assertEquals(sourceTrans.user.id, targetTrans.user.id)
        self.assertEquals(sourceTrans.date, targetTrans.date)

        trans = db.query(Transaction).all()

        print(trans)
        self.assertEquals(len(trans), 2)
