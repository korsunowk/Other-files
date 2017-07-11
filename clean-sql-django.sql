SELECT

  video_editor_team_tags.offensive_team_id as team_id,
  teams.name as team_name,

  video_editor_team_tags.game_period_id,
  video_editor_game_periods.short_name AS game_period_name,

  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id = 3
    THEN 1
    ELSE 0
  END) AS p3_made,
  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id IN (3, 19)
    THEN 1
    ELSE 0
  END) AS p3_attempts,

  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id IN (1, 2)
    THEN 1
    ELSE 0
  END) AS p2_made,
  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id IN (1, 2, 17, 18)
    THEN 1
    ELSE 0
  END) AS p2_attempts,

  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id = 4
    THEN 1
    ELSE 0
  END) AS ft_made,
  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id IN (4, 16)
    THEN 1
    ELSE 0
  END) AS ft_attempts,

  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id IN (1, 2, 3)
    THEN 1
    ELSE 0
  END) AS fg_made,
  SUM(CASE
    WHEN video_editor_individual_tags.action_result_id IN (1, 2, 3, 17, 18, 19)
    THEN 1
    ELSE 0
  END) AS fg_attempts

FROM video_editor_team_tags
INNER JOIN video_editor_individual_tags ON (video_editor_team_tags.id = video_editor_individual_tags.team_tag_id)
LEFT JOIN teams ON (teams.id = video_editor_team_tags.offensive_team_id)
INNER JOIN video_editor_game_periods ON (video_editor_team_tags.game_period_id = video_editor_game_periods.id)
WHERE video_editor_team_tags.game_id = {{ game }}
  AND video_editor_team_tags.deleted = 0
  AND video_editor_individual_tags.deleted = 0
  AND video_editor_team_tags.game_period_id IS NOT NULL
  AND video_editor_individual_tags.action_id IN (1, 2) /* Shot / FT */

GROUP BY video_editor_team_tags.offensive_team_id,
         video_editor_team_tags.game_period_id,
         video_editor_game_periods.short_name,
         team_name
ORDER BY video_editor_team_tags.game_period_id
