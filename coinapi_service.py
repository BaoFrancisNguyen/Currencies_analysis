import requests
import json
from coinapi_config import API_KEY, BASE_URL
from datetime import date, datetime, timedelta

headers = {'X-CoinAPI-Key': API_KEY}


'''def coinapi_service_get_all_assets():
    url = BASE_URL + 'v1/assets'
    response = requests.get(url, headers=headers)

    # 200 / sinon afficher le code d'erreur
    if response.status_code == 200:
        print("L'appel à l'API a fonctionné")
        data = json.loads(response.text)
        nb_assets = len(data)
        # asset_id
        # name
        print("Nombre d'assets monétaires:", nb_assets)
        if nb_assets >= 10:
            for i in range(10):
                d = data[i]
                print(d["asset_id"] + ": " + d["name"])

        print()
        print("Quota restant:", response.headers["x-ratelimit-remaining"])
    else:
        # cas d'erreur
        print("L'appel à l'API a retourné une erreur:", response.status_code)
'''

def get_dates_intervals( date_start, date_end, interval_days):
    diff = date_end - date_start
    diff_days = diff.days
    dates_intervals = []
    interval_begin_date = date_start
    while diff_days > 0:
        nb_days_to_add = interval_days-1
        if diff_days < interval_days-1:
            nb_days_to_add = diff_days
        interval_end_date = interval_begin_date + timedelta(days=nb_days_to_add)
        dates_intervals.append([interval_begin_date, interval_end_date])
        diff_days -= nb_days_to_add+1
        interval_begin_date = interval_end_date + timedelta(days=1)

    return dates_intervals

# extended : start and end date can be separated by more than 100 days
# plusieurs appels à l'API par tranche de 100 jours et concaténation des données
# exemple : 1 janv 2023 -> 1 mai 2024 est au dessus de 100 jours, il y aura 2 appels à l'API puis concaténation des données
def coin_api_get_exchange_rates_extended(assets, start_date, end_date):

    rates = []
    dates_intervals = get_dates_intervals(start_date, end_date, 100)
   
    if len(dates_intervals) > 0: # si pas d'intervalle, on n'a rien à récupérer

        for i in dates_intervals: # boucle sur les intervalles de dates
            intervals_rates = coin_api_get_exchange_rates(assets, i[0], i[1]) # appel à l'API, i[0] = date début, i[1] = date fin
            rates += intervals_rates # concaténation des données
    
    return rates

   


def coin_api_get_exchange_rates(assets, start_date, end_date):
    # Bitcoin en euros
    # 1 jour
    # 1 janv 2021 -> 10 janv 2021
    # -> gestion erreurs
    # -> deserialiser
    # -> afficher tel quel
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = (end_date + timedelta(1)).strftime("%Y-%m-%d")

    url = BASE_URL + 'v1/exchangerate/' + assets + '/history?period_id=1DAY&time_start='+ start_date + 'T00:00:00&time_end=' + end_date + 'T00:00:00'
   
    response = requests.get(url, headers=headers)
    if response.status_code == 200: # status code 200 = OK
        print("L'appel à l'API a fonctionné")
        data = json.loads(response.text)
       
        #print("Quota restant:", response.headers["x-ratelimit-remaining"]) ne marche plus ??? ne le retrouve plus dans le output : headers
        return data
    else:
        print("L'appel à l'API a retourné une erreur:", response.status_code)
        return None
