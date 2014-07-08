from trine import model
from trine.model import User
from trine.tests import TrineControllerTestCase

__author__ = 'Marek'


class TestApiCrudRestController(TrineControllerTestCase):
    def setUp(self):
        super().setUp()

        self.defaultEnviron = {'REMOTE_USER': 'mareks'}
        self.defaultHeader = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.defaults = dict(extra_environ=self.defaultEnviron, headers=self.defaultHeader)

    def test_get_all(self):
        resp = self.app.get('/api/v1/quick-key/tag', status=200, **self.defaults)