from typing import List, Set

from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.match import Match


def create(title: str) -> League:
    league = League()
    league.title = title
    league.save()

    Player.objects.create(league=league, name='X', is_ghost=True)

    return league


def calculate_matches_result(matches: List[Match]) -> None:
    for match in matches:
        match.player1.initialize_results()
        match.player2.initialize_results()

    for match in matches:
        match.player1.matched.add(match.player2)
        match.player2.matched.add(match.player1)

        if match.score1 > match.score2:
            match.player1.increase_wins(match.player2)
            match.player2.increase_loses(match.player1)
        elif match.score2 > match.score1:
            match.player2.increase_wins(match.player1)
            match.player1.increase_loses(match.player2)
        else:
            match.player2.increase_draws()
            match.player1.increase_draws()


def calculate_rankings(players: Set[Player]) -> None:
    for m_player in players:
        m_player.initialize_ranking()
        # m_player.opponents_total_wins = sum([opponent.wins for opponent in m_player.matched])
        m_player.opponents_total_wins = sum([opponent.wins for opponent in m_player.matched_wins])

    sorted_players = sorted(players,
                            key=lambda p: (not p.is_ghost,
                                           p.wins * 3 + p.draws,
                                           p.opponents_total_wins,
                                           p.max_strikes_count,
                                           p.max_strikes_start * -1,
                                           p.pk * -1),
                            reverse=True)
    for idx, m_player in enumerate(sorted_players):
        m_player.ranking = idx+1
