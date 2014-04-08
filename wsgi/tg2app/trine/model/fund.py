from datetime import datetime

from trine.utils.AutoRepr import AutoRepr
from trine.utils.uuidType import id_column, UuidColumn

__author__ = 'Marek'

from sqlalchemy.orm import relationship, backref, synonym
from sqlalchemy import String, Float, Text, ForeignKey, Table, Column, TIMESTAMP, UniqueConstraint, Boolean

from trine.model import DeclarativeBase as Base, DBSession, User

class Tag(Base, AutoRepr):
    __tablename__ = "Tag"

    TYPE_INCOME = "INCOME"
    TYPE_EXPENSE = "EXPENSE"

    id = id_column()
    created = synonym("date")

    name = Column(String(length=128))
    type = Column(String(length=16), default=TYPE_EXPENSE)
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)
    ishidden = Column(Boolean, default=False, nullable=False)

    _user_id = Column(UuidColumn, ForeignKey(User.id), nullable=False)
    _user = relationship(User, foreign_keys=_user_id, backref=backref('tags', order_by=created))

    __table_args__ = (UniqueConstraint(name, _user_id, name='_name_user_id_uc'), )

    class __sprox__(object):
        hide_fields = ['groups']
        # field_widget_types = {'name':TextField}


tags = Table('tags', Base.metadata,
    Column('Tag_id', UuidColumn, ForeignKey('Tag.id')),
    Column('TagGroup_id', UuidColumn, ForeignKey('TagGroup.id'))
)


class TagGroup(Base, AutoRepr):
    __tablename__ = "TagGroup"

    id = id_column()
    created = Column(TIMESTAMP, default=datetime.now, nullable=False)

    _user_id = Column(UuidColumn, ForeignKey(User.id), nullable=False)
    _user = relationship(User, foreign_keys=_user_id, backref=backref('tagGroups', order_by=created))

    # many to many TagGroup<->Tag
    tags = relationship('Tag', secondary=tags, backref='groups')

    class __sprox__(object):
        hide_fields = ['incomes', 'expenses']


class Fund(Base, AutoRepr):
    __tablename__ = "fund"

    id = id_column()
    amount = Column(Float, nullable=False)

    foreignCurrency = Column(Float, nullable=True)
    currency = Column(
        String(3)) # according to http://www.xe.com/iso4217.php and symbol can be found http://www.xe.com/symbols.php

    date = Column(TIMESTAMP, default=datetime.now, nullable=False)
    description = Column(Text)

    incomeTagGroup_id = Column(UuidColumn, ForeignKey(TagGroup.id))
    expenseTagGroup_id = Column(UuidColumn, ForeignKey(TagGroup.id))

    incomeTagGroup = relationship(TagGroup, foreign_keys=incomeTagGroup_id, backref=backref('incomes', order_by=id))
    expenseTagGroup = relationship(TagGroup, foreign_keys=expenseTagGroup_id, backref=backref('expenses', order_by=id))

    _user_id = Column(UuidColumn, ForeignKey(User.id), nullable=False)
    _user = relationship(User, foreign_keys=_user_id, backref=backref('funds', order_by=date))





