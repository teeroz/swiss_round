from django.db import models
from django.forms import model_to_dict

from swiss.models.league import League


class Player(models.Model):
    league = models.ForeignKey(League, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    memo = models.CharField(max_length=64, default='')
    is_ghost = models.BooleanField(default=False)
    is_dropped = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)
    family = models.ManyToManyField("self", symmetrical=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)

    wins = 0
    draws = 0
    loses = 0
    strikes_count = 0
    strikes_start = 0
    max_strikes_count = 0
    max_strikes_start = 0

    matched = set()
    matched_wins = set()
    matched_loses = set()
    matched_same = set()
    matched_lower = set()

    opponents_total_wins = 0
    ranking = 0

    def __str__(self) -> str:
        return str(self.name)

    def initialize_results(self) -> None:
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.strikes_count = 0
        self.strikes_start = 0
        self.max_strikes_count = 0
        self.max_strikes_start = 0
        self.matched = set()
        self.matched_wins = set()
        self.matched_loses = set()

    def increase_wins(self, opponent) -> None:
        self.wins += 1
        if self.strikes_count <= 0:
            self.strikes_start = self.wins + self.draws + self.loses
        self.strikes_count += 1
        if self.strikes_count > self.max_strikes_count:
            self.max_strikes_start = self.strikes_start
            self.max_strikes_count = self.strikes_count

        self.matched_wins.add(opponent)

    def increase_draws(self) -> None:
        self.draws += 1
        self.strikes_count = 0

    def increase_loses(self, opponent) -> None:
        self.loses += 1
        self.strikes_count = 0

        self.matched_loses.add(opponent)

    def initialize_ranking(self) -> None:
        self.opponents_total_wins = 0
        self.ranking = 0

    def to_dict(self) -> dict:
        to_dict = model_to_dict(self, exclude="family")
        to_dict.update({
            'wins': self.wins,
            'draws': self.draws,
            'loses': self.loses,
            'max_strikes_count': self.max_strikes_count,
            'max_strikes_start': self.max_strikes_start,
            'opponents_total_wins': self.opponents_total_wins,
            'ranking': self.ranking
        })

        return to_dict
