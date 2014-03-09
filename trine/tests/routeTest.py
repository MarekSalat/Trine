from unittest import TestCase
from trine.tests.route import Route

__author__ = 'Marek'


class TestTag(TestCase):
    def setUp(self):
        self.route = Route('{controller}/{action}/{id}', defaults={'controller': 'home', 'action': 'index', 'id': None})

    def test_routePattern(self):
        print(self.route.pattern)

    def test_routeMatch__slash(self):
        r1 = self.route.match('home/index/5/')
        self.assertIsNotNone(r1)

        r2 = self.route.match('home/index/5')
        self.assertIsNotNone(r2)

        self.assertEqual(r1, r2, 'should remove slash at the of string')

        r1 = self.route.match('home/index/5/?test=5')
        self.assertIsNotNone(r1)

        r2 = self.route.match('home/index/5?test=5')
        self.assertIsNotNone(r2)

        self.assertEqual(r1, r2, 'should remove slash in front of query string')

    def test_routeMatch_full(self):
        self.assertIsNotNone(self.route.match('home/index/5'))

    def test_routeMatch_queryString(self):
        self.assertIsNotNone(self.route.match('home/index?id=5'))
        self.assertIsNotNone(self.route.match('home?action=index&id=5'))
        self.assertIsNotNone(self.route.match('?controller=home&action=index&id=5'))

    def test_routeMatch_without_id(self):
        self.assertIsNotNone(self.route.match('home/index'))

    def test_routeMatch_without_index(self):
        self.assertIsNotNone(self.route.match('home'))

    def test_routeMatch_completely_default(self):
        self.assertIsNotNone(self.route.match(''))

