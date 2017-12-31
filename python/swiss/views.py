import json
from typing import List, Set

from django.forms import model_to_dict
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from swiss.core import lib_league
from swiss.core import lib_player
from swiss.core import lib_round
from swiss.models.league import League
from swiss.models.match import Match
from swiss.models.player import Player
from swiss.models.round import Round


@csrf_exempt
def v_league(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        return create_league(request)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def create_league(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body.decode('utf-8'))
    league = lib_league.create(data['title'])

    return JsonResponse(model_to_dict(league))


@csrf_exempt
def v_leagues(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return get_leagues()

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_leagues() -> JsonResponse:
    leagues = League.objects.order_by('-pk')
    result = [model_to_dict(m_league) for m_league in leagues]
    return JsonResponse({'leagues': result})


@csrf_exempt
def v_a_league(request: HttpRequest, league_id: int) -> HttpResponse:
    if request.method == 'GET':
        return get_league(league_id)
    elif request.method == 'PUT':
        return edit_league(request, league_id)
    elif request.method == 'DELETE':
        return remove_league(league_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_league(league_id: int) -> JsonResponse:
    m_league = get_object_or_404(League, pk=league_id)
    return JsonResponse(model_to_dict(m_league))


def edit_league(request: HttpRequest, league_id: int) -> JsonResponse:
    data = json.loads(request.body.decode('utf-8'))

    m_league = get_object_or_404(League, pk=league_id)
    m_league.title = data['title']
    m_league.save()

    return JsonResponse(model_to_dict(m_league))


def remove_league(league_id: int) -> JsonResponse:
    m_league = get_object_or_404(League, pk=league_id)
    m_league.delete()
    return JsonResponse(model_to_dict(m_league))


@csrf_exempt
def v_player(request: HttpRequest, league_id: int) -> HttpResponse:
    if request.method == 'POST':
        return add_player(request, league_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def add_player(request: HttpRequest, league_id: int) -> JsonResponse:
    m_league = get_object_or_404(League, pk=league_id)

    # TODO 같은 이름의 플레이어가 있는지 체크하기

    data = json.loads(request.body.decode('utf-8'))
    memo = ''
    if 'memo' in data:
        memo = data['memo']
    player = lib_player.add(m_league, data['name'], memo)

    return JsonResponse(model_to_dict(player))


@csrf_exempt
def v_a_player(request: HttpRequest, league_id: int, player_id: int) -> HttpResponse:
    if request.method == 'GET':
        return get_player(league_id, player_id)
    elif request.method == 'PUT':
        return edit_player(request, league_id, player_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_player(league_id: int, player_id: int) -> JsonResponse:
    m_player = get_object_or_404(Player, pk=player_id, league_id=league_id)  # type: Player

    players, matches = m_player.league.get_players_and_matches()  # type: Set[Player], List[Match]
    lib_league.calculate_matches_result(matches)
    lib_league.calculate_rankings(players)

    m_player = [m_player for m_player in players if m_player.id == player_id][0]

    # matches_history
    dict_matches_history = []
    matches_history = [m_match for m_match in matches
                       if m_match.player1_id == player_id or m_match.player2_id == player_id]
    for m_match in matches_history:
        dict_match = model_to_dict(m_match)

        opponent, my_score, your_score = (m_match.player2, m_match.score1, m_match.score2) \
            if m_match.player1_id == player_id \
            else (m_match.player1, m_match.score2, m_match.score1)
        dict_match['opponent'] = opponent.to_dict()
        dict_match['result'] = 'W' if my_score > your_score else ('L' if my_score < your_score else 'D')

        dict_matches_history.append(dict_match)

    return JsonResponse({'player': m_player.to_dict(), 'matches': dict_matches_history})


def edit_player(request: HttpRequest, league_id: int, player_id: int) -> JsonResponse:
    m_player = get_object_or_404(Player, pk=player_id, league_id=league_id)  # type: Player

    data = json.loads(request.body.decode('utf-8'))

    if 'name' in data:
        m_player.name = data['name']
        m_player.memo = data['memo']
        m_player.save()
    elif 'is_dropped' in data:
        m_player.is_dropped = data['is_dropped']
        m_player.save()

    return get_player(league_id, player_id)


@csrf_exempt
def v_players(request: HttpRequest, league_id: int) -> HttpResponse:
    if request.method == 'GET':
        return get_players(league_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_players(league_id: int) -> JsonResponse:
    m_league = get_object_or_404(League, pk=league_id)

    players, matches = m_league.get_players_and_matches()  # type: Set[Player], List[Match]
    lib_league.calculate_matches_result(matches)
    lib_league.calculate_rankings(players)

    players = sorted(players, key=lambda p: p.ranking)  # type: List[Player]

    result = [player.to_dict() for player in players if player.is_ghost is False]
    return JsonResponse({'players': result})


@csrf_exempt
def v_rounds(request: HttpRequest, league_id: int) -> HttpResponse:
    if request.method == 'GET':
        return get_rounds(league_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_rounds(league_id: int) -> JsonResponse:
    m_league = get_object_or_404(League, pk=league_id)
    rounds = m_league.rounds.order_by('-pk')
    result = [model_to_dict(m_round) for m_round in rounds]
    return JsonResponse({'rounds': result})


@csrf_exempt
def v_round(request: HttpRequest, league_id: int) -> HttpResponse:
    if request.method == 'POST':
        return start_new_round(league_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def start_new_round(league_id: int) -> JsonResponse:
    m_league = get_object_or_404(League, pk=league_id)
    m_round = lib_round.start_new_round(m_league)
    return JsonResponse(model_to_dict(m_round))


@csrf_exempt
def v_a_round(request: HttpRequest, league_id: int, round_id: int) -> HttpResponse:
    if request.method == 'GET':
        return get_round(league_id, round_id)
    elif request.method == 'DELETE':
        return remove_round(league_id, round_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_round(league_id: int, round_id: int) -> JsonResponse:
    m_round = get_object_or_404(Round, pk=round_id, league_id=league_id)

    return JsonResponse(model_to_dict(m_round))


def remove_round(league_id: int, round_id: int) -> JsonResponse:
    m_round = get_object_or_404(Round, pk=round_id, league_id=league_id)
    m_round.delete()

    return JsonResponse(model_to_dict(m_round))


@csrf_exempt
def v_matches(request: HttpRequest, league_id: int, round_id: int) -> HttpResponse:
    if request.method == 'GET':
        return get_matches(league_id, round_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_matches(league_id: int, round_id: int) -> JsonResponse:
    m_round = get_object_or_404(Round, pk=round_id, league_id=league_id)

    players, matches = m_round.league.get_players_and_matches()  # type: Set[Player], List[Match]
    lib_league.calculate_matches_result([m_match for m_match in matches if m_match.round_id < m_round.id])

    result = []
    matches = [m_match for m_match in matches if m_match.round_id == m_round.id]
    for match in matches:
        dict_match = model_to_dict(match)
        dict_match['player1'] = match.player1.to_dict()
        dict_match['player2'] = match.player2.to_dict()
        result.append(dict_match)

    return JsonResponse({'round': model_to_dict(m_round), 'matches': result})


@csrf_exempt
def v_a_match(request: HttpRequest, league_id: int, round_id: int, match_id: int) -> HttpResponse:
    if request.method == 'PUT':
        return update_score(request, league_id, round_id, match_id)

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def update_score(request: HttpRequest, league_id: int, round_id: int, match_id: int) -> JsonResponse:
    match = get_object_or_404(Match, pk=match_id, league_id=league_id, round_id=round_id)

    data = json.loads(request.body.decode('utf-8'))
    match.score1 = data['score1']
    match.score2 = data['score2']
    match.save()

    return get_matches(league_id, round_id)
