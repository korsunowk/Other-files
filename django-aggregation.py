from django.db.models import Count, Case, When, Sum


@staticmethod
def aggregate_game_stats(game_stats):
    """
    Help method for aggregation game stats
    :param game_stats: GameStats table
    :return: dictionary with stats from GameStats table
    """
    return game_stats.aggregate(
        gp=Count('game_id'),
        won_count=Count(Case(When(won=True, then=1))),
        loss_count=Count(Case(When(won=False, then=1))),
        fg_attempts=Sum('fg_attempts'),
        ft_attempts=Sum('ft_attempts'),
        of_rebounds=Sum('of_rebounds'),
        pts=Sum('points'),
        turnovers=Sum('turnovers')
    )
