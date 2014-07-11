from random import random
from nose.tools import eq_
from trine.model import TagGroup, UserGroup, User, DBSession as db, Tag
from trine.tests.models import ModelTest

__author__ = 'Marek'


class TestGroup(ModelTest):
    """Unit test case for the ``Group`` model."""
    klass = TagGroup

    def setUp(self):
        super().setUp()
        group = UserGroup(name="test group 0")
        self.users = [
            User(name="user 0", email="user0@localhost.host", password="test", groups=[group]),
        ]

        self.tags = []
        for i in range(10):
            self.tags.append(Tag(name="tag %d" % i, user=self.users[0]))

        db.add_all(self.tags)
        db.flush()

    def test_with_these_tags(self):
        groups = [
            TagGroup(user=self.users[0], tags=self.tags[0:3]),
            TagGroup(user=self.users[0], tags=self.tags[0:4]),
            TagGroup(user=self.users[0], tags=self.tags[1:4]),
            TagGroup(user=self.users[0], tags=self.tags[0:5]),
            TagGroup(user=self.users[0], tags=self.tags[2:5]),
            TagGroup(user=self.users[0], tags=self.tags[2:6]),
            TagGroup(user=self.users[0], tags=self.tags[5:10]),
            TagGroup(user=self.users[0], tags=self.tags[3:8]),
            TagGroup(user=self.users[0], tags=self.tags),
        ]

        db.add_all(groups)
        db.flush()

        for i, group in enumerate(groups):
            self.assertEquals(TagGroup.with_these_tags(group.tags).first().id, group.id, "Group %d" % i)

        self.assertEquals(TagGroup.with_these_tags([]).all(), [])

    def test_new_with_these_tags(self):
        self.assertEquals(TagGroup.with_these_tags([]).all(), [])

        groups = [
            TagGroup(user=self.users[0], tags=self.tags[0:3]),
            TagGroup(user=self.users[0], tags=self.tags[0:4]),
            TagGroup(user=self.users[0], tags=self.tags[2:5]),
        ]

        db.add_all(groups)
        db.flush()

        self.assertEquals(TagGroup.new_with_these_tags([self.tags[2], self.tags[1], self.tags[0]]).id,
                          groups[0].id)

        self.assertNotIn(TagGroup.new_with_these_tags([self.tags[2], self.tags[3], self.tags[4], self.tags[4]]).id,
                         [group.id for group in groups])

