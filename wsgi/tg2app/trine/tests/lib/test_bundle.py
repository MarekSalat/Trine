from unittest import TestCase
from trine.lib.bundels import Bundle

__author__ = 'Marek'


class TestBundle(TestCase):
    def test_version(self):
        bundle = Bundle("/github/Trine/wsgi/tg2app/trine/public/bundles/app.js", [
            "/github/Trine/wsgi/tg2app/trine/public/javascript/controllers.js",
            "/github/Trine/wsgi/tg2app/trine/public/javascript/services.js",
            "/github/Trine/wsgi/tg2app/trine/public/javascript/modules.js"
        ])

        print(bundle.version)
