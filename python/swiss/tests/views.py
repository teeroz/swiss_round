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

    def test_edit_player_family(self):
        dict_league = views.create_league({'title': 'edit_player_family'})
        dict_player1 = views.add_player(dict_league['id'], {'name': '1', 'memo': ''})
        dict_player2 = views.add_player(dict_league['id'], {'name': '2', 'memo': ''})
        dict_player3 = views.add_player(dict_league['id'], {'name': '3', 'memo': ''})

        dict_player1 = views.edit_player(league_id=dict_league['id'],
                                         player_id=dict_player1['id'],
                                         data={'family': [dict_player2['id'], dict_player3['id']]})

        self.assertSetEqual({p['id'] for p in dict_player1['player']['family']},
                            {dict_player2['id'], dict_player3['id']})

