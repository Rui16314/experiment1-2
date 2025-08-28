from . import models
from .models import C, Subsession, Group, PlayerFirstPrice  # updated

class BidPage(Page):
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):
        return dict(
            valuation=self.player.valuation,
            opponent_bid=self.player.opponent_bid,
        )


class ResultsWaitPage(WaitPage):
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


