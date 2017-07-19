win_streak, lose_streak = [[]], [[]]

for game in games_stats.order_by('-game__game_date'):
    if game.won:
        win_streak[-1].append(game)
        lose_streak.append([])
    else:
        win_streak.append([])
        lose_streak[-1].append(game)
