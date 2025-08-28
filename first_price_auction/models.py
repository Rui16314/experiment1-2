from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'first_price_auction'  # Change to 'repeated_first_price_fixed' for Session 2
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    valuation = models.FloatField()
    bid = models.FloatField(min=0, max=1)
    opponent_bid = models.FloatField()
    payoff = models.FloatField()

