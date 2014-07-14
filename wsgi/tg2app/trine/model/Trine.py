from copy import copy, deepcopy
from datetime import datetime
import re
import uuid

from trine.utils.AutoRepr import AutoRepr
from trine.utils.uuidType import id_column, UuidColumn, JsonableUUID

__author__ = 'Marek'

from sqlalchemy.orm import relationship, backref, make_transient
from sqlalchemy import String, Float, Text, ForeignKey, Table, Column, TIMESTAMP, UniqueConstraint, Boolean, or_, func

from trine.model import DeclarativeBase as Base, User, DBSession


class Tag(Base, AutoRepr):
    __tablename__ = "Tag"

    TYPE_INCOME = "INCOME"
    TYPE_EXPENSE = "EXPENSE"

    id = id_column()

    name = Column(String(length=128))
    type = Column(String(length=16), default=TYPE_EXPENSE)

    ishidden = Column(Boolean, default=False, nullable=True)

    _user_id = Column(UuidColumn, ForeignKey(User.id), nullable=False)
    user = relationship(User, foreign_keys=_user_id, backref=backref('tags'))

    __table_args__ = (UniqueConstraint(name, _user_id, name='_name_user_id_uc'), )

    class __sprox__(object):
        hide_fields = ['groups']

    @classmethod
    def get_names_from_str(cls, line: str) -> list:
        """
        Parse string of tags separated by comma

        :param line:
        :return: list of parsed names
        """
        tags = line
        tags = re.sub(r'\s+', ' ', tags)
        tags = re.sub(r' ?, ?', ',', tags)
        tags = re.sub(r',+', ',', tags)  # ",,,,,," => ","
        tags = re.sub(r',$', '', tags)  # delete last comma if exist
        tags = re.sub(r'^,', '', tags)  # delete first comma if exist

        if re.match(r"^\s*$", tags):
            return []

        # FIXME: there should be magic method handle list uniqueness
        names = []
        for name in tags.split(","):
            if name in names:
                continue
            names.append(name)
        return names

    @classmethod
    def by_names(cls, names: list, user: User):
        return DBSession.query(Tag).with_parent(user).filter(Tag.name.in_(names))

    @classmethod
    def new_from_name_list(cls, str_names: list, user: User, type) -> list:
        """
        Add only tags which does not exist for user yet

        :param str_names:
        :param user:
        :param type:
        :return: list of Tag
        """
        existing_names = DBSession.query(Tag).with_parent(user). \
            filter(or_(*[Tag.name == name for name in str_names])).all()

        not_existing_names = list(set(str_names) - set([tag.name for tag in existing_names]))

        for name in not_existing_names:
            tag = Tag(user=user, name=name, type=type)
            DBSession.add(tag)
            existing_names.append(tag)

        return existing_names


table_tags = Table('tags', Base.metadata,
                   Column('Tag_id', UuidColumn, ForeignKey('Tag.id')),
                   Column('TagGroup_id', UuidColumn, ForeignKey('TagGroup.id')),
)


class TagGroup(Base, AutoRepr):
    __tablename__ = "TagGroup"

    id = id_column()

    _user_id = Column(UuidColumn, ForeignKey(User.id), nullable=False)
    user = relationship(User, foreign_keys=_user_id, backref=backref('tagGroups'))

    # many to many TagGroup<->Tag
    tags = relationship('Tag', secondary=table_tags, backref='groups')

    class __sprox__(object):
        hide_fields = ['incomes', 'expenses']

    @classmethod
    def new_with_these_tags(cls, tags: list):
        """
        Add only if this group does not exist (exactly with these tags) yet.

        :param tags: list of Tag
        :return: TagGroup
        """
        if not tags:
            raise AssertionError()

        groups = cls.with_these_tags(tags).all()
        if not groups:
            group = TagGroup(user=tags[0].user, tags=tags)
            DBSession.add(group)
            groups = [group]

        # @TODO: display warning, because there should be only one group
        return groups[0]

    @classmethod
    def with_these_tags(cls, tags: list) -> list:
        """
        Return groups which contains exactly these tags

        :param tags: list of Tag
        :return: TagGroup query
        """
        if not tags:
            return DBSession.query(TagGroup).filter(TagGroup.id == None)

        tags_ids = [tag.id for tag in tags]

        # a and b and c <=> not (not a or not b or not c)
        groups = DBSession.query(TagGroup). \
            join(TagGroup.tags). \
            filter(TagGroup.tags.any(Tag.id.in_(tags_ids))). \
            filter(~TagGroup.tags.any(~Tag.id.in_(tags_ids))). \
            group_by(TagGroup.id). \
            having(func.count(Tag.id) == len(tags_ids))

        return groups


class Transaction(Base, AutoRepr):
    __tablename__ = "transaction"

    id = id_column()
    amount = Column(Float, nullable=False)

    foreignCurrencyAmount = Column(Float, nullable=True)
    foreignCurrency = Column(
        String(3))  # according to http://www.xe.com/iso4217.php and symbol can be found http://www.xe.com/symbols.php

    date = Column(TIMESTAMP, default=datetime.utcnow, nullable=True)
    description = Column(Text)

    incomeTagGroup_id = Column(UuidColumn, ForeignKey(TagGroup.id))
    expenseTagGroup_id = Column(UuidColumn, ForeignKey(TagGroup.id))

    incomeTagGroup = relationship(TagGroup, foreign_keys=incomeTagGroup_id, backref=backref('incomes', order_by=id))
    expenseTagGroup = relationship(TagGroup, foreign_keys=expenseTagGroup_id, backref=backref('expenses', order_by=id))

    # can bound more transaction together (for example transfer from account to account)
    transferKey = Column(UuidColumn, nullable=True, default=None)

    _user_id = Column(UuidColumn, ForeignKey(User.id), nullable=False)
    user = relationship(User, foreign_keys=_user_id, backref=backref('transactions', order_by=date))

    @classmethod
    def new_transfer(cls, template_transaction, from_group: TagGroup, to_group: TagGroup):
        """
        Add transfer. Transfer os composed of two Transaction which is source of money and target where money should go.
        These transaction are bind via special field ```transfer_key```

        :param template_transaction: Transaction used for generating transfer
        :param from_group: incomeTagGroup of source
        :param to_group: incomeTagGroup of target
        :return: source:Transaction, target:Transaction
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

        DBSession.add_all([source, target])
        DBSession.flush()
        return source, target

    @classmethod
    def get_total_incomes(cls, user: User, **kw):
        return cls.get_balance(user, **kw).filter(cls.amount > 0)

    @classmethod
    def get_total_expenses(cls, user: User, **kw):
        return cls.get_balance(user, **kw).filter(cls.amount < 0)

    @classmethod
    def get_balances_per_tag(cls, user: User, tag_type=Tag.TYPE_INCOME):
        if tag_type is not Tag.TYPE_INCOME and tag_type is not Tag.TYPE_EXPENSE:
            raise Exception('Unsupported tag type: ' + str(tag_type))

        query = DBSession.query(Tag.name, func.sum(Transaction.amount)).with_parent(user) \
            .filter(Transaction.transferKey == None) \
            .join(Tag.groups)

        if tag_type == Tag.TYPE_INCOME:
            query = query.join(TagGroup.incomes)
        else:
            query = query.join(TagGroup.expenses)

        return query.group_by(Tag.name)

    @classmethod
    def get_balance(cls, user: User, to_date=None, **kw):
        query = DBSession.query(func.sum(cls.amount)).with_parent(user).filter(cls.transferKey == None)
        if not to_date:
            query = query.filter(cls.date <= datetime.utcnow())

        return query