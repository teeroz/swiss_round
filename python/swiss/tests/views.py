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

    def test_start_new_round_for_family(self):
        dict_league = views.create_league(data={'title': 'start_new_round_for_family'})

        dict_player1 = views.add_player(league_id=dict_league['id'], data={'name': '1', 'memo': ''})
        dict_player2 = views.add_player(league_id=dict_league['id'], data={'name': '2', 'memo': ''})
        dict_player3 = views.add_player(league_id=dict_league['id'], data={'name': '3', 'memo': ''})
        dict_player4 = views.add_player(league_id=dict_league['id'], data={'name': '4', 'memo': ''})
        dict_player5 = views.add_player(league_id=dict_league['id'], data={'name': '5', 'memo': ''})
        dict_player6 = views.add_player(league_id=dict_league['id'], data={'name': '6', 'memo': ''})
        dict_player7 = views.add_player(league_id=dict_league['id'], data={'name': '7', 'memo': ''})
        dict_player8 = views.add_player(league_id=dict_league['id'], data={'name': '8', 'memo': ''})

        views.edit_player(league_id=dict_league['id'],
                          player_id=dict_player1['id'],
                          data={'family': [dict_player2['id']]})
        views.edit_player(league_id=dict_league['id'],
                          player_id=dict_player3['id'],
                          data={'family': [dict_player4['id'], dict_player5['id']]})
        views.edit_player(league_id=dict_league['id'],
                          player_id=dict_player4['id'],
                          data={'family': [dict_player3['id'], dict_player5['id']]})
        views.edit_player(league_id=dict_league['id'],
                          player_id=dict_player5['id'],
                          data={'family': [dict_player3['id'], dict_player4['id']]})

        for idx in range(1, 5, 1):
            print('===== ROUND {} ====='.format(idx))
            dict_round = views.start_new_round(league_id=dict_league['id'])
            dict_matches = views.get_round(league_id=dict_league['id'], round_id=dict_round['id'])
            for dict_match in dict_matches['matches']:
                print('----- MATCH {} vs {} -----'.format(dict_match['player1']['name'], dict_match['player2']['name']))
                self.assertNotEqual({dict_match['player1']['id'], dict_match['player2']['id']},
                                    {dict_player1['id'], dict_player2['id']})
                self.assertNotEqual({dict_match['player1']['id'], dict_match['player2']['id']},
                                    {dict_player3['id'], dict_player4['id']})
                self.assertNotEqual({dict_match['player1']['id'], dict_match['player2']['id']},
                                    {dict_player3['id'], dict_player5['id']})
                self.assertNotEqual({dict_match['player1']['id'], dict_match['player2']['id']},
                                    {dict_player4['id'], dict_player5['id']})
                views.update_score(league_id=dict_league['id'],
                                   round_id=dict_round['id'],
                                   match_id=dict_match['id'],
                                   data={'score1': 1, 'score2': 0})

    def test_start_new_round_for_ghost(self):
        dict_league = views.create_league(data={'title': 'start_new_round_for_family'})

        dict_player1 = views.add_player(league_id=dict_league['id'], data={'name': '1', 'memo': ''})
        dict_player2 = views.add_player(league_id=dict_league['id'], data={'name': '2', 'memo': ''})
        dict_player3 = views.add_player(league_id=dict_league['id'], data={'name': '3', 'memo': ''})
        dict_player4 = views.add_player(league_id=dict_league['id'], data={'name': '4', 'memo': ''})
        dict_player5 = views.add_player(league_id=dict_league['id'], data={'name': '5', 'memo': ''})
        dict_player6 = views.add_player(league_id=dict_league['id'], data={'name': '6', 'memo': ''})
        dict_player7 = views.add_player(league_id=dict_league['id'], data={'name': '7', 'memo': ''})

        for idx in range(1, 6, 1):
            print('===== ROUND {} ====='.format(idx))
            dict_round = views.start_new_round(league_id=dict_league['id'])
            dict_matches = views.get_round(league_id=dict_league['id'], round_id=dict_round['id'])
            dict_last_player = None
            for dict_match in dict_matches['matches']:
                print('----- MATCH {} vs {} -----'.format(dict_match['player1']['name'], dict_match['player2']['name']))
                views.update_score(league_id=dict_league['id'],
                                   round_id=dict_round['id'],
                                   match_id=dict_match['id'],
                                   data={'score1': 1, 'score2': 0})
                dict_last_player = dict_match['player2']
            self.assertTrue(dict_last_player['is_ghost'])
