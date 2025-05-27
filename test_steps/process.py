import json
import requests
import re
import datetime

def process(data, game_name, tag_line, num_matches=50):
    """
    Processes the extracted data from the API and returns a dictionary containing formatted information 
    for the new database schema.

    Args:
        data (dict): The extracted data from the API in JSON format.
        game_name (str): The game name of the player.
        tag_line (str): The tag line of the player.
        num_matches (int): Number of recent matches to process.

    Returns:
        formatted_data (dict):
            
            User (dict): dict containing user information for the 'user' table:
                - id (str): The PUUID of the player.
                - username (str): The game name of the player.
                - tag (str): The tag line of the player.
                - tier (str): The tier of the player.
                - rank (str): The rank of the player.
                - lp (int): The current LP of the player.
                - wins (int): Number of wins.
                - losses (int): Number of losses.
                - games_played (int): The number of games played by the player.
                - avg_placement (float): Average placement across matches.
                - top4_rate (float): Rate of top 4 finishes.
                - position (int): Leaderboard position.
                - last_updated (str): Timestamp of last update.
            
            LPHistory (list): A list of LP history entries for tracking LP changes over time.
        
    """
    try:
        # Extract basic player information
        puuid = data['summoner']['puuid']
        username = game_name
        tag = tag_line
        lp = int(re.findall(r'\d+', data['ranked']['rating_text'])[0])
        games_played = int(data['ranked']['num_games'])
        
        # Extract tier and rank information from rating_text
        rating_text = data['ranked']['rating_text']  # e.g., "CHALLENGER I 1942 LP"
        
        # Parse tier and rank from rating text
        rating_parts = rating_text.split()
        if len(rating_parts) >= 2:
            tier = rating_parts[0]  # e.g., "CHALLENGER", "GRANDMASTER", "MASTER", "DIAMOND", etc.
            rank = rating_parts[1]  # e.g., "I", "II", "III", "IV" (or empty for CHALLENGER/GRANDMASTER)
        else:
            tier = 'UNRANKED'
            rank = ''
        
        # Calculate statistics from recent matches
        placements = []
        wins = 0
        losses = 0
        lp_history = []
        
        for i, match in enumerate(data['matches'][:num_matches]):
            placement = match['placement']
            placements.append(placement)
            
            # Count wins (top 4) and losses (bottom 4)
            if placement <= 4:
                wins += 1
            else:
                losses += 1
            
            # Extract LP for history tracking
            match_lp = int(re.findall(r'\d+', match['summary']['player_rating'])[0])
            match_timestamp = datetime.datetime.fromtimestamp(match['match_timestamp'] / 1000)
            
            lp_history.append({
                'user_id': puuid,
                'lp': match_lp,
                'timestamp': match_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Calculate derived statistics
        avg_placement = sum(placements) / len(placements) if placements else 8.0
        top4_rate = (wins / len(placements)) if placements else 0.0
        
        # Position would typically come from leaderboard API, defaulting to 0 for now
        position = 0
        
        # Current timestamp for last_updated
        last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create user data structure for new schema
        user_data = {
            'id': puuid,
            'username': username,
            'tag': tag,
            'tier': tier,
            'rank': rank,
            'lp': lp,
            'wins': wins,
            'losses': losses,
            'games_played': games_played,
            'avg_placement': round(avg_placement, 2),
            'top4_rate': round(top4_rate, 2),
            'position': position,
            'last_updated': last_updated
        }
        
        # Prepare output for new schema
        output = {
            'User': user_data,
            'LPHistory': lp_history
        }
        
        # Save processed data for debugging
        with open("processed_data.json", "w") as f:
            json.dump(output, f, indent=4)
            
        return output
                
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def process_leaderboard_data(leaderboard_data, player_details_cache=None):
    """
    Processes the extracted leaderboard data and formats it for the leaderboard_entry table.
    
    Args:
        leaderboard_data (dict): Raw leaderboard data from Riot API containing challenger, grandmaster, master tiers
        player_details_cache (dict): Optional cache of player details to avoid redundant API calls
        
    Returns:
        list: List of formatted leaderboard entries ready for database insertion
    """
    if not leaderboard_data:
        print("No leaderboard data to process")
        return []
    
    processed_entries = []
    current_position = 1
    
    if player_details_cache is None:
        player_details_cache = {}
    
    try:
        # Process each tier in order: challenger -> grandmaster -> master
        for tier in ["challenger", "grandmaster", "master"]:
            tier_entries = leaderboard_data.get(tier, [])
            
            print(f"Processing {tier} tier: {len(tier_entries)} players")
            
            for entry in tier_entries:
                summoner_id = entry.get("summonerId")
                if not summoner_id:
                    continue
                
                # Get player details (riot ID) if not cached
                if summoner_id not in player_details_cache:
                    # This would require API call - for now use placeholder
                    player_details_cache[summoner_id] = {
                        "game_name": f"Player_{summoner_id[:8]}",
                        "tag_line": "NA1"
                    }
                
                player_details = player_details_cache[summoner_id]
                
                # Extract leaderboard information
                league_points = entry.get("leaguePoints", 0)
                wins = entry.get("wins", 0)
                losses = entry.get("losses", 0)
                games_played = wins + losses
                
                # Calculate win rate and average placement
                win_rate = round((wins / games_played), 2) if games_played > 0 else 0.0
                
                # For TFT, "wins" in leaderboard context usually means top 4 finishes
                # Average placement estimation based on win rate (this is an approximation)
                if win_rate >= 0.6:
                    avg_placement = 3.5
                elif win_rate >= 0.4:
                    avg_placement = 4.5
                elif win_rate >= 0.2:
                    avg_placement = 5.5
                else:
                    avg_placement = 6.5
                
                # Determine rank based on tier
                if tier.upper() == "CHALLENGER":
                    rank = "I"
                elif tier.upper() == "GRANDMASTER":
                    rank = "I"
                else:  # MASTER
                    rank = "I"
                
                # Current timestamp
                last_updated = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Create leaderboard entry
                leaderboard_entry = {
                    'player_name': player_details.get("game_name", "Unknown"),
                    'tagline': player_details.get("tag_line", "Unknown"),
                    'tier': tier.upper(),
                    'rank': rank,
                    'league_points': league_points,
                    'wins': wins,
                    'losses': losses,
                    'games_played': games_played,
                    'average_placement': avg_placement,
                    'win_rate': win_rate,
                    'rank_position': current_position,
                    'last_updated': last_updated
                }
                
                processed_entries.append(leaderboard_entry)
                current_position += 1
        
        print(f"Successfully processed {len(processed_entries)} leaderboard entries")
        
        # Save processed leaderboard data for debugging
        with open("processed_leaderboard_data.json", "w") as f:
            json.dump(processed_entries, f, indent=4)
        
        return processed_entries
        
    except Exception as e:
        print(f"Error processing leaderboard data: {e}")
        return []

def parse_rating_from_text(rating_text):
    """
    Parse tier, rank, and LP from rating text like "CHALLENGER I 1942 LP"
    
    Args:
        rating_text (str): Rating text to parse
        
    Returns:
        tuple: (tier, rank, lp)
    """
    try:
        parts = rating_text.split()
        if len(parts) >= 3:
            tier = parts[0]
            rank = parts[1] 
            lp = int(re.findall(r'\d+', ' '.join(parts[2:]))[0])
            return tier, rank, lp
    except:
        pass
    
    return "UNRANKED", "", 0