import json
import urllib.request
import urllib.parse
from typing import List, Set

import os
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponseForbidden
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from swiss.core import lib_league, lib_user
from swiss.core import lib_player
from swiss.core import lib_round
from swiss.models.league import League
from swiss.models.match import Match
from swiss.models.player import Player
from swiss.models.round import Round
from swiss.models.user import User


@csrf_exempt
def v_auth_facebook(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        return JsonResponse(authenticate_facebook(data))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def authenticate_facebook(data: dict) -> dict:
    params = urllib.parse.urlencode({
        'client_id': data['clientId'],
        'redirect_uri': data['redirectUri'],
        'client_secret': os.environ['SWISS_FACEBOOK_CLIENT_SECRET'],
        'code': data['code']
    })
    url = 'https://graph.facebook.com/v2.11/oauth/access_token?%s' % params
    with urllib.request.urlopen(url) as res:
        token_info = json.loads(res.read().decode('utf-8'))

    params = urllib.parse.urlencode({
        'access_token': token_info['access_token']
    })
    url = 'https://graph.facebook.com/v2.11/me?%s' % params
    with urllib.request.urlopen(url) as res:
        profile = json.loads(res.read().decode('utf-8'))

    lib_user.register('facebook', profile['id'], token_info['access_token'], token_info['expires_in'])

    token_info.update(profile)
    return token_info


@csrf_exempt
def v_league(request: HttpRequest) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        return JsonResponse(create_league(user, data))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def create_league(user: User, data: dict) -> dict:
    m_league = lib_league.create(user, data['title'])

    return model_to_dict(m_league)


def v_leagues(request: HttpRequest) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'GET':
        return JsonResponse(get_leagues(user))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_leagues(user: User) -> dict:
    leagues = user.leagues.order_by('-pk')
    result = [model_to_dict(m_league) for m_league in leagues]
    return {'leagues': result}


@csrf_exempt
def v_a_league(request: HttpRequest, league_id: int) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'GET':
        return JsonResponse(get_league(user, league_id))
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        return JsonResponse(edit_league(user, league_id, data))
    elif request.method == 'DELETE':
        return JsonResponse(remove_league(user, league_id))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_league(user: User, league_id: int) -> dict:
    m_league = get_object_or_404(League, pk=league_id, user_id=user.id)

    return {'league': model_to_dict(m_league),
            'players': __get_players(m_league),
            'rounds': __get_rounds(m_league)}


def __get_players(m_league: League) -> List[dict]:
    players, matches = m_league.get_players_and_matches()  # type: Set[Player], List[Match]
    lib_league.calculate_matches_result(matches)
    lib_league.calculate_rankings(players)

    players = sorted(players, key=lambda p: p.ranking)  # type: List[Player]

    return [m_player.to_dict() for m_player in players if m_player.is_ghost is False]


def __get_rounds(m_league: League) -> List[dict]:
    rounds = m_league.rounds.order_by('-pk')
    return [model_to_dict(m_round) for m_round in rounds]


def edit_league(user: User, league_id: int, data: dict) -> dict:
    m_league = get_object_or_404(League, pk=league_id, user_id=user.id)
    m_league.title = data['title']
    m_league.save()

    return model_to_dict(m_league)


def remove_league(user: User, league_id: int) -> dict:
    m_league = get_object_or_404(League, pk=league_id, user_id=user.id)
    m_league.delete()

    return model_to_dict(m_league)


@csrf_exempt
def v_player(request: HttpRequest, league_id: int) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        return JsonResponse(add_player(user, league_id, data))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def add_player(user: User, league_id: int, data: dict) -> dict:
    m_league = get_object_or_404(League, pk=league_id, user_id=user.id)

    # TODO 같은 이름의 플레이어가 있는지 체크하기

    memo = ''
    if 'memo' in data:
        memo = data['memo']
    m_player = lib_player.add(m_league, data['name'], memo)

    return model_to_dict(m_player)


@csrf_exempt
def v_a_player(request: HttpRequest, league_id: int, player_id: int) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'GET':
        return JsonResponse(get_player(league_id, player_id))
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        return JsonResponse(edit_player(league_id, player_id, data))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_player(league_id: int, player_id: int) -> dict:
    m_this_player = get_object_or_404(Player, pk=player_id, league_id=league_id)  # type: Player

    players, matches = m_this_player.league.get_players_and_matches()  # type: Set[Player], List[Match]
    lib_league.calculate_matches_result(matches)
    lib_league.calculate_rankings(players)

    m_this_player = [m_player for m_player in players if m_player.id == player_id][0]

    # matches_history
    dict_matches_history = []
    matches_history = [m_match for m_match in matches
                       if m_match.player1_id == player_id or m_match.player2_id == player_id]
    for m_match in matches_history:
        dict_match = model_to_dict(m_match)

        m_opponent, my_score, your_score = (m_match.player2, m_match.score1, m_match.score2) \
            if m_match.player1_id == player_id \
            else (m_match.player1, m_match.score2, m_match.score1)
        dict_match['opponent'] = m_opponent.to_dict()
        dict_match['result'] = 'W' if my_score > your_score else ('L' if my_score < your_score else 'D')

        dict_matches_history.append(dict_match)

    dict_this_player = m_this_player.to_dict()

    # family
    family_member_ids = m_this_player.family.values_list('id', flat=True)
    family = [m_player for m_player in players if (m_player.id in family_member_ids)]
    dict_family = []
    for m_family_member in family:
        dict_family.append(m_family_member.to_dict())
    dict_this_player['family'] = dict_family

    return {'player': dict_this_player, 'matches': dict_matches_history}


def edit_player(league_id: int, player_id: int, data: dict) -> dict:
    m_player = get_object_or_404(Player, pk=player_id, league_id=league_id)  # type: Player

    if 'name' in data:
        m_player.name = data['name']
        m_player.memo = data['memo']
        m_player.save()
    elif 'is_dropped' in data:
        m_player.is_dropped = data['is_dropped']
        m_player.save()
    elif 'family' in data:
        for m_family_member in m_player.family.all():
            m_family_member.family.clear()
            m_family_member.is_family = False
            m_family_member.save()

        m_player.family.clear()
        m_player.is_family = False
        m_player.save()

        family = [m_player]
        for family_member_id in data['family']:
            try:
                m_family_member = Player.objects.get(pk=family_member_id)
                m_family_member.family.clear()
                family.append(m_family_member)
            except ObjectDoesNotExist:
                continue
        while family:
            m_person = family.pop()
            for m_family_member in family:
                m_person.family.add(m_family_member)
                m_family_member.is_family = True
            m_person.is_family = True
            m_person.save()

    return get_player(league_id, player_id)


@csrf_exempt
def v_round(request: HttpRequest, league_id: int) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'POST':
        return JsonResponse(start_new_round(user, league_id))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def start_new_round(user: User, league_id: int) -> dict:
    m_league = get_object_or_404(League, pk=league_id, user_id=user.id)
    m_round = lib_round.start_new_round(m_league)

    if m_round is None:
        return {'id': None}

    return model_to_dict(m_round)


@csrf_exempt
def v_a_round(request: HttpRequest, league_id: int, round_id: int) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'GET':
        return JsonResponse(get_round(league_id, round_id))
    elif request.method == 'DELETE':
        return JsonResponse(remove_round(league_id, round_id))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def get_round(league_id: int, round_id: int) -> dict:
    m_round = get_object_or_404(Round, pk=round_id, league_id=league_id)

    return {'round': model_to_dict(m_round), 'matches': __get_matches(m_round)}


def __get_matches(m_round: Round) -> List[dict]:
    players, matches = m_round.league.get_players_and_matches()  # type: Set[Player], List[Match]
    lib_league.calculate_matches_result([m for m in matches if m.round_id < m_round.id])

    result = []
    matches = [m for m in matches if m.round_id == m_round.id]
    for match in matches:
        dict_match = model_to_dict(match)
        dict_match['player1'] = match.player1.to_dict()
        dict_match['player2'] = match.player2.to_dict()
        result.append(dict_match)

    return result


def remove_round(league_id: int, round_id: int) -> dict:
    m_round = get_object_or_404(Round, pk=round_id, league_id=league_id)
    m_round.delete()

    return model_to_dict(m_round)


@csrf_exempt
def v_a_match(request: HttpRequest, league_id: int, round_id: int, match_id: int) -> HttpResponse:
    user = lib_user.get_user(request)
    if user is None:
        return HttpResponseForbidden('Invalid authorization')

    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        return JsonResponse(update_score(league_id, round_id, match_id, data))

    return HttpResponseBadRequest('The {} method is not supported.'.format(request.method))


def update_score(league_id: int, round_id: int, match_id: int, data: dict) -> dict:
    match = get_object_or_404(Match, pk=match_id, league_id=league_id, round_id=round_id)

    match.score1 = data['score1']
    match.score2 = data['score2']
    match.save()

    return get_round(league_id, round_id)
