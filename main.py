from datetime import date, datetime, timedelta
from coinapi_service import coin_api_get_exchange_rates_extended
import json
from os import path # vérifier si un fichier existe

#date de début et date de fin
#récupérer les dates du jour et du jour - 100 jours
date_end = date.today()
date_end_str = date_end.strftime("%Y-%m-%d") # date du jour string
date_start_str_100 = (date_end - timedelta(days=100)).strftime("%Y-%m-%d") # date du jour - 100 jours

# 1 - 
#   date de début et date de fin
#   regarder si le fichier existe
#   récupérer la date de début et la date de fin / saved_data_date_start, saved_data_date_end
#   créer fonction load_json_data_from_file(filename), récupérer les données du fichier json qu'il faudra désérialiser
# 2 -comparer les dates avec celles du fichier json

# 3 - faire les appels à l'API avant / après
def load_json_data_from_file( filename):

    f = open(filename, "r") #lire le fichier json si il existe
    json_data = f.read()
    f.close()
    return json_data

assets = "BTC/EUR"
data_filename = assets.replace("/", "_") + "_" + ".json"

# créer un fichier json en écriture et sauvegarder les données json 
def save_json_data_to_file( filename, json_data):

    f = open(filename, "w")
    f.write(json_data)
    f.close()

# json.dumps() transforme un objet python en json / sérialisation
def get_json_rates(rates_data):

    rates_json = []
    for r in rates_data:
        rates_json.append({"date": r["time_period_start"][:10], "rate": r["rate_close"]})
    return json.dumps(rates_json) 

# si fichier json existe, comparer [date_start, date_end] avec [saved_data_date_start, saved_data_date_end]
# si fichier json n'existe pas, faire appel à l'API
save_data_date_start = None
save_data_date_end = None

if path.exists(data_filename):
    json_rates = load_json_data_from_file(data_filename)
    json_rates_data = json.loads(json_rates) # désérialisation
    if len(json_rates_data) > 0:
        save_data_date_start = json_rates_data[0]["date"]
        save_data_date_end = json_rates_data[-1]["date"]
        print("date start:", save_data_date_start)
        print("date end:", save_data_date_end)
else:
    print("fichier json non trouvé ou pas de data")


print("saved date start:", date_start_str_100) 
print("saved date end:", date_end_str)
print()

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

date_intervals = get_dates_intervals(date(2021, 1, 1), date(2021, 5, 27), 100)
# appel à l'API ("BTC/EUR", "AAAA-MM-JJ" ou date_start_str_100,"AAAA-MM-JJJ ou date_end_str)
rates = coin_api_get_exchange_rates_extended("BTC/EUR", date_intervals[0][0], date_intervals[0][1])

if rates:
    json = get_json_rates(rates)
    
    save_json_data_to_file( data_filename, json)
    print("BTC/EUR, nombre de cours:", len(rates))
    for r in rates:
        print(r["time_period_start"][:100], ":", r["rate_close"])
        
# .time_period_start    :     rate_close
# 2021-01-01 : 24032.11824302815
# 2021-01-02 : 24032.11824302815
# date du jour: date_today = date.today()
# date_tomorow = date_today +/- timedelta(days=1) soustraire ou additionner des jours
# difference: date_diff = date_tomorow - date_today
    # print(date_diff.days)

# date: date(2023, 1, 1)
# jour : %d, mois = %m, année = %Y
# date.strftime("%Y-%m-%d") date utilisée pour l'API
# date_france = date.strftime("%d/%m/%Y")

# date_start / date_end = date object
# interval_days = int

# [[date_start, date_end], [date_start, date_end], [date_start, date_end]]


#print(get_dates_intervals(date(2021, 1, 1), date(2021, 5, 27), 100))

