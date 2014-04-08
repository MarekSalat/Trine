import json
import os
import pprint
from unittest import TestCase
from sqlalchemy import func, Column
from tg import jsonify
from trine.model import Tag, Fund, TagGroup, User


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

    def test_some(self):
        # fields = exclude_fields(Fund, [Fund._user, Fund._user_id, Fund.expenseTagGroup_id, Fund.incomeTagGroup_id, Fund.expenseTagGroup, Fund.incomeTagGroup])
        funds = DBSession.query(Fund).options(
            subqueryload(Fund.incomeTagGroup).subqueryload(TagGroup.tags),
            subqueryload(Fund.expenseTagGroup).subqueryload(TagGroup.tags)
        ).all()

        fund_json = jsonify.encode(dict(funds=funds))
        parsed = json.loads(fund_json)
        print(json.dumps(parsed, indent=2, sort_keys=True), len(funds))

        # print(fields)
        # print(fields[0])

    def xxtest_tag(self):
        db = DBSession()

        res = db.query(func.sum(Fund.amount).label("balance"))
        print(res.one().balance)
        print(res.filter(Fund.amount < 0).one().balance)
        print(res.filter(Fund.amount > 0).one().balance)

        res = db.query(Fund) \
            .filter(Fund.expenseTagGroup.has(TagGroup.tags.any(Tag.name.in_(["traveling", "grocery"])))) \
            .filter(Fund.incomeTagGroup.has(TagGroup.tags.any(Tag.name.in_(["cash"]))))

        print("\n\nAll funds with expense tags [traveling or grocery] and income tag [cash]\n")
        for r in res.all():
            print(r)

        print("\n\nAll expenses per tag\n")
        for tag in db.query(Tag).filter(Tag.type == Tag.TYPE_EXPENSE):
            print(tag.name)
            for funds in [group.expenses.all() for group in tag.groups]:
                for fund in funds:
                    print(fund)

    def xxtest_user(self):
        db = Session()
        user = db.query(User) \
            .filter(User.password == User.encryptPassword('root'), User.email == r'salat.marek42@gmail.com') \
            .one()

        self.assertIsNotNone(user)