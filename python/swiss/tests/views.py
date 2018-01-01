import logging
from unittest import TestCase

from GenGoZ import settings
from swiss import views


logger = logging.getLogger(__name__)


class Tests(TestCase):
    def setUp(self):
        pass

    def test_create_league(self):
        title = 'League Title'
        result = views.create_league({'title': title})
        self.assertEqual(result['title'], title)
