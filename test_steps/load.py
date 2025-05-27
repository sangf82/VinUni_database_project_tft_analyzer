import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_to_sql(data):
    """
    Loads processed data into the new database schema (user and lp_history tables).
    
    Args:
        data (dict): Processed data containing User and LPHistory information
    """
    # Connect to the database using environment variables
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

    cursor = conn.cursor()

    # Get the data
    user_data = data['User']
    lp_history = data['LPHistory']

    # Insert or update user data
    cursor.execute("""
        INSERT INTO user (id, username, tag, tier, `rank`, lp, wins, losses, games_played, 
                         avg_placement, top4_rate, position, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            username=VALUES(username), 
            tag=VALUES(tag), 
            tier=VALUES(tier), 
            `rank`=VALUES(`rank`), 
            lp=VALUES(lp), 
            wins=VALUES(wins), 
            losses=VALUES(losses), 
            games_played=VALUES(games_played),
            avg_placement=VALUES(avg_placement),
            top4_rate=VALUES(top4_rate),
            position=VALUES(position),
            last_updated=VALUES(last_updated)
    """, (
        user_data['id'], user_data['username'], user_data['tag'], 
        user_data['tier'], user_data['rank'], user_data['lp'],
        user_data['wins'], user_data['losses'], user_data['games_played'],
        user_data['avg_placement'], user_data['top4_rate'], 
        user_data['position'], user_data['last_updated']
    ))

    # Insert LP history entries
    for lp_entry in lp_history:
        cursor.execute("""
            INSERT IGNORE INTO lp_history (user_id, lp, timestamp)
            VALUES (%s, %s, %s)
        """, (lp_entry['user_id'], lp_entry['lp'], lp_entry['timestamp']))

    print("Data loaded successfully into new schema.")
    
    # Commit all changes
    conn.commit()

    # Close connection
    cursor.close()
    conn.close()
    
def load_leaderboard_to_sql(leaderboard_entries):
    """
    Loads processed leaderboard data into the leaderboard_entry table.
    
    Args:
        leaderboard_entries (list): List of processed leaderboard entries
    """
    if not leaderboard_entries:
        print("No leaderboard entries to load")
        return
    
    # Connect to the database using environment variables
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

    cursor = conn.cursor()

    try:
        # Clear existing leaderboard data (since it's a snapshot)
        cursor.execute("DELETE FROM leaderboard_entry")
        print("Cleared existing leaderboard data")
        
        # Insert new leaderboard entries
        insert_query = """
            INSERT INTO leaderboard_entry 
            (username, leaderboard_region, tier, `rank`, lp, wins, losses, 
             games_played, avg_placement, top4_rate, position, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for entry in leaderboard_entries:
            cursor.execute(insert_query, (
                entry['player_name'],
                'VN2',  # Default region for Vietnam server
                entry['tier'],
                entry['rank'],
                entry['league_points'],
                entry['wins'],
                entry['losses'],
                entry['games_played'],
                entry['average_placement'],
                entry['win_rate'],
                entry['rank_position'],
                entry['last_updated']
            ))
        
        # Commit all changes
        conn.commit()
        print(f"Successfully loaded {len(leaderboard_entries)} leaderboard entries")
        
    except Exception as e:
        print(f"Error loading leaderboard data: {e}")
        conn.rollback()
        
    finally:
        # Close connection
        cursor.close()
        conn.close()

def load_match_companions_to_sql(companions):
    """
    Loads match companion data into the tft_match_companion table.
    
    Args:
        companions (list): List of companion entries with match IDs and player IDs
    """
    if not companions:
        print("No match companion data to load")
        return
    
    # Connect to the database using environment variables
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

    cursor = conn.cursor()

    try:
        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tft_match_companion (
            match_id VARCHAR(20),
            puuid VARCHAR(100),
            content_id VARCHAR(20),
            skin_id INT,
            placement INT,
            PRIMARY KEY (match_id, puuid)
        )
        """)
        
        # Insert match companions
        for companion in companions:
            cursor.execute("""
            INSERT INTO tft_match_companion 
            (match_id, puuid, content_id, skin_id, placement)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            content_id = VALUES(content_id),
            skin_id = VALUES(skin_id),
            placement = VALUES(placement)
            """, (
                companion['match_id'],
                companion['puuid'],
                companion['content_id'],
                companion['skin_id'],
                companion['placement']
            ))
        
        conn.commit()
        print(f"Successfully loaded {len(companions)} match companion entries")
        
    except Exception as e:
        print(f"Error loading match companion data: {e}")
        conn.rollback()
    
    finally:
        # Close connection
        cursor.close()
        conn.close()

def load_combined_data(user_data=None, leaderboard_data=None, companions_data=None):
    """
    Loads user data, leaderboard data, and match companion data in a single transaction.
    
    Args:
        user_data (dict): Individual player data for user/lp_history tables
        leaderboard_data (list): Leaderboard entries for leaderboard_entry table
        companions_data (list): Match companion data for tft_match_companion table
    """
    if user_data:
        load_to_sql(user_data)
        
    if leaderboard_data:
        load_leaderboard_to_sql(leaderboard_data)
        
    if companions_data:
        load_match_companions_to_sql(companions_data)

# if __name__ == "__main__":
#     sample_data = {
#         'Player': {
#             'puuid': 'player-1234',
#             'gameName': 'TestPlayer',
#             'tagLine': 'NA1',
#             'lastLP': 100,
#             'gamePlayed': 50
#         },

#         'Champion' : {'champ-1', 'champ-2'},

#         'Match' : [
#             {
#                 'MatchID': 'match-abc',
#                 'gameLength': 32.5,
#                 'endDatetime': '2024-05-10 13:45:00'
#             }
#         ],

#         'MatchPlayerInfo' : [
#             {
#                 'puuid': 'player-1234',
#                 'MatchID': 'match-abc',
#                 'placement': 1,
#                 'currentLP': 120
#             }
#         ],

#         'MatchPlayerChampionInfo' : [
#             {
#                 'puuid': 'player-1234',
#                 'MatchID': 'match-abc',
#                 'ChampionID': 'champ-1',
#                 'quantity': 2
#             },
#             {
#                 'puuid': 'player-1234',
#                 'MatchID': 'match-abc',
#                 'ChampionID': 'champ-2',
#                 'quantity': 1
#             }
#         ]
#     }
    
#     load_to_sql(sample_data)
