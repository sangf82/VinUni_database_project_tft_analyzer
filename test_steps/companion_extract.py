#!/usr/bin/env python3
"""
Module for extending the existing extract.py to include matdef extract_player_companions(puuid, region="vn2", match_count=5):h companion data extraction.
This will add the ability to extract Little Legend (Pet) data from match details.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_match_companions(match_id, region="vn2"):
    """
    Extract companion (Little Legend/Pet) information from a specific match.
    
    Args:
        match_id (str): Match ID to retrieve
        region (str): Region/platform ID (e.g., "vn2", "kr", "jp1")
        
    Returns:
        list: List of player-companion mappings
    """
    try:
        api_key = os.environ.get("RIOT_API_KEY")
        if not api_key:
            print("Missing RIOT_API_KEY in environment variables")
            return []
            
        url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        
        match_data = response.json()
        companions = []
        
        # Extract companion data for each participant
        for participant in match_data.get('info', {}).get('participants', []):
            companion_data = participant.get('companion', {})
            if companion_data:
                companions.append({
                    'match_id': match_id,
                    'puuid': participant.get('puuid'),
                    'content_id': companion_data.get('content_ID'),
                    'skin_id': companion_data.get('skin_ID'),
                    'placement': participant.get('placement')
                })
        
        return companions
        
    except Exception as e:
        print(f"Error extracting match companion data: {e}")
        return []

def extract_player_match_history(puuid, region="vn2", count=20):
    """
    Extract a player's recent match history.
    
    Args:
        puuid (str): Player's PUUID
        region (str): Region code (e.g., "vn2", "kr", "jp1")
        count (int): Number of matches to retrieve
        
    Returns:
        list: List of match IDs
    """
    try:
        api_key = os.environ.get("RIOT_API_KEY")
        if not api_key:
            print("Missing RIOT_API_KEY in environment variables")
            return []
            
        # Determine the correct regional routing value
        regional_routing = "asia"  # Default to asia for Vietnam server (vn2)
        
        url = f"https://{regional_routing}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}&api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        print(f"Error extracting player match history: {e}")
        return []

def extract_player_companions(puuid, region="vn2", match_count=50):
    """
    Extract all companion data for a player's recent matches.
    
    Args:
        puuid (str): Player's PUUID
        region (str): Region code (e.g., "vn2", "kr", "jp1")
        match_count (int): Number of matches to analyze
        
    Returns:
        dict: Dictionary of match_id -> companion data
    """
    # Get player's recent matches
    match_ids = extract_player_match_history(puuid, region, match_count)
    
    if not match_ids:
        print(f"No matches found for player {puuid}")
        return {}
    
    # Extract companion data for each match
    companion_data = {}
    for match_id in match_ids:
        companions = extract_match_companions(match_id, region)
        if companions:
            # Find this player's companion in this match
            for companion in companions:
                if companion['puuid'] == puuid:
                    companion_data[match_id] = companion
                    break
    
    return companion_data

def enrich_match_data_with_companions(match_data):
    """
    Enrich existing match data with companion information.
    
    Args:
        match_data (dict): Existing match data structure
        
    Returns:
        dict: Enriched match data with companion information
    """
    # This is a placeholder for how you might integrate this with your existing ETL
    # You would need to adapt this to your specific data structures
    
    if 'info' in match_data and 'participants' in match_data['info']:
        for participant in match_data['info']['participants']:
            if 'companion' in participant:
                puuid = participant.get('puuid')
                content_id = participant['companion'].get('content_ID')
                skin_id = participant['companion'].get('skin_ID')
                
                # You could look up the tactician name/image from your database here
                # and add it to the match data
                
                participant['companion_details'] = {
                    'content_id': content_id,
                    'skin_id': skin_id
                    # Add more details as needed
                }
    
    return match_data

# Example usage if this module is run directly
if __name__ == "__main__":
    # You would need a valid PUUID and region to test this
    test_puuid = "YOUR_TEST_PUUID"
    test_region = "vn2"
    
    print(f"Extracting companion data for player {test_puuid} in region {test_region}...")
    companion_data = extract_player_companions(test_puuid, test_region)
    
    if companion_data:
        print(f"Found companion data in {len(companion_data)} matches:")
        for match_id, companion in companion_data.items():
            print(f"Match {match_id}: Companion Content ID {companion['content_id']}, Skin ID {companion['skin_id']}")
    else:
        print("No companion data found.")
