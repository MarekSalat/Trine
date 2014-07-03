from trine.tests import TrineControllerTestCase

__author__ = 'Marek'


class TestApiCrudRestController(TrineControllerTestCase):

    def test_get_all(self):
        response = self.app.get('/')
        print(response)