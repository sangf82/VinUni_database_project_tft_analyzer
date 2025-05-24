import json
import requests
import re
import datetime

def process(data, game_name, tag_line, num_matches=5):
    """
    Processes the extracted data from the API and returns a dictionary containing formatted information 

    Args:
        data (dict): The extracted data from the API in JSON format.

    Returns:
        formatted_data (dict):
            
            Player (dict): dict containing player information:
                - puuid (str): The PUUID of the player.
                - gameName (str): The game name of the player.
                - tagLine (str): The tag line of the player.
                - lastLP (int): The last LP of the player.
                - gamePlayed (int): The number of games played by the player.
            
            Match (list): A list of dictionaries containing match information, each dictionary contains:
                - MatchID (str): The match ID.
                - gameLength (float): The duration of the match.
                - endDatetime (str): date time formnat of the match end time.
                
            MatchPlayerInfo (list): A list of dictionaries containing player information in each match, each dictionary contains:
                - puuid (str): The PUUID of the player.
                - MatchID (str): The match ID.
                - placement (int): The placement of the player in the match.
                - currentLP (int): The current LP of the player in the match.
                
            MatchPlayerChampionInfo (list): A list of dictionaries containing champion information for each player in each match, each dictionary contains:
                - puuid (str): The PUUID of the player.
                - MatchID (str): The match ID.
                - ChampionId (str): The ID of the champion used by the player.
                - quantity (int): The quantity of the champion used by the player.
            
            Champion (set): A set of champion IDs.
            
            
            
            
        
    """
    try:
        puuid = data['summoner']['puuid']
        gameName = game_name
        tagLine = tag_line
        lastLP = int(re.findall(r'\d+', data['ranked']['rating_text'])[0]) 
        gmaePlayed = int(data['ranked']['num_games'])
        
        PLayer = {
            'puuid': puuid,
            'gameName': gameName,
            'tagLine': tagLine,
            'lastLP': lastLP,
            'gamePlayed': gmaePlayed
            }
        
        Match = []
        MatchPlayerInfo = []
        MatchPlayerChampionInfo = []
        Champions = []
        
        for i,match in enumerate(data['matches'][:num_matches]):
            
            match_dict = {}
            matchplayer_dict = {}
            
            
            
            MatchID = match['riot_match_id']
            endDatetime = datetime.datetime.fromtimestamp(match['match_timestamp'] / 1000)
            try:
                metadata_match = requests.get(match['match_data_url']).json()
                gameLength = metadata_match['info']['game_length']
            except requests.exceptions.RequestException as e:
                print(f"Error fetching match meta data: {e}")     
                gameLength = None
            
            match_dict['MatchID'] = MatchID
            match_dict['gameLength'] = gameLength
            match_dict['endDatetime'] = endDatetime
           
            Match.append(match_dict)
            
            
            placement = match['placement']
            currentLP = int(re.findall(r'\d+',match['summary']['player_rating'])[0])
            
            matchplayer_dict['puuid'] = puuid
            matchplayer_dict['MatchID'] = MatchID
            matchplayer_dict['placement'] = placement
            matchplayer_dict['currentLP'] = currentLP
            
            MatchPlayerInfo.append(matchplayer_dict)
            
            champions = [champion['character_id'] for champion in match['summary']['units']]
            unique_champions = set(champions)
            champions_count = {champion: champions.count(champion) for champion in unique_champions}
            for champion in champions_count:
                
                matchplayerchampion_dict = {}
                matchplayerchampion_dict['puuid'] = puuid
                matchplayerchampion_dict['MatchID'] = MatchID
                matchplayerchampion_dict['ChampionId'] = champion
                matchplayerchampion_dict['quantity'] = champions_count[champion]
                MatchPlayerChampionInfo.append(matchplayerchampion_dict)
                Champions.append(champion)
                
        Champions = set(Champions)
         
        out = {'Player': PLayer,
                'Match': Match,
                'MatchPlayerInfo': MatchPlayerInfo,
                'MatchPlayerChampionInfo': MatchPlayerChampionInfo,
                'Champion': Champions}
        
        # save json out
        with open("processed_data.json", "w") as f:
            json.dump(out, f, indent=4)  # save json to debug
            
        return out
                
    except Exception as e:
        print(f"Error processing data: {e}")
        return None