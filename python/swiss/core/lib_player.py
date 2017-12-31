from typing import List, Set

from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.match import Match


def add(league: League, name: str, memo: str) -> Player:
    player = Player()
    player.name = name
    if memo:
        player.memo = memo
    player.league = league
    player.save()

    return player


def get_players(league: League) -> List[Player]:
    return league.players.order_by('name')


def get_wins(player: Player, matches: Set[Match]) -> int:
    player.wins = 0

    for match in matches:
        if match.player1_id == player.id and match.score1 > match.score2:
            player.wins += 1
        if match.player2_id == player.id and match.score2 > match.score1:
            player.wins += 1

    return player.wins


def get_round_results(player: Player, matches: Set[Match]) -> dict:
    wins, draws, loses = 0, 0, 0
    strikes, max_strikes = 0, 0

    for match in matches:
        if match.player1_id == player.id:
            if match.score1 > match.score2:
                wins += 1
                strikes += 1
                if strikes > max_strikes:
                    max_strikes = strikes
            elif match.score1 < match.score2:
                loses += 1
                strikes = 0
            else:
                draws += 1
                strikes = 0
        if match.player2_id == player.id:
            if match.score2 > match.score1:
                wins += 1
                strikes += 1
                if strikes > max_strikes:
                    max_strikes = strikes
            elif match.score2 < match.score1:
                loses += 1
                strikes = 0
            else:
                draws += 1
                strikes = 0

    return {
        wins: wins,
        draws: draws,
        loses: loses,
        strikes: max_strikes
    }
