import json
import unittest

from app.model import DBSession
from sqlalchemy import func
from tg import jsonify
from sqlalchemy.orm import subqueryload, defer

from trine.model import Tag, Transaction, TagGroup, User
from trine.tests import TrineControllerTestCase


@unittest.skip("classing skipping")
class TestTag(TrineControllerTestCase):
    def test_deref(self):
        trans = DBSession.query(Transaction).options(
            subqueryload(Transaction.incomeTagGroup).subqueryload(TagGroup.tags),
            subqueryload(Transaction.expenseTagGroup).subqueryload(TagGroup.tags)
        ).options(defer('_user_id'))

        tran = trans.first()
        print(tran)
        print(json.dumps({'fsd': tran.incomeTagGroup.tags[0]}))

    def test_concat(self):
        user = DBSession.query(User).filter(User.id == "d09b9111-70a0-43c0-9373-aba10f2af592").all()[0]

        # balanceQuery = DBSession.query(func.sum(Transaction.amount).label("balance")).with_parent(user).\
        # filter(Transaction.date > datetime.utcnow())

        tags = DBSession.query(Tag).with_parent(user).filter(Tag.type == Tag.TYPE_INCOME)
        balances = []
        # for tag in tags:
        balance = DBSession.query(Transaction.id, func.sum(Transaction.amount).label("balance")).with_parent(user)
        balances = DBSession.query(Tag.name, balance.c.balance). \
            filter(Transaction.incomeTagGroup.has(TagGroup.tags.any(Tag.id == balance)))
        balances.append(balances)

        print(balances)


    def test_some(self):
        # fields = exclude_fields(Transaction, [Transaction.user, Transaction._user_id, Transaction.expenseTagGroup_id, Transaction.incomeTagGroup_id, Transaction.expenseTagGroup, Transaction.incomeTagGroup])
        transactions = DBSession.query(Transaction).options(
            subqueryload(Transaction.incomeTagGroup).subqueryload(TagGroup.tags),
            subqueryload(Transaction.expenseTagGroup).subqueryload(TagGroup.tags)
        ).all()

        transaction_json = jsonify.encode(dict(transactions=transactions))
        parsed = json.loads(transaction_json)
        print(json.dumps(parsed, indent=2, sort_keys=True), len(transactions))

        # print(fields)
        # print(fields[0])

    def test_tag(self):
        db = DBSession()

        res = db.query(func.sum(Transaction.amount).label("balance"))
        print(res.one().balance)
        print(res.filter(Transaction.amount < 0).one().balance)
        print(res.filter(Transaction.amount > 0).one().balance)

        res = db.query(Transaction) \
            .filter(Transaction.expenseTagGroup.has(TagGroup.tags.any(Tag.name.in_(["traveling", "grocery"])))) \
            .filter(Transaction.incomeTagGroup.has(TagGroup.tags.any(Tag.name.in_(["cash"]))))

        print("\n\nAll transactions with expense tags [traveling or grocery] and income tag [cash]\n")
        for r in res.all():
            print(r)

        print("\n\nAll expenses per tag\n")
        for tag in db.query(Tag).filter(Tag.type == Tag.TYPE_EXPENSE):
            print(tag.name)
            for transactions in [group.expenses.all() for group in tag.groups]:
                for transaction in transactions:
                    print(transaction)

    def test_user(self):
        db = DBSession()
        user = db.query(User) \
            .filter(User.password == User.encryptPassword('root'), User.email == r'salat.marek42@gmail.com') \
            .one()

        self.assertIsNotNone(user)