import requests

# === CONFIG === #
AREA = "asia"
RIOTID = "TLNYBY1/YBY1"
API_TOKEN = "RGAPI-969f8a6a-e090-44f2-ba50-d7aa20d7f318"
REGION = "vn2"

url_1 = f"https://{AREA}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{RIOTID}?api_key={API_TOKEN}"

r1 = requests.get(url_1)
res_1 = r1.json()
id= res_1["puuid"]
print(id)

url_2 = f"https://{REGION}.api.riotgames.com/tft/league/v1/by-puuid/{id}?api_key={API_TOKEN}"

r2 = requests.get(url_2)
res_2 = r2.json()
print(res_2)


