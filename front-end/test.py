import requests

url_1 = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/TLNYBY1/YBY1?api_key=RGAPI-969f8a6a-e090-44f2-ba50-d7aa20d7f318"

r_1 = requests.get(url_1)
print(r_1.status_code)
print(r_1.json())