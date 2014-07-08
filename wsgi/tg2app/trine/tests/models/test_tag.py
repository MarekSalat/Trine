from nose.tools import eq_
from trine.model import Tag, User, DBSession as db, UserGroup
from trine.tests.models import ModelTest

__author__ = 'Marek'


class TestTag(ModelTest):
    """Unit test case for the ``Group`` model."""
    klass = Tag

    def setUp(self):
        super().setUp()
        group = UserGroup(name="group 0")
        self.users = [
            User(name="user 0", email="user0@localhost.host", password="test", groups=[group]),
            User(name="user 1", email="user2@localhost.host", password="test", groups=[group])
        ]

        self.tags = [
            Tag(name='tag 0 user 0', user=self.users[0]),
            Tag(name='tag 1 user 0', user=self.users[0]),
            Tag(name='tag 0 user 1', user=self.users[1]),
        ]

        db.add_all(self.tags)
        db.flush()

    def test_create(self):
        user0 = db.query(User).filter(User.email == "user0@localhost.host").first()
        self.assertEquals(user0, self.users[0])

    def test_get_names_from_str(self):
        self.assertListEqual(Tag.get_names_from_str(""), [])
        self.assertListEqual(Tag.get_names_from_str(",,,,"), [])
        self.assertListEqual(Tag.get_names_from_str(",  ,"), [])
        self.assertListEqual(Tag.get_names_from_str(",  , ,"), [])
        self.assertListEqual(Tag.get_names_from_str("tag"), ["tag"])
        self.assertListEqual(Tag.get_names_from_str("tag   spaces"), ["tag spaces"])
        self.assertListEqual(Tag.get_names_from_str("tag 1, tag 2"), ["tag 1", "tag 2"])
        self.assertListEqual(Tag.get_names_from_str(",,,tag 1, tag 2"), ["tag 1", "tag 2"])
        self.assertListEqual(Tag.get_names_from_str("tag  1,,, tag 2"), ["tag 1", "tag 2"])
        self.assertListEqual(Tag.get_names_from_str("tag 1, tag 2,,,"), ["tag 1", "tag 2"])
        self.assertListEqual(Tag.get_names_from_str("tag, tag"), ["tag"])

    def test_by_names(self):
        self.assertListEqual(Tag.by_names(["tag 0 user 0"], self.users[0]).all(), [self.tags[0]])
        self.assertListEqual(Tag.by_names(["tag 1 user 0"], self.users[0]).all(), [self.tags[1]])
        self.assertListEqual(Tag.by_names(["tag 0 user 0", "tag 1 user 0"], self.users[0]).all(), self.tags[0:2])
        self.assertListEqual(Tag.by_names(["tag 0 user 0", "tag 1 user 0"], self.users[1]).all(), [])
