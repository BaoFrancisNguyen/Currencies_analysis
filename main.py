import requests
import json
from api_config import API_KEY #API dans le fichier api_config.py

BASE_URL ='https://rest.coinapi.io/'

url = BASE_URL +'v1/assets' 
headers = {'X-CoinAPI-Key' : API_KEY}
response = requests.get(url, headers=headers) 


if response.status_code != 200: # test si la requête a réussi
    print(f"Error : {response.status_code}")
    exit()

data = json.loads(response.text) # convertir en dictionnaire

print()

nb_assents = len(data)

print(f"Nombre d'assets : {nb_assents}")
if nb_assents > 0:
    print("Liste des assets :")
    for asset in data[0:10]:
        print(f"{asset['asset_id']}: {asset['name']}")
       

print(" Coût de la requête: ", response.headers["x-ratelimit-request-cost"])
        
print(" Requêtes restantes: ", response.headers["x-ratelimit-remaining"])
