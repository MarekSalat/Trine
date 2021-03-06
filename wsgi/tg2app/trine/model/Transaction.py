from copy import deepcopy
from datetime import datetime

import uuid

from trine.utils.AutoRepr import AutoRepr
from trine.utils.uuidType import id_column, UuidColumn, JsonableUUID

__author__ = 'Marek'

from sqlalchemy.orm import relationship, backref, make_transient
from sqlalchemy import String, Float, Text, ForeignKey, Column, TIMESTAMP, func, or_

from trine.model import DeclarativeBase as Base, User, DBSession, Tag, TagGroup


class Transaction(Base, AutoRepr):
    __tablename__ = "transaction"

    id = id_column()
    amount = Column(Float, nullable=False)

    foreignCurrencyAmount = Column(Float, nullable=True)
    foreignCurrency = Column(
        String(3))  # according to http://www.xe.com/iso4217.php and symbol can be found http://www.xe.com/symbols.php

    # UTC time
    date = Column(TIMESTAMP, default=datetime.utcnow, nullable=True)
    # tells how to convert date to user previously defined timezone
    timezoneCode = Column(String(3), default='UTC', nullable=True)

    description = Column(Text)

    incomeTagGroup_id = Column(UuidColumn, ForeignKey(TagGroup.id))
    expenseTagGroup_id = Column(UuidColumn, ForeignKey(TagGroup.id))

    incomeTagGroup = relationship(TagGroup, foreign_keys=incomeTagGroup_id, backref=backref('incomes', order_by=id))
    expenseTagGroup = relationship(TagGroup, foreign_keys=expenseTagGroup_id, backref=backref('expenses', order_by=id))

    # can bound more transaction together (for example transfer from account to account)
    transferKey = Column(UuidColumn, nullable=True, default=None)

    _user_id = Column(UuidColumn, ForeignKey(User.id), nullable=False)
    user = relationship(User, foreign_keys=_user_id, backref=backref('transactions', order_by=date))

    def calculate_amount(self):
        """
        There should be one (and only one) balancing income tag in incomeTagGroup field

        Story:
            -   I have in cash 42$, I do not remember how much I spend. I want to add my balance a application should
                calculate how much I spent.
                amount: 42$; incomeTagGroup: cash; expenseTagGroup: pub, beers; -> App should create transaction
                    with 42$ minus actual cash balance
            -   I have not used app for a while. I know my balances and I do not want to calculate how much I need to
                add or subtract.
            -   I had 453$ on my "account" now I have 896$ on my account and the difference is my "salary"
                amount: 896$; incomeTagGroup: account, salary;    -> App should create transaction with 443$

        """
        balance = self.get_balances_per_tag(self.user)\
            .filter(
                Tag.id.in_([tag.id for tag in self.incomeTagGroup.tags])
            ).all()

        if len(balance) != 1:
            raise Exception("There should be one (and only one) balancing income tag in incomeTagGroup field")
        else:
            balance = balance[0]

        self.amount -= balance[1]
        return self

    @classmethod
    def new_transfer(cls, template_transaction, from_group: TagGroup, to_group: TagGroup):
        """
        Add transfer. Transfer os composed of two Transaction which is source of money and target where money should go.
        These transaction are bind via special field ```transfer_key```

        :param template_transaction: Transaction used for generating transfer
        :param from_group: incomeTagGroup of source
        :param to_group: incomeTagGroup of target
        :return: source:Transaction, target:Transaction
        Story:
            -   I have withdraw some money and I do not want add two separate transactions
        """
        make_transient(template_transaction)

        user = template_transaction.user
        template_transaction.user = None
        if not template_transaction._user_id:
            template_transaction._user_id = str(user.id)
        template_transaction.transferKey = JsonableUUID(uuid.uuid4().hex)
        template_transaction.incomeTagGroup = None
        template_transaction.incomeTagGroup_id = None
        template_transaction.expenseTagGroup = None
        template_transaction.expenseTagGroup_id = None

        if not template_transaction.date:
            template_transaction.date = datetime.utcnow()

        source = deepcopy(template_transaction)
        """ :type: Transaction """
        source.incomeTagGroup = from_group
        source.user = user

        target = deepcopy(template_transaction)
        """ :type: Transaction """

        target.incomeTagGroup = to_group
        target.amount *= -1
        target.user = user
        if target.foreignCurrencyAmount:
            target.foreignCurrencyAmount *= -1

        return source, target

    @classmethod
    def get_total_incomes(cls, user: User, **kw):
        return cls.get_balance(user, **kw).filter(cls.amount > 0)

    @classmethod
    def get_total_expenses(cls, user: User, **kw):
        return cls.get_balance(user, **kw).filter(cls.amount < 0)

    @classmethod
    def get_balance(cls, user: User, from_date=None, to_date=None, only_planned=False, **kw):
        query = DBSession.query(func.sum(cls.amount)).with_parent(user).filter(cls.transferKey == None)

        if to_date:
            query = query.filter(cls.date <= to_date)
        if from_date and not only_planned:
            query = query.filter(cls.date >= from_date)
        if only_planned:
            _from_date = from_date if from_date else datetime.utcnow()
            query = query.filter(or_(cls.date == None, cls.date > _from_date))

        return query

    @classmethod
    def get_balances_per_tag(cls, user: User, tag_type=Tag.TYPE_INCOME, from_date=None, to_date=None, only_planned=False, **kw):
        if tag_type is not Tag.TYPE_INCOME and tag_type is not Tag.TYPE_EXPENSE:
            raise Exception('Unsupported tag type: ' + str(tag_type))

        query = DBSession.query(Tag.name, func.sum(cls.amount)).with_parent(user) \
            .filter(Transaction.transferKey == None) \
            .join(Tag.groups)\
            .filter(Tag.groups.any(TagGroup.incomes.any(cls.amount < 0)))

        if to_date:
            query = query.filter(cls.date < to_date)
        if from_date and not only_planned:
            query = query.filter(cls.date > from_date)
        if only_planned:
            _from_date = from_date if from_date else datetime.utcnow()
            query = query.filter(or_(cls.date == None, cls.date >= _from_date))

        if tag_type == Tag.TYPE_INCOME:
            query = query.join(TagGroup.incomes)
        else:
            query = query.join(TagGroup.expenses)

        return query.group_by(Tag.name)

