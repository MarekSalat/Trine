from datetime import datetime
import json
import os
import pprint
from unittest import TestCase
import uuid
from sqlalchemy import func, Column, and_, select, or_
from tg import jsonify
from trine.model import Tag, Transaction, TagGroup, User


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload, contains_eager, defer, class_mapper, RelationshipProperty

# an Engine, which the Session will use for connection
# resources
here = os.path.dirname(os.path.abspath(__file__))
some_engine = create_engine('sqlite:///'+here+"../../../devdata.db", echo=False, echo_pool=False, pool_recycle=3600)

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
DBSession = Session()

# print(DBSession.query("").all())

def exclude_fields(entity, cols):
    cls = class_mapper(entity)

    clsFields = [p.key for p in cls.iterate_properties if isinstance(getattr(entity, p.key), Column)]
    excludedFields = [p if isinstance(p, str) else p.key for p in cols]

    fields = set(clsFields)-set(excludedFields)

    return [getattr(entity, key) for key in fields]

class TestTag(TestCase):
    def test_deref(self):
        trans = DBSession.query(Transaction).options(
                subqueryload(Transaction.incomeTagGroup).subqueryload(TagGroup.tags),
                subqueryload(Transaction.expenseTagGroup).subqueryload(TagGroup.tags)
            ).options(defer('_user_id'))

        tran = trans.first()
        print(tran)
        print(json.dumps({'fsd':tran.incomeTagGroup.tags[0]}))

    def xxtest_concat(self):
        user = DBSession.query(User).filter(User.id == "d09b9111-70a0-43c0-9373-aba10f2af592").all()[0]

        # balanceQuery = DBSession.query(func.sum(Transaction.amount).label("balance")).with_parent(user).\
        #                         filter(Transaction.date > datetime.utcnow())

        tags = DBSession.query(Tag).with_parent(user).filter(Tag.type == Tag.TYPE_INCOME)
        balances = []
        # for tag in tags:
        balance = DBSession.query(Transaction.id, func.sum(Transaction.amount).label("balance")).with_parent(user)
        balances = DBSession.query(Tag.name, balance.c.balance).\
            filter(Transaction.incomeTagGroup.has(TagGroup.tags.any(Tag.id == balance)))
        balances.append(balances)

        print(balances)


    def xxtest_some(self):
        # fields = exclude_fields(Transaction, [Transaction._user, Transaction._user_id, Transaction.expenseTagGroup_id, Transaction.incomeTagGroup_id, Transaction.expenseTagGroup, Transaction.incomeTagGroup])
        transactions = DBSession.query(Transaction).options(
            subqueryload(Transaction.incomeTagGroup).subqueryload(TagGroup.tags),
            subqueryload(Transaction.expenseTagGroup).subqueryload(TagGroup.tags)
        ).all()

        transaction_json = jsonify.encode(dict(transactions=transactions))
        parsed = json.loads(transaction_json)
        print(json.dumps(parsed, indent=2, sort_keys=True), len(transactions))

        # print(fields)
        # print(fields[0])

    def xxtest_tag(self):
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

    def xxtest_user(self):
        db = Session()
        user = db.query(User) \
            .filter(User.password == User.encryptPassword('root'), User.email == r'salat.marek42@gmail.com') \
            .one()

        self.assertIsNotNone(user)