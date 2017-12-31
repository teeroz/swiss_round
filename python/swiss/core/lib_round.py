import random
from typing import Set, Optional

from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.round import Round
from swiss.models.match import Match


def start_new_round(league: League) -> Optional[Round]:
    players = league.players.all()
    rounds = league.rounds.all()
    matches = league.matches.all()

    # matches 플레이어 초기화
    dict_players = {}
    for player in players:
        dict_players[player.id] = player
    for match in matches:
        match.player1 = dict_players[match.player1_id]
        match.player2 = dict_players[match.player2_id]

    new_matches = _get_matches_of_new_round(players, matches)
    if new_matches is None:
        return None

    m_round = Round.objects.create(league=league, no=len(rounds)+1)

    for player1, player2 in new_matches:
        Match.objects.create(league=league, round=m_round, player1=player1, player2=player2,
                             score1=1 if player2.is_ghost is True else 0)

    return m_round


def _get_matches_of_new_round(players: Set[Player], matches: Set[Match]) -> Optional[list]:
    result = []

    _calculate_wins(matches)
    # 부전승은 항상 제일 마지막에 나오도록 하기 위함
    for player in players:
        if player.is_ghost:
            player.wins = -1

    _calculate_matched(matches)

    # 드랍한 사용자 제외
    candidates = {player for player in players if player.is_dropped is False}
    # 플레이어가 홀수라면 고스트 제외
    if len(candidates) % 2 != 0:
        candidates = {player for player in candidates if player.is_ghost is False}

    # reserved_player1 팝 되었을 때 대상 플레이어1을 저장
    reserved_player1 = None
    # blacklist 플레이어2 후보에서 제외할 플레이어
    blacklist = set()
    # result_stack 최종 결과를 저장하기 위한 스택
    result_stack = []
    while len(candidates) > 0:
        if reserved_player1:
            player1 = reserved_player1
            reserved_player1 = None
        else:
            player1 = _choose_first_player(candidates)
            candidates.remove(player1)

        player2 = _choose_second_player(player1, candidates - blacklist)

        if player2:
            candidates.remove(player2)
            result_stack.append((player1, player2, blacklist))
            blacklist = set()
        # 상대를 찾지 못한 경우
        else:
            # 첫 매치의 경우라면 라운드를 만들 수 없는 상태
            if len(result_stack) <= 0:
                return None

            reserved_player1, popped_player2, blacklist = result_stack.pop()

            candidates.add(player1)
            candidates.add(popped_player2)
            blacklist.add(popped_player2)

    for player1, player2, blacklist in result_stack:
        result.append((player1, player2))

    return result


def _calculate_wins(matches: Set[Match]) -> None:
    for match in matches:
        match.player1.wins = 0
        match.player2.wins = 0

    for match in matches:
        if match.score1 > match.score2:
            match.player1.wins += 1
        elif match.score2 > match.score1:
            match.player2.wins += 1


def _calculate_matched(matches: Set[Match]) -> None:
    for match in matches:
        match.player1.matched = set()
        match.player2.matched = set()

    for match in matches:
        match.player1.matched.add(match.player2)
        match.player2.matched.add(match.player1)


def _choose_first_player(players: Set[Player]) -> Optional[Player]:
    if len(players) <= 0:
        return None

    _calculate_matched_others(players)

    sorted_players = sorted(players,
                            key=lambda p: (p.wins, len(p.matched_same), len(p.matched_lower), random.random()),
                            reverse=True)
    return sorted_players[0]


def _choose_second_player(player: Player, players: Set[Player]) -> Optional[Player]:
    if len(players) <= 0:
        return None

    candidates = set(players)

    # 이번 상대는 제외
    if player in candidates:
        candidates.remove(player)

    # 이미 대전한 상대는 제외
    for matched_player in player.matched:
        if matched_player in candidates:
            candidates.remove(matched_player)

    # 대전할 상대가 없는 경우
    if len(candidates) <= 0:
        return None

    _calculate_matched_others(candidates)

    sorted_players = sorted(candidates,
                            key=lambda p: (p.wins, len(p.matched_same), len(p.matched_lower), random.random()),
                            reverse=True)
    return sorted_players[0]


def _calculate_matched_others(players: Set[Player]) -> None:
    # players_by_wins 승수별 플레이어 목록
    players_by_wins = {}
    for player in players:
        if player.wins not in players_by_wins:
            players_by_wins[player.wins] = set()
        players_by_wins[player.wins].add(player)

    for (wins, players) in players_by_wins.items():
        # players_lower 바로 밑의 승수 플레이어 목록
        players_lower = set()
        for lower_wins in range(wins-1, -1, -1):
            if lower_wins in players_by_wins:
                players_lower = players_by_wins[lower_wins]
                break

        # matched_same & matched_lower 계산
        for player in players:
            player.matched_same = player.matched & players
            player.matched_lower = player.matched & players_lower
