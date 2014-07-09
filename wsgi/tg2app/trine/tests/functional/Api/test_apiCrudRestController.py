import json
from trine import model
from trine.model import User, Transaction, DBSession as db
from trine.tests import TrineControllerTestCase

__author__ = 'Marek'


class TestApiCrudRestController(TrineControllerTestCase):
    def setUp(self):
        super().setUp()

        self.defaultEnviron = {'REMOTE_USER': 'mareks'}
        self.defaultHeader = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.defaults = dict(extra_environ=self.defaultEnviron, headers=self.defaultHeader)

    def test_get_all(self):
        resp = self.app.get('/api/v1/quick-key/transaction?limit=2', status=200, **self.defaults)
        self.assertEquals(resp.json_body['entries'], 2)
        self.assertEquals(resp.json_body['total_entries'], 8)

        resp = self.app.get('/api/v1/quick-key/transaction?order_by=date|desc;amount|desc', status=200, **self.defaults)
        print(json.dumps(resp.json_body, sort_keys=True, indent=4))

    def test_get_one(self):
        id = db.query(Transaction).limit(0).first().id
        resp = self.app.get('/api/v1/quick-key/transaction/%s' % id, status=200, **self.defaults)

    def test_post(self):
        transaction = dict(amount=42, incomeTagGroup=['tag'], expenseTagGroup=['tag1', 'tag2'])
        resp = self.app.post_json('/api/v1/quick-key/transaction', params=transaction, **self.defaults)

        print(resp.json_body)