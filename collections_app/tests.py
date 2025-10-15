from django.test import TestCase


class CollectionsAppSmokeTest(TestCase):
    def test_imports(self):
        from . import models
        self.assertIsNotNone(models)
