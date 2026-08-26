-- NBA Player Performance Analysis
-- 2024-25 Season


-- 1. View the first 10 players in the dataset
SELECT *
FROM players
LIMIT 10;


-- 2. Top 10 scorers
SELECT
    Player,
    Team,
    Position,
    Games,
    Points_Per_Game
FROM players
ORDER BY Points_Per_Game DESC
LIMIT 10;


-- 3. Top 10 rebounders
SELECT
    Player,
    Team,
    Position,
    Games,
    Rebounds_Per_Game
FROM players
ORDER BY Rebounds_Per_Game DESC
LIMIT 10;


-- 4. Top 10 assist leaders
SELECT
    Player,
    Team,
    Position,
    Games,
    Assists_Per_Game
FROM players
ORDER BY Assists_Per_Game DESC
LIMIT 10;


-- 5. Average scoring by position
SELECT
    Position,
    ROUND(AVG(Points_Per_Game), 2) AS Avg_Points_Per_Game
FROM players
GROUP BY Position
ORDER BY Avg_Points_Per_Game DESC;


-- 6. High-scoring players with at least 20 PPG
SELECT
    Player,
    Team,
    Position,
    Points_Per_Game
FROM players
WHERE Points_Per_Game >= 20
ORDER BY Points_Per_Game DESC;


-- 7. Players averaging at least 20 PPG and 5 assists
SELECT
    Player,
    Team,
    Points_Per_Game,
    Assists_Per_Game
FROM players
WHERE Points_Per_Game >= 20
  AND Assists_Per_Game >= 5
ORDER BY Points_Per_Game DESC;

-- 8. Average player scoring by team
-- Exclude combined multi-team records such as 2TM and 3TM
SELECT
    Team,
    ROUND(AVG(Points_Per_Game), 2) AS Avg_Player_PPG
FROM players
WHERE Team NOT LIKE '%TM'
GROUP BY Team
ORDER BY Avg_Player_PPG DESC;