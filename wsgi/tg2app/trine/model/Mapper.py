import re
from sqlalchemy import or_
from trine.model import User, TagGroup, Tag

__author__ = 'Marek'

class Mapper:
    pass

class TagMapper(Mapper):
    @classmethod
    def getTagNamesListFromString(self, tagname: str) ->list:
        tags = tagname
        tags = re.sub(r'\s+', ' ', tags);
        tags = re.sub(r' ?, ?', ',', tags);
        tags = re.sub(r',+', ',', tags);   # ",,,,,," => ","
        tags = re.sub(r',$', '', tags);    # delete last comma if exist
        tags = re.sub(r'^,', '', tags);    # delete first comma if exist

        if re.match(r"^\s*$",tags):
            return []

        return tags.split(",")

class TagGroupMapper(Mapper):

    def __init__(self, db):
        super().__init__()
        self.db = db

    def getTagGroupOrCreateFromTagNames(self, tagNames:list, user:User, type) -> TagGroup:
        if not tagNames:
            return None

        groups = self.getGroupsFromTagNames(tagNames, user)
        if not groups:
            groups = [self.createNewGroupFromTagNames(tagNames, user, type)]

        # @TODO: display warning, because there should be only one group
        return groups[0]


    def getGroupsFromTagNames(self, tagNames:list, user:User) -> list:
        if not tagNames:
            return []

        # @TODO: there should be better solution how to get group directly from sql. See filtering
        groups = self.db.query(TagGroup).with_parent(user).\
            filter(TagGroup.tags.any(Tag.name.in_(tagNames))).\
            filter(~TagGroup.tags.any(~Tag.name.in_(tagNames))).\
            group_by(TagGroup.id)
            # having(func.count(TagGroup.tags) == len(tags))

        groups = [group for group in groups if len(group.tags) == len(tagNames) ]
        return groups

    def createNewGroupFromTagNames(self, tagNames:list, user:User, type) -> TagGroup:
        tags = self.db.query(Tag).with_parent(user).filter(or_(*[Tag.name == name for name in tagNames])).all()

        fetchedTagNames = [tag.name for tag in tags]
        notExistingTagNames = list(set(tagNames) - set(fetchedTagNames))

        for name in notExistingTagNames:
            tag = Tag(_user=user, name=name, type=type)
            tags.append(tag)

        return TagGroup(_user=user, tags=tags)

    def findTagByNames(self, names:list, user:User):
        return self.db.query(Tag).with_parent(user).filter(Tag.name.in_(names))

