from app import db
from models import User, PlayerStats, MatchHistory, Champion, ChampionPick, LPHistory, LeaderboardEntry
from datetime import datetime, timedelta
import random
import logging

def initialize_sample_data():
    """Initialize the database with comprehensive sample TFT data"""
    try:
        # Clear existing data
        db.session.query(ChampionPick).delete()
        db.session.query(MatchHistory).delete()
        db.session.query(LPHistory).delete()
        db.session.query(PlayerStats).delete()
        db.session.query(LeaderboardEntry).delete()
        db.session.query(Champion).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create TFT Champions (Set 12 champions) - Fixed duplicates
        champions = [
            # 1-cost champions
            ('Ashe', 1), ('Blitzcrank', 1), ('Elise', 1), ('Jayce', 1), ('Jinx', 1),
            ('Kog\'Maw', 1), ('Lillia', 1), ('Maddie', 1), ('Powder', 1), ('Singed', 1),
            ('Trundle', 1), ('Violet', 1), ('Warwick', 1),
            
            # 2-cost champions  
            ('Akali', 2), ('Camille', 2), ('Darius', 2), ('Draven', 2), ('Gangplank', 2),
            ('Kassadin', 2), ('Leona', 2), ('Nocturne', 2), ('Rell', 2), ('Renata', 2),
            ('Sett', 2), ('Tristana', 2), ('Urgot', 2), ('Zeri', 2),
            
            # 3-cost champions
            ('Ambessa', 3), ('Cassiopeia', 3), ('Corki', 3), ('Ezreal', 3), ('Hecarim', 3),
            ('Heimerdinger', 3), ('Katarina', 3), ('Mordekaiser', 3), ('Nunu', 3), ('Renni', 3),
            ('Scar', 3), ('Swain', 3), ('Twisted Fate', 3), ('Vander', 3), ('Vladimir', 3),
            
            # 4-cost champions
            ('Caitlyn', 4), ('Dr. Mundo', 4), ('Ekko', 4), ('Gnar', 4), ('Irelia', 4),
            ('LeBlanc', 4), ('Loris', 4), ('Rumble', 4), ('Silco', 4),
            ('Twitch', 4), ('Vi', 4), ('Ziggs', 4),
            
            # 5-cost champions
            ('Mel', 5), ('Viktor', 5)
        ]
        
        for name, cost in champions:
            champion = Champion(
                name=name,
                cost=cost,
                health=random.randint(500, 2000),
                attack_damage=random.randint(50, 200),
                armor=random.randint(20, 80),
                magic_resist=random.randint(20, 80),
                image_url=f'https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/{name}.png'
            )
            db.session.add(champion)
        
        db.session.commit()
        logging.info(f"Created {len(champions)} champions")
        
        # Create registered users from top 30 VN players
        top_30_players = [
            ('tlnyby1', 'TLN YBY1', 'YBY1'),
            ('edgmaris', 'EDG Maris', 'Maris'),
            ('chunji', 'ChunJi', 'Chun'),
            ('stillness1090', 'Stillness', '1090'),
            ('hnzluckyboiz', 'HnZ Luckyboiz', '1092'),
            ('gdroyal1704', 'GD Royal', '1704'),
            ('beevtt', 'BEE vtt', 'VTT'),
            ('a3cv01', 'A3Cv01', '1803'),
            ('gdfeed1681', 'GDFEED', '1681'),
            ('ea7gnut', 'EA7 Gnut', '2004'),
            ('bdgdovis', 'BDG Dovis', 'Doong'),
            ('swllaih', 'SW Llaih', 'Fam'),
            ('ea7longbentre', 'EA7 longbentre', '6030'),
            ('tlnmidfeed', 'TLN MidFeed', '1010'),
            ('trikhanh1810', 'TriKhanh1810', 'AVXX'),
            ('bdghuyee', 'BDG Huyee', '1959'),
            ('yugii0707', 'Yugii', '0707'),
            ('hani1401', 'H A N I', '1401'),
            ('vpncci', 'VP NCCI', '310'),
            ('vici309', 'Vici', '309'),
            ('furyhom', 'Furyhom', 'Zxy'),
            ('hnzkhocmanh20', 'HnZ khocmanh20', '2011'),
            ('kinne3636', 'Kinne', '3636'),
            ('quysotvn', 'Quý Sớt', '2611'),
            ('vpmilo', 'VP Milo', 'EA7'),
            ('cutehehe', 'Cute hehe', '2442'),
            ('Player1', 'TestUser', 'TAG1'),
            ('Player2', 'SampleGamer', 'TAG2'),
            ('Player3', 'TFTMaster', 'TAG3'),
            ('DemoUser', 'DemoPlayer', 'DEMO')
        ]
        
        sample_users = top_30_players
        
        for username, riot_name, riot_tag in sample_users:
            user = User(username=username, riot_name=riot_name, riot_tag=riot_tag)
            user.set_password('password123')
            db.session.add(user)
        
        db.session.commit()
        logging.info(f"Created {len(sample_users)} users")
        
        # Create leaderboard entries for top 50 players (based on actual VN data)
        vn_players = [
            ('TLN YBY1', 'YBY1', 'CHALLENGER', '', 1942),
            ('EDG Maris', 'Maris', 'CHALLENGER', '', 1773),
            ('ChunJi', 'Chun', 'CHALLENGER', '', 1765),
            ('Stillness', '1090', 'CHALLENGER', '', 1733),
            ('HnZ Luckyboiz', '1092', 'CHALLENGER', '', 1725),
            ('GD Royal', '1704', 'CHALLENGER', '', 1692),
            ('BEE vtt', 'VTT', 'CHALLENGER', '', 1648),
            ('A3Cv01', '1803', 'CHALLENGER', '', 1597),
            ('GDFEED', '1681', 'CHALLENGER', '', 1575),
            ('EA7 Gnut', '2004', 'CHALLENGER', '', 1555),
            ('BDG Dovis', 'Doong', 'CHALLENGER', '', 1551),
            ('SW Llaih', 'Fam', 'CHALLENGER', '', 1545),
            ('EA7 longbentre', '6030', 'CHALLENGER', '', 1532),
            ('TLN MidFeed', '1010', 'CHALLENGER', '', 1532),
            ('TriKhanh1810', 'AVXX', 'CHALLENGER', '', 1501),
            ('BDG Huyee', '1959', 'CHALLENGER', '', 1498),
            ('Yugii', '0707', 'CHALLENGER', '', 1490),
            ('H A N I', '1401', 'CHALLENGER', '', 1470),
            ('VP NCCI', '310', 'CHALLENGER', '', 1469),
            ('Vici', '309', 'CHALLENGER', '', 1458),
            ('Furyhom', 'Zxy', 'CHALLENGER', '', 1456),
            ('HnZ khocmanh20', '2011', 'CHALLENGER', '', 1435),
            ('Kinne', '3636', 'CHALLENGER', '', 1432),
            ('Quý Sớt', '2611', 'CHALLENGER', '', 1430),
            ('VP Milo', 'EA7', 'CHALLENGER', '', 1427),
            ('Cute hehe', '2442', 'CHALLENGER', '', 1419)
        ]
        
        # Add more players for full leaderboard
        tiers = ['GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD']
        ranks = ['I', 'II', 'III', 'IV']
        
        rank_position = len(vn_players) + 1
        
        for i in range(25, 51):  # Add players 25-50
            tier = random.choice(tiers)
            rank = random.choice(ranks) if tier not in ['GRANDMASTER', 'MASTER'] else ''
            lp = random.randint(800, 1400) if tier in ['GRANDMASTER', 'MASTER'] else random.randint(0, 100)
            
            player = LeaderboardEntry(
                player_name=f'Player{i}',
                tagline=f'TAG{i}',
                tier=tier,
                rank=rank,
                league_points=lp,
                wins=random.randint(80, 200),
                losses=random.randint(50, 150),
                games_played=random.randint(200, 500),
                average_placement=round(random.uniform(3.0, 5.5), 1),
                win_rate=round(random.uniform(40.0, 75.0), 1),
                rank_position=rank_position
            )
            vn_players.append((player.player_name, player.tagline, player.tier, player.rank, player.league_points))
            rank_position += 1
        
        # Create leaderboard entries
        for i, (name, tagline, tier, rank, lp) in enumerate(vn_players, 1):
            wins = random.randint(100, 300)
            losses = random.randint(80, 200)
            games = wins + losses
            
            leaderboard_entry = LeaderboardEntry(
                player_name=name,
                tagline=tagline,
                tier=tier,
                rank=rank,
                league_points=lp,
                wins=wins,
                losses=losses,
                games_played=games,
                average_placement=round(random.uniform(3.0, 4.8), 1),
                win_rate=round((wins / games) * 100, 1),
                rank_position=i
            )
            db.session.add(leaderboard_entry)
        
        db.session.commit()
        logging.info(f"Created {len(vn_players)} leaderboard entries")
        
        # Create player stats and match history for registered users
        users = User.query.all()
        all_champions = Champion.query.all()
        
        # Realistic LP values for top 30 players based on actual leaderboard
        top_player_lp = [1942, 1773, 1765, 1733, 1725, 1692, 1648, 1597, 1575, 1555, 
                        1551, 1545, 1532, 1532, 1501, 1498, 1490, 1470, 1469, 1458,
                        1456, 1435, 1432, 1430, 1427, 1419, 1200, 1150, 1100, 1050]
        
        for i, user in enumerate(users):
            # Create realistic player stats based on rank position
            if i < len(top_player_lp):
                # Top 30 players - all Challenger/Master tier
                lp = top_player_lp[i]
                if lp >= 1400:
                    tier = 'CHALLENGER'
                    rank = ''
                else:
                    tier = 'MASTER'
                    rank = ''
            else:
                # Other players
                tier_choices = ['MASTER', 'DIAMOND', 'PLATINUM']
                tier = random.choice(tier_choices)
                rank = random.choice(['I', 'II', 'III', 'IV']) if tier not in ['MASTER', 'CHALLENGER'] else ''
                lp = random.randint(800, 1300) if tier == 'MASTER' else random.randint(0, 100)
            
            # Enhanced stats for top players
            if i < 26:  # Top 26 players get higher quality stats
                wins = random.randint(200, 400)
                losses = random.randint(100, 250)
                games = wins + losses
                top_four_rate = round(random.uniform(60.0, 80.0), 1)
                avg_placement = round(random.uniform(3.0, 4.2), 1)
            else:
                wins = random.randint(100, 200)
                losses = random.randint(80, 150)
                games = wins + losses
                top_four_rate = round(random.uniform(45.0, 65.0), 1)
                avg_placement = round(random.uniform(3.5, 4.8), 1)
            
            stats = PlayerStats(
                user_id=user.id,
                tier=tier,
                rank=rank,
                league_points=lp,
                wins=wins,
                losses=losses,
                games_played=games,
                average_placement=avg_placement,
                top_four_rate=top_four_rate
            )
            db.session.add(stats)
            
            # Create extensive match history (100 matches for top players, 50 for others)
            num_matches = 100 if i < 26 else 50
            base_lp = max(100, lp - random.randint(200, 500))  # Start lower for progression
            match_date = datetime.utcnow() - timedelta(days=60 if i < 26 else 30)
            
            for match_num in range(num_matches):
                # Better placement distribution for top players
                if i < 26:  # Top players have better average placements
                    placement_weights = [15, 20, 20, 25, 10, 5, 3, 2]  # Weighted towards top 4
                else:
                    placement_weights = [8, 12, 15, 20, 18, 12, 8, 7]  # More balanced
                
                placement = random.choices(range(1, 9), weights=placement_weights)[0]
                
                # Enhanced LP change calculation based on current tier and placement
                base_lp_gain = 30 if tier == 'CHALLENGER' else 35
                
                if placement == 1:
                    lp_change = random.randint(base_lp_gain, base_lp_gain + 20)
                elif placement == 2:
                    lp_change = random.randint(15, base_lp_gain - 5)
                elif placement == 3:
                    lp_change = random.randint(5, 20)
                elif placement == 4:
                    lp_change = random.randint(-5, 10)
                elif placement == 5:
                    lp_change = random.randint(-15, -5)
                elif placement == 6:
                    lp_change = random.randint(-25, -10)
                elif placement == 7:
                    lp_change = random.randint(-35, -20)
                else:  # 8th place
                    lp_change = random.randint(-45, -30)
                
                base_lp += lp_change
                base_lp = max(0, base_lp)  # LP can't go below 0
                
                match = MatchHistory(
                    user_id=user.id,
                    match_id=f'VN1_{user.id}_{match_num}',
                    placement=placement,
                    lp_change=lp_change,
                    lp_after=base_lp,
                    game_length=random.randint(1800, 3600),  # 30-60 minutes
                    game_version='14.1',
                    played_at=match_date + timedelta(hours=random.randint(1, 23), minutes=random.randint(0, 59))
                )
                db.session.add(match)
                db.session.flush()  # Get the match ID
                
                # Enhanced champion picks with realistic compositions
                if placement <= 4:  # Top 4 gets better comps
                    num_champions = random.randint(5, 8)  # More complete boards
                    star_level_weights = [30, 50, 20]  # More 2-stars for top players
                else:
                    num_champions = random.randint(3, 6)
                    star_level_weights = [60, 35, 5]  # Mostly 1-stars for bottom placements
                
                picked_champions = random.sample(all_champions, num_champions)
                
                # Realistic TFT item combinations
                item_combinations = [
                    '["Infinity Edge", "Last Whisper", "Bloodthirster"]',
                    '["Rabadon\'s Deathcap", "Archangel\'s Staff", "Blue Buff"]',
                    '["Gargoyle Stoneplate", "Warmog\'s Armor", "Dragon\'s Claw"]',
                    '["Guinsoo\'s Rageblade", "Titan\'s Resolve", "Runaan\'s Hurricane"]',
                    '["Morellonomicon", "Ionic Spark", "Hand of Justice"]',
                    '["Spear of Shojin", "Edge of Night", "Quicksilver"]',
                    '["Sterak\'s Gage", "Redemption", "Locket of the Iron Solari"]',
                    '["Hextech Gunblade", "Giant Slayer", "Zephyr"]'
                ]
                
                for champion in picked_champions:
                    star_level = random.choices([1, 2, 3], weights=star_level_weights)[0]
                    items = random.choice(item_combinations)
                    
                    pick = ChampionPick(
                        match_id=match.id,
                        champion_id=champion.id,
                        star_level=star_level,
                        items=items
                    )
                    db.session.add(pick)
                
                # Add LP history entry
                lp_history = LPHistory(
                    user_id=user.id,
                    lp_value=base_lp,
                    tier=tier,
                    rank=rank,
                    recorded_at=match.played_at
                )
                db.session.add(lp_history)
                
                match_date += timedelta(hours=random.randint(1, 4))  # More frequent matches for realistic progression
            
            # Update final stats
            stats.calculate_stats_from_matches()
        
        db.session.commit()
        logging.info(f"Created comprehensive match history and stats for {len(users)} users")
        
        logging.info("Sample data initialization completed successfully!")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error initializing sample data: {e}")
        raise

if __name__ == '__main__':
    from app import app
    with app.app_context():
        initialize_sample_data()

