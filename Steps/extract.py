import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_data_from_api(tag_line, game_name):
    """
    Extracts data from the given API URL, tag_line, game_name, and returns ....
    
    Args:
        tag_line (str): tag line of the player.
        game_name (str): The name of the player.
        
    Returns:
        data (dict): The extracted data from the API in JSON format.
    """
    # Get API key from environment variables
    api_key = os.environ.get("RIOT_API_KEY")
    
    # try:
    #     headers = {
    #         "X-Riot-Token": api_key
    #     }
        
        
    #     api_url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    #     response = requests.get(api_url, headers=headers)
        
    #     response.raise_for_status()  # Raise an error for bad responses
        
    #     data = response.json()
    #     with open("account_info.json", "w") as f:
    #         json.dump(data, f, indent=4)  # save json to debug
    #     return data
    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching data from API: {e}")
    #     return None
    
    try:
        # Fixed the URL by adding a question mark before 'source'
        url = f"https://api.metatft.com/public/profile/lookup_by_riotid/VN2/{game_name}/{tag_line}?source=full_profile&tft_set=TFTSet14&include_revival_matches=true"
        response = requests.get(url)
        print(url)
        data = response.json()
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)  # save json to debug
        return data, game_name, tag_line
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def extract_leaderboard_data():
    """
    Extracts leaderboard data from Riot API for Challenger, Grandmaster, and Master tiers.
    
    Returns:
        dict: Combined leaderboard data containing all tiers with player information
    """
    api_key = os.environ.get("RIOT_API_KEY")
    
    if not api_key:
        print("Error: RIOT_API_KEY not found in environment variables")
        return None
    
    headers = {
        "X-Riot-Token": api_key
    }
    
    # TFT API endpoints for different tiers
    endpoints = {
        "challenger": "https://vn2.api.riotgames.com/tft/league/v1/challenger",
        "grandmaster": "https://vn2.api.riotgames.com/tft/league/v1/grandmaster", 
        "master": "https://vn2.api.riotgames.com/tft/league/v1/master"
    }
    
    leaderboard_data = {
        "challenger": [],
        "grandmaster": [],
        "master": [],
        "last_updated": None
    }
    
    try:
        for tier, endpoint in endpoints.items():
            print(f"Fetching {tier} leaderboard...")
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            
            tier_data = response.json()
            leaderboard_data[tier] = tier_data.get("entries", [])
            
            # Use the first successful response timestamp as last_updated
            if not leaderboard_data["last_updated"] and tier_data:
                leaderboard_data["last_updated"] = tier_data.get("timestamp")
        
        # Save leaderboard data for debugging
        with open("leaderboard_data.json", "w") as f:
            json.dump(leaderboard_data, f, indent=4)
        
        print(f"Successfully extracted leaderboard data:")
        print(f"- Challenger: {len(leaderboard_data['challenger'])} players")
        print(f"- Grandmaster: {len(leaderboard_data['grandmaster'])} players") 
        print(f"- Master: {len(leaderboard_data['master'])} players")
        
        return leaderboard_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching leaderboard data from Riot API: {e}")
        return None

def extract_player_details_from_summoner_id(summoner_id):
    """
    Gets detailed player information including riot ID from summoner ID.
    
    Args:
        summoner_id (str): The summoner ID
        
    Returns:
        dict: Player details including riot ID (game_name#tag_line)
    """
    api_key = os.environ.get("RIOT_API_KEY")
    
    if not api_key:
        return None
        
    headers = {
        "X-Riot-Token": api_key
    }
    
    try:
        # Get summoner details first
        summoner_url = f"https://vn2.api.riotgames.com/tft/summoner/v1/summoners/{summoner_id}"
        summoner_response = requests.get(summoner_url, headers=headers)
        summoner_response.raise_for_status()
        summoner_data = summoner_response.json()
        
        # Get account details using puuid
        puuid = summoner_data.get("puuid")
        if puuid:
            account_url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
            account_response = requests.get(account_url, headers=headers)
            account_response.raise_for_status()
            account_data = account_response.json()
            
            return {
                "summoner_id": summoner_id,
                "puuid": puuid,
                "game_name": account_data.get("gameName"),
                "tag_line": account_data.get("tagLine"),
                "summoner_level": summoner_data.get("summonerLevel"),
                "profile_icon_id": summoner_data.get("profileIconId")
            }
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player details for summoner {summoner_id}: {e}")
        
    return None

if __name__ == "__main__":
    tag_line = 'YBY1'
    game_name = 'TLN YBY1'
    api_key = 'RGAPI-f5cfc33d-d1b3-4457-a624-7e682bb1e8ad'
    extract_data_from_api(api_key, tag_line, game_name)