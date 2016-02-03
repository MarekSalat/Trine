import re
from sqlalchemy import UniqueConstraint, Column, ForeignKey, Boolean, String, or_
from sqlalchemy.orm import relationship, backref
from trine.model import DeclarativeBase as Base, DBSession, User
from trine.utils.AutoRepr import AutoRepr
from trine.utils.uuidType import UuidColumn, id_column

__author__ = 'Marek'


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
        if not str_names:
            return []

        existing_names = DBSession.query(Tag).with_parent(user). \
            filter(or_(*[Tag.name == name for name in str_names])).all()

        not_existing_names = list(set(str_names) - set([tag.name for tag in existing_names]))

        for name in not_existing_names:
            tag = Tag(user=user, name=name, type=type)
            DBSession.add(tag)
            existing_names.append(tag)

        return existing_names


