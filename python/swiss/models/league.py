from typing import List

from django.db import models

from swiss.models.user import User


class League(models.Model):
    user = models.ForeignKey(User, related_name='leagues', on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)

    def get_players_and_matches(self) -> (List, List):
        players = self.players.all()
        matches = self.matches.order_by('pk')

        dict_players = {}
        for m_player in players:
            dict_players[m_player.id] = m_player
        for m_match in matches:
            m_match.player1 = dict_players[m_match.player1_id]
            m_match.player2 = dict_players[m_match.player2_id]

        return players, matches
