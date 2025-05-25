import json
import requests


def extract_data_from_api(api_key, tag_line, game_name):
    """
    Extracts data from the given API URL, api_key, tag_line, game_name, and returns ....
    
    Args:
        tag_line (str): tag line of the player.
        game_name (str): The name of the player.
        
    Returns:
        data (dict): The extracted data from the API in JSON format.
    """
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
        url = f"https://api.metatft.com/public/profile/lookup_by_riotid/VN2/{game_name}/{tag_line}source=full_profile&tft_set=TFTSet14&include_revival_matches=true"
        response = requests.get(url)
        data = response.json()
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)  # save json to debug
        return data, game_name, tag_line
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    
if __name__ == "__main__":
    tag_line = 'YBY1'
    game_name = 'TLN YBY1'
    api_key = "RGAPI-52d87177-b111-4c6e-99bf-35ba3e79325c"
    extract_data_from_api(api_key, tag_line, game_name)