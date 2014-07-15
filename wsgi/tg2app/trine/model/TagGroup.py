from sqlalchemy import func, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from trine.model import DeclarativeBase as Base, DBSession, Tag, User
from trine.utils.AutoRepr import AutoRepr
from trine.utils.uuidType import id_column, UuidColumn

__author__ = 'Marek'

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