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
        self.assertGreaterEqual(resp.json_body['total_entries'], 2)

        self.app.get('/api/v1/quick-key/transaction?order_by=date|desc;amount|desc', status=200, **self.defaults)

    def test_get_one(self):
        id = db.query(Transaction).limit(0).first().id
        resp = self.app.get('/api/v1/quick-key/transaction/%s' % id, status=200, **self.defaults)
        self.assertIsNotNone(resp.json_body['value'])
        self.assertEquals(resp.json_body['value']['id'], str(id))

    def test_post(self):
        transaction = dict(amount=42, incomeTagGroup=['tag'], expenseTagGroup=['tag1', 'tag2'])
        resp = self.app.post_json('/api/v1/quick-key/transaction', params=transaction, **self.defaults)

        self.assertTrue('value' in resp.json_body)
        trans1 = resp.json_body['value']

        self.assertEqual(trans1['amount'], 42)
        self.assertEqual(len(trans1['incomeTagGroup']['tags']), 1)
        self.assertEqual(len(trans1['expenseTagGroup']['tags']), 2)
        self.assertEqual(trans1['incomeTagGroup']['tags'][0]['name'], 'tag')
        self.assertListEqual(sorted([tag['name'] for tag in trans1['expenseTagGroup']['tags']]), ['tag1', 'tag2'])

        resp2 = self.app.post_json('/api/v1/quick-key/transaction', params=transaction, status=200, **self.defaults)
        trans2 = resp.json_body['value']

        self.assertEqual(trans2['incomeTagGroup'], resp2.json_body['value']['incomeTagGroup'])
        self.assertEqual(trans2['expenseTagGroup'], resp2.json_body['value']['expenseTagGroup'])

        transaction['incomeTagGroup_id'] = trans2['incomeTagGroup']['id']
        transaction['expenseTagGroup_id'] = trans2['expenseTagGroup']['id']

        resp3 = self.app.post_json('/api/v1/quick-key/transaction', params=transaction, status=200, **self.defaults)
        trans3 = resp3.json_body['value']

        self.assertEqual(trans1['incomeTagGroup'], trans3['incomeTagGroup'])
        self.assertEqual(trans1['expenseTagGroup'], trans3['expenseTagGroup'])

    def test_post_as_transfer(self):
        transaction = dict(amount=-500, incomeTagGroup=['from account'], expenseTagGroup=['to account'])
        resp = self.app.post_json('/api/v1/quick-key/transaction?as_transfer=1', params=transaction, status=200,
                                  **self.defaults)
        trans = resp.json_body['value_list']

        self.assertEqual(len(trans), 2)
        self.assertEqual(trans[0]['incomeTagGroup']['tags'][0]['name'], 'from account')
        self.assertEqual(trans[1]['incomeTagGroup']['tags'][0]['name'], 'to account')

    def test_put(self):
        id = db.query(Transaction).filter(Transaction.transferKey != None).limit(0).first().id
        new_transaction = dict(amount=-500, incomeTagGroup=['tag1'])

        resp = self.app.put_json('/api/v1/quick-key/transaction/%s' % id, new_transaction, status=200, **self.defaults)
        resp2 = self.app.get('/api/v1/quick-key/transaction/%s' % id, status=200, **self.defaults)

        self.assertEqual(resp.json_body, resp2.json_body)