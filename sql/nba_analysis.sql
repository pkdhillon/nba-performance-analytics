-- NBA Player Performance Analysis
-- 2024-25 Season


-- 1. View the first 10 players in the dataset
-- No minimum-games filter because this query is only used
-- to inspect the cleaned database.

SELECT *
FROM players
LIMIT 10;


-- 2. Top 10 scorers among players who played at least 58 games

SELECT
    Player,
    Team,
    Position,
    Games,
    Points_Per_Game
FROM players
WHERE Games >= 58
ORDER BY Points_Per_Game DESC
LIMIT 10;


-- 3. Top 10 rebounders among players who played at least 58 games

SELECT
    Player,
    Team,
    Position,
    Games,
    Rebounds_Per_Game
FROM players
WHERE Games >= 58
ORDER BY Rebounds_Per_Game DESC
LIMIT 10;


-- 4. Top 10 assist leaders among players who played at least 58 games

SELECT
    Player,
    Team,
    Position,
    Games,
    Assists_Per_Game
FROM players
WHERE Games >= 58
ORDER BY Assists_Per_Game DESC
LIMIT 10;


-- 5. Average scoring by position among qualified players

SELECT
    Position,
    ROUND(AVG(Points_Per_Game), 2) AS Avg_Points_Per_Game
FROM players
WHERE Games >= 58
GROUP BY Position
ORDER BY Avg_Points_Per_Game DESC;


-- 6. High-scoring qualified players averaging at least 20 PPG

SELECT
    Player,
    Team,
    Position,
    Games,
    Points_Per_Game
FROM players
WHERE Games >= 58
  AND Points_Per_Game >= 20
ORDER BY Points_Per_Game DESC;


-- 7. Qualified players averaging at least 20 PPG and 5 assists

SELECT
    Player,
    Team,
    Games,
    Points_Per_Game,
    Assists_Per_Game
FROM players
WHERE Games >= 58
  AND Points_Per_Game >= 20
  AND Assists_Per_Game >= 5
ORDER BY Points_Per_Game DESC;


-- 8. Average player scoring by team
-- Exclude combined multi-team records such as 2TM and 3TM.
-- Only players who played at least 58 games are included.

SELECT
    Team,
    ROUND(AVG(Points_Per_Game), 2) AS Avg_Player_PPG
FROM players
WHERE Games >= 58
  AND Team NOT IN ('2TM', '3TM')
GROUP BY Team
ORDER BY Avg_Player_PPG DESC;