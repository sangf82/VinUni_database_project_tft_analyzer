-- TFT Analyzer Database Schema
-- Vietnam Server (VN2) Configuration

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS tft_analyzer;
USE tft_analyzer;

-- ===================================
-- MAIN TABLES
-- ===================================

-- User table: Player profiles and current rankings
CREATE TABLE IF NOT EXISTS user (
    id VARCHAR(100) PRIMARY KEY,           -- Player PUUID
    username VARCHAR(50) NOT NULL,         -- In-game name
    tag VARCHAR(10) NOT NULL,              -- Tag line (e.g., VN2)
    tier VARCHAR(20) DEFAULT 'UNRANKED',   -- CHALLENGER, GRANDMASTER, MASTER, etc.
    `rank` VARCHAR(5) DEFAULT '',          -- I, II, III, IV (empty for CHALLENGER/GRANDMASTER)
    lp INT DEFAULT 0,                      -- League Points
    wins INT DEFAULT 0,                    -- Total wins (top 4 finishes)
    losses INT DEFAULT 0,                  -- Total losses (bottom 4 finishes)
    games_played INT DEFAULT 0,            -- Total games
    avg_placement DECIMAL(4,2) DEFAULT 0.00, -- Average placement (1.00-8.00)
    top4_rate DECIMAL(5,2) DEFAULT 0.00,   -- Win rate percentage (0.00-100.00)
    position INT DEFAULT 0,                -- Leaderboard position (0 if not ranked)
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_lp (lp DESC),
    INDEX idx_tier (tier),
    INDEX idx_position (position),
    INDEX idx_last_updated (last_updated)
);

-- LP History table: Track LP changes over time
CREATE TABLE IF NOT EXISTS lp_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,         -- References user.id
    lp INT NOT NULL,                       -- LP at this point in time
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    INDEX idx_user_timestamp (user_id, timestamp),
    INDEX idx_timestamp (timestamp)
);

-- Leaderboard Entry table: Daily snapshots of top players
CREATE TABLE IF NOT EXISTS leaderboard_entry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    leaderboard_region VARCHAR(10) DEFAULT 'VN2',
    tier VARCHAR(20) NOT NULL,             -- CHALLENGER, GRANDMASTER, MASTER
    `rank` VARCHAR(5) DEFAULT '',
    lp INT NOT NULL,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    games_played INT DEFAULT 0,
    avg_placement DECIMAL(4,2) DEFAULT 0.00,
    top4_rate DECIMAL(5,2) DEFAULT 0.00,
    position INT DEFAULT 0,                -- Rank position (1 = #1 player)
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_position (position),
    INDEX idx_lp (lp DESC),
    INDEX idx_tier_rank (tier, `rank`),
    INDEX idx_last_updated (last_updated)
);

-- TFT Match Companion table: Little Legend data
CREATE TABLE IF NOT EXISTS tft_match_companion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id VARCHAR(20) NOT NULL,         -- Riot match ID
    puuid VARCHAR(100) NOT NULL,           -- Player PUUID
    content_id VARCHAR(20),                -- Little Legend content ID
    skin_id INT,                           -- Skin variant ID
    placement INT,                         -- Player's placement in match (1-8)
    match_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_match_player (match_id, puuid),
    INDEX idx_match_id (match_id),
    INDEX idx_puuid (puuid),
    INDEX idx_content_id (content_id),
    INDEX idx_placement (placement)
);

-- ===================================
-- VIEWS FOR FRONTEND DEVELOPERS
-- ===================================

-- Current Leaderboard View: Easy access to current top players
CREATE OR REPLACE VIEW v_current_leaderboard AS
SELECT 
    position,
    username,
    tier,
    `rank`,
    lp,
    wins,
    losses,
    games_played,
    ROUND(top4_rate, 2) as win_rate_percent,
    ROUND(avg_placement, 2) as avg_placement,
    last_updated
FROM leaderboard_entry 
WHERE position > 0
ORDER BY position ASC;

-- Player Profile View: Complete player information
CREATE OR REPLACE VIEW v_player_profiles AS
SELECT 
    u.id as player_id,
    u.username,
    u.tag,
    u.tier,
    u.`rank`,
    u.lp,
    u.wins,
    u.losses,
    u.games_played,
    ROUND(u.top4_rate, 2) as win_rate_percent,
    ROUND(u.avg_placement, 2) as avg_placement,
    u.position as leaderboard_position,
    u.last_updated,
    -- LP trend (change from previous entry)
    (SELECT (u.lp - lh.lp) 
     FROM lp_history lh 
     WHERE lh.user_id = u.id 
     ORDER BY lh.timestamp DESC 
     LIMIT 1 OFFSET 1) as lp_change
FROM user u;

-- Match History View: Player's recent match performance
CREATE OR REPLACE VIEW v_match_history AS
SELECT 
    c.match_id,
    u.username,
    u.tag,
    c.placement,
    c.content_id as little_legend_id,
    c.skin_id as little_legend_skin,
    c.match_timestamp,
    CASE 
        WHEN c.placement <= 4 THEN 'WIN' 
        ELSE 'LOSS' 
    END as result
FROM tft_match_companion c
JOIN user u ON c.puuid = u.id
ORDER BY c.match_timestamp DESC;

-- LP History View: Track LP changes over time
CREATE OR REPLACE VIEW v_lp_trends AS
SELECT 
    u.username,
    u.tag,
    lh.lp,
    lh.timestamp,
    LAG(lh.lp) OVER (PARTITION BY u.id ORDER BY lh.timestamp) as previous_lp,
    (lh.lp - LAG(lh.lp) OVER (PARTITION BY u.id ORDER BY lh.timestamp)) as lp_change
FROM lp_history lh
JOIN user u ON lh.user_id = u.id
ORDER BY u.username, lh.timestamp DESC;

-- Top Little Legends View: Most popular companions
CREATE OR REPLACE VIEW v_popular_little_legends AS
SELECT 
    content_id,
    skin_id,
    COUNT(*) as usage_count,
    COUNT(CASE WHEN placement <= 4 THEN 1 END) as wins,
    ROUND(
        (COUNT(CASE WHEN placement <= 4 THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as win_rate_percent,
    ROUND(AVG(placement), 2) as avg_placement
FROM tft_match_companion
WHERE content_id IS NOT NULL
GROUP BY content_id, skin_id
HAVING usage_count >= 5  -- Only show legends used 5+ times
ORDER BY usage_count DESC, win_rate_percent DESC;

-- ===================================
-- SAMPLE QUERIES FOR FRONTEND DEVELOPERS
-- ===================================

/*
-- Get current leaderboard (top 50 players)
SELECT * FROM v_current_leaderboard LIMIT 50;

-- Get specific player profile
SELECT * FROM v_player_profiles WHERE username = 'PlayerName';

-- Get player's recent matches
SELECT * FROM v_match_history 
WHERE username = 'PlayerName' 
ORDER BY match_timestamp DESC 
LIMIT 20;

-- Get player's LP trend over last 30 days
SELECT * FROM v_lp_trends 
WHERE username = 'PlayerName' 
AND timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY timestamp DESC;

-- Get most popular Little Legends
SELECT * FROM v_popular_little_legends LIMIT 10;

-- Search players by name (partial match)
SELECT username, tag, tier, lp, position 
FROM v_player_profiles 
WHERE username LIKE '%search_term%' 
ORDER BY lp DESC;
*/
