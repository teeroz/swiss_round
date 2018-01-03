import random

from django.test import TestCase

from swiss.core import lib_round
from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.round import Round
from swiss.models.match import Match


class Tests(TestCase):
    league = {}
    players = {}
    rounds = {}
    matches = []
    players_by_wins = {}

    def setUp(self):
        self.league = League.objects.create(title='4th')

        for i in range(0, 19):
            self.players[i] = Player.objects.create(league=self.league, name='p{:2d}'.format(i))

        matches = {
            1: [(10, 5), (7, 6), (13, 8), (3, 1), (9, 4), (2, 11), (12, 0)],
            2: [(3, 2), (7, 9), (10, 12), (14, 13), (16, 15), (17, 18), (1, 4), (5, 6), (8, 11)],
            3: [(3, 7), (14, 10), (16, 17), (1, 2), (8, 5), (13, 9), (18, 15), (6, 4), (11, 0)],
            4: [(14, 3), (1, 16), (7, 8), (10, 13), (2, 17), (18, 5), (9, 6), (11, 15), (4, 0)],
            5: [(1, 14), (3, 10), (7, 16), (18, 2), (8, 9), (11, 13), (4, 5), (6, 15)],
            # 6: [(3, 8), (7, 1), (10, 11), (14, 18), (16, 9), (2, 6), (13, 4), (12, 5), (17, 15)],
            # 7: [(3, 11), (14, 7), (10, 1), (13, 2), (16, 8), (4, 18), (12, 6), (9, 17), (15, 5)],
            # 8: [(3, 16), (2, 14), (10, 7), (1, 13), (9, 18), (12, 11), (4, 15), (6, 8), (17, 5)],
            # 9: [(3, 9), (10, 2), (12, 1), (13, 7), (16, 14), (17, 4), (8, 15), (18, 6), (11, 5)],
            # 10: [(13, 3), (16, 10), (1, 9), (14, 12), (7, 15), (2, 5), (8, 18), (4, 11), (17, 6)],
            # 11: [(3, 17), (10, 4), (8, 14), (1, 18), (12, 7), (13, 16), (2, 15), (9, 5), (11, 6)],
            # 12: [(3, 12), (10, 8), (17, 1), (18, 13), (14, 11), (6, 16), (7, 5), (4, 2), (15, 9)],
            # 13: [(4, 3), (17, 10), (14, 9), (7, 2), (13, 6), (8, 1), (15, 12), (16, 5), (18, 11)],
            # 14: [(3, 18), (10, 9), (15, 13), (17, 7), (14, 6), (1, 5), (4, 8), (11, 16), (2, 12)],
            # 15: [(3, 15), (10, 18), (4, 14), (7, 11), (6, 1), (5, 13), (8, 17), (16, 2), (9, 12)],
            # 16: [(3, 6), (10, 15), (14, 5), (7, 4), (1, 11), (16, 18), (8, 12), (13, 17), (2, 9)],
            # 17: [(3, 5), (10, 6), (14, 17), (7, 18), (1, 15), (13, 12), (8, 2), (16, 4), (9, 11)],
        }

        for round_idx, matches in matches.items():
            self.rounds[round_idx] = Round.objects.create(league=self.league, no=round_idx)

            for winner_idx, loser_idx in matches:
                match = Match.objects.create(league=self.league, round=self.rounds[round_idx],
                                             player1=self.players[winner_idx], player2=self.players[loser_idx],
                                             score1=1, score2=0)
                self.matches.append(match)

        for m_player in self.players.values():
            m_player.wins = 0
            m_player.matched = set()

        # noinspection PyTypeChecker
        lib_round._calculate_wins(self.matches)
        # noinspection PyTypeChecker
        lib_round._calculate_matched(self.matches)

    def test_calculate_wins(self):
        self.assertEqual(self.players[1].wins, 4)
        self.assertEqual(self.players[2].wins, 2)
        self.assertEqual(self.players[3].wins, 4)
        self.assertEqual(self.players[4].wins, 2)
        self.assertEqual(self.players[5].wins, 1)

    def test_calculate_matched(self):
        self.assertEqual(self.players[1].matched,
                         {self.players[3], self.players[4], self.players[2], self.players[16], self.players[14]})
        self.assertEqual(self.players[8].matched,
                         {self.players[13], self.players[11], self.players[5], self.players[7], self.players[9]})

    def test_calculate_matched_others(self):
        # noinspection PyTypeChecker
        lib_round._calculate_matched_others(self.players.values())

        self.assertEqual(self.players[1].matched_same, {self.players[3]})
        self.assertEqual(self.players[1].matched_lower, {self.players[14]})

        self.assertEqual(self.players[8].matched_same, {self.players[11]})
        self.assertEqual(self.players[8].matched_lower, {self.players[9], self.players[13]})

    """
    def test_choose_first_player(self):
        # noinspection PyTypeChecker
        lib_round._calculate_matched_others(self.players.values())

        # noinspection PyTypeChecker
        player = lib_round._choose_first_player(self.players.values())
        self.assertEqual(player, self.players[3])

    def test_choose_second_player(self):
        players = set(self.players.values())  # type: Set[Player]

        player1 = lib_round._choose_first_player(players)
        self.assertEqual(player1, self.players[3])

        player2 = lib_round._choose_second_player(player1, players)
        self.assertIn(player2, {self.players[8], self.players[11]})

        players.remove(player1)
        players.remove(player2)

        player1 = lib_round._choose_first_player(players)
        self.assertIn(player1, {self.players[1], self.players[7]})

        player2 = lib_round._choose_second_player(player1, players)
        self.assertIn(player2, {self.players[1], self.players[7]})
    """

    def test_make_matches(self):
        league = League.objects.create(title='5th')

        players = set()
        for i in range(1, 13):
            players.add(Player.objects.create(league=league, name='p{:2d}'.format(i)))

        rounds = set()
        matches = set()
        for round_idx in range(1, 12):
            this_matches = lib_round._get_matches_of_new_round(players, matches)
            if this_matches is None:
                break

            the_round = Round.objects.create(league=league, no=round_idx)
            rounds.add(the_round)

            for player1, player2 in this_matches:
                if random.random() > .3:
                    winner = player1
                    loser = player2
                else:
                    winner = player2
                    loser = player1

                match = Match.objects.create(league=league, round=the_round,
                                             player1=winner, player2=loser,
                                             score1=1, score2=0)
                matches.add(match)

        for m_player in self.players.values():
            m_player.wins = 0
            m_player.matched = set()

        lib_round._calculate_wins(matches)
        lib_round._calculate_matched(matches)

        for player in sorted(players, key=lambda p: (p.wins, p.name), reverse=True):
            print('Player #{} {} wins / {}'.format(player.name, player.wins, len(player.matched)))
            self.assertEqual(len(player.matched), len(rounds))
