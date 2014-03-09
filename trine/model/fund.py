import datetime

from trine.utils.AutoRepr import AutoRepr
from trine.utils.uuidType import id_column, UUID

__author__ = 'Marek'

from sqlalchemy.orm import relationship, backref
from sqlalchemy import String, Float, DateTime, Text, ForeignKey, Table, Column

from trine.model import DeclarativeBase as Base, DBSession


class Tag(Base, AutoRepr):
    __tablename__ = "Tag"

    TYPE_INCOME = "INCOME"
    TYPE_EXPENSE = "EXPENSE"

    id = id_column()
    name = Column(String(length=128), unique=True)
    type = Column(String(length=16), default=TYPE_EXPENSE)

    class __sprox__(object):
        hide_fields = ['groups']
        # field_widget_types = {'name':TextField}


tags = Table('tags', Base.metadata,
             Column('Tag_id', UUID, ForeignKey('Tag.id')),
             Column('TagGroup_id', UUID, ForeignKey('TagGroup.id'))
)


class TagGroup(Base, AutoRepr):
    __tablename__ = "TagGroup"

    id = id_column()

    # many to many TagGroup<->Tag
    tags = relationship('Tag', secondary=tags, backref='groups', lazy='dynamic')

    class __sprox__(object):
        hide_fields = ['incomes', 'expenses']


class Fund(Base, AutoRepr):
    __tablename__ = "fund"

    id = id_column()
    amount = Column(Float, nullable=False)

    foreignCurrency = Column(Float, nullable=True)
    currency = Column(
        String(3)) # according to http://www.xe.com/iso4217.php and symbol can be found http://www.xe.com/symbols.php

    date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    description = Column(Text)

    incomeTagGroup_id = Column(UUID, ForeignKey(TagGroup.id))
    expenseTagGroup_id = Column(UUID, ForeignKey(TagGroup.id))

    incomeTagGroup = relationship(TagGroup, foreign_keys=incomeTagGroup_id,
                                  backref=backref('incomes', lazy='dynamic', order_by=id))
    expenseTagGroup = relationship(TagGroup, foreign_keys=expenseTagGroup_id,
                                   backref=backref('expenses', lazy='dynamic', order_by=id))


# noinspection PyArgumentList
def seedSchema(db: DBSession):
    # user = User(name="Marek", email="salat.marek42@gmail.com",
    #             password=User.encryptPassword('root'),
    #             defaultCurrency="CZK")

    grocery = Tag(name="grocery")
    beers = Tag(name="beers")
    home = Tag(name="home")
    traveling = Tag(name="traveling")
    bus = Tag(name="bus")
    train = Tag(name="train")

    cash = Tag(name="cash", type=Tag.TYPE_INCOME)
    account = Tag(name="account", type=Tag.TYPE_INCOME)
    salary = Tag(name="salary", type=Tag.TYPE_INCOME)

    funds = []

    group_cash = TagGroup(tags=[cash])
    group_account = TagGroup(tags=[account])
    group_account_salary = TagGroup(tags=[account, salary])

    funds.append(Fund(
        amount=5000,
        foreignCurrency=5000 / 28,
        currency="EUR",
        incomeTagGroup=group_account_salary
    ))

    funds.append(Fund(
        amount=-50,
        incomeTagGroup=group_cash,
        expenseTagGroup=TagGroup(tags=[grocery, beers])
    ))

    funds.append(Fund(
        amount=-150,
        incomeTagGroup=group_account,
        expenseTagGroup=TagGroup(tags=[traveling, bus])
    ))

    group_traveling_train = TagGroup(tags=[traveling, train])
    funds.append(Fund(
        amount=-200,
        incomeTagGroup=group_cash,
        expenseTagGroup=group_traveling_train
    ))

    funds.append(Fund(
        amount=-128,
        incomeTagGroup=group_account,
        expenseTagGroup=group_traveling_train
    ))

    funds.append(Fund(
        amount=-42,
        incomeTagGroup=group_account,
        expenseTagGroup=TagGroup(tags=[grocery, home, beers])
    ))

    for fund in funds:
        db.add(fund)
        # db.commit()





