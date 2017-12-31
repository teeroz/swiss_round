from django.db import models

from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.round import Round


class Match(models.Model):
    league = models.ForeignKey(League, related_name='matches', on_delete=models.CASCADE)
    round = models.ForeignKey(Round, related_name='matches', on_delete=models.CASCADE)
    player1 = models.ForeignKey(Player, related_name='matches1', on_delete=models.DO_NOTHING)
    player2 = models.ForeignKey(Player, related_name='matches2', on_delete=models.DO_NOTHING, null=True)
    score1 = models.PositiveSmallIntegerField(default=0)
    score2 = models.PositiveSmallIntegerField(default=0)
    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '{} vs {}'.format(self.player1, self.player2)
