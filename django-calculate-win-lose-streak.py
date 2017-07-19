win_streak, lose_streak = [[]], [[]]

for game in games_stats.order_by('-game__game_date'):
    if game.won:
        win_streak[-1].append(game)
        lose_streak.append([])
    else:
        win_streak.append([])
        lose_streak[-1].append(game)

# get array with streak with max len
win_streak = max(win_streak, key=lambda x: len(x))
lose_streak = max(lose_streak, key=lambda x: len(x))
