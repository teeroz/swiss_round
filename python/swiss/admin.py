from django.contrib import admin

from swiss.models.league import League
from swiss.models.match import Match
from swiss.models.player import Player
from swiss.models.round import Round


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass
