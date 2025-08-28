from otree.api import *
import random

class Instructions(Page):
    def is_displayed(player):
        return player.round_number == 1

class Bid(Page):
    form_model = 'player'
    form_fields = ['bid']

    def before_next_page(player, timeout_happened):
        # Assign valuation only in round 1
        if player.round_number == 1:
            player.valuation = round(random.uniform(0.10, 1.00), 2)
        else:
            # Copy valuation from previous round
            player.valuation = player.in_round(1).valuation

class ResultsWaitPage(WaitPage):
    group_by_arrival_time = False  # Fixed pairing across rounds

    def after_all_players_arrive(group):
        p1, p2 = group.get_players()
        p1.opponent_bid = p2.bid
        p2.opponent_bid = p1.bid

        for p in [p1, p2]:
            if p.bid > p.opponent_bid:
                p.payoff = round(p.valuation - p.bid, 2)
            elif p.bid == p.opponent_bid:
                p.payoff = round((p.valuation - p.bid) / 2, 2)
            else:
                p.payoff = 0

class Results(Page):
    def vars_for_template(player):
        return dict(
            valuation=player.valuation,
            bid=player.bid,
            opponent_bid=player.opponent_bid,
            payoff=player.payoff,
        )

page_sequence = [Instructions, Bid, ResultsWaitPage, Results]


