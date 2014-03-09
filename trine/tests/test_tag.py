from unittest import TestCase
from sqlalchemy import func
from sandbox import Tag, createSchema, Fund, TagGroup, Session, seedSchema, User


class TestTag(TestCase):
    def xxtest_createAndSeed(self):
        createSchema()
        seedSchema()

    def test_tag(self):
        db = Session()

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

    def test_user(self):
        db = Session()
        user = db.query(User) \
            .filter(User.password == User.encryptPassword('root'), User.email == r'salat.marek42@gmail.com') \
            .one()

        self.assertIsNotNone(user)