SELECT

  players.id,
  players.first_name,
  players.last_name,

  AVG(players_stats.df_rebounds) AS df_rebounds,
  AVG(players_stats.fouls_received) AS fouls_received,
  AVG(players_stats.points) AS points,
  AVG(players_stats.turnovers) AS turnovers,
  AVG(players_stats.block_shots) AS block_shots,
  AVG(players_stats.assists) AS assists,
  AVG(players_stats.p3_attempts) AS p3_attempts,
  AVG(players_stats.shots_rejected) AS shots_rejected,
  AVG(players_stats.ft_made) AS ft_made,
  AVG(players_stats.ft_attempts) AS ft_attempts,
  AVG(players_stats.fouls_made) AS fouls_made,
  AVG(players_stats.steals) AS steals,
  AVG(players_stats.p2_made) AS p2_made,
  AVG(players_stats.p3_made) AS p3_made,
  AVG(players_stats.fg_made) AS fg_made,
  AVG(players_stats.of_rebounds) AS of_rebounds,
  AVG(players_stats.fg_attempts) AS fg_attempts,
  AVG(players_stats.p2_attempts) AS p2_attempts,

  AVG(ft_made / NULLIF(ft_attempts, 0) * 100) as ft_percent,
  AVG(fg_made / NULLIF(fg_attempts, 0) * 100) as fg_percent,

  AVG(p2_made / NULLIF(p2_attempts, 0) * 100) as p2_percent,
  AVG(p3_made / NULLIF(p3_attempts, 0) * 100) as p3_percent,

  (((((((((AVG(players_stats.points) + AVG(players_stats.assists) * 1.5 + AVG(players_stats.steals))
  + AVG(players_stats.block_shots) * 0.75) + AVG(players_stats.of_rebounds) * 1.25)
  + AVG(players_stats.df_rebounds) * 0.75) + AVG(players_stats.p3_made) / 2)
  + AVG(players_stats.fouls_received) / 2) - AVG(players_stats.fouls_made) / 2)
  - (AVG(players_stats.fg_attempts) - AVG(players_stats.fg_made))
  * 0.75 - AVG(players_stats.turnovers)) - (AVG(players_stats.ft_attempts)
  - AVG(players_stats.ft_made)) / 2) / ((SUM(date_part('minutes', players_stats.minutes)) * 60 + SUM(date_part('seconds',
  players_stats.minutes))) / COUNT(*) / 60) AS VIR,

  CASE WHEN AVG(players_stats.fg_attempts)
  = 0 THEN 0 ELSE AVG(players_stats.points) / (AVG(players_stats.fg_attempts)
  + AVG(players_stats.ft_attempts) / 2 + AVG(players_stats.turnovers)) END AS OER,

  ((AVG(players_stats.points) + AVG(players_stats.fouls_received)
  + AVG(players_stats.of_rebounds) + AVG(players_stats.df_rebounds)
  + AVG(players_stats.block_shots) + AVG(players_stats.steals) + AVG(players_stats.assists)
  - AVG(players_stats.fouls_made) - AVG(players_stats.turnovers)
  - AVG(players_stats.shots_rejected)) - (AVG(players_stats.fg_attempts)
  - AVG(players_stats.fg_made))) - (AVG(players_stats.ft_attempts)
  - AVG(players_stats.ft_made)) AS VAL

FROM players_stats
INNER JOIN games ON (players_stats.game_id = games.id)
inner join players players on (players_stats.player_id = players.id)

WHERE games.season_id = {{ season }}
  AND games.league_id = {{ league }}

GROUP BY players.id, players.first_name, players.last_name
