#import faster_than_requests as requests
from datetime import datetime, timedelta
import json
import requests


def return_stations():
    with open('./tidestations.json') as f:
        data = json.load(f)
        return data


def get_high_low_prediction(station_id, time_series=None, start_date=None, end_date=None):
    high_low_list = []
    if start_date and end_date:
        r = requests.get(f'https://api-iwls.dfo-mpo.gc.ca/api/v1/stations/{station_id}/data?time-series-code=wlp-hilo&from={start_date}&to={end_date}')
    else:
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        tomorrow_plus_7_hours = now + timedelta(days=1.25)
        r = requests.get(f'https://api-iwls.dfo-mpo.gc.ca/api/v1/stations/{station_id}/data?time-series-code=wlp-hilo&from={now.strftime("%Y-%m-%dT%H:%M:%SZ")}&to={tomorrow.strftime("%Y-%m-%dT%H:%M:%SZ")}')
        if len(r.json()) is 3:
            r = requests.get(f'https://api-iwls.dfo-mpo.gc.ca/api/v1/stations/{station_id}/data?time-series-code=wlp-hilo&from={now.strftime("%Y-%m-%dT%H:%M:%SZ")}&to={tomorrow_plus_7_hours.strftime("%Y-%m-%dT%H:%M:%SZ")}')

    
    if r.status_code == 200:
        response = r.json()
        for high_low in response:
            high_low_list.append({
                "date_time": high_low["eventDate"],
                "meters": round(high_low["value"], 2),
                "feet": round(high_low["value"] * 3.2808399, 2),
            })
        high_low_list = determine_high_and_low(high_low_list)
        return high_low_list

def determine_high_and_low(high_low_list):
    list_length = len(high_low_list)
    sorted_high_low_list = sorted(high_low_list, key=lambda d: d['meters'])
    for i in range(list_length//2,list_length):
        sorted_high_low_list[i]["tide"] = "high"
    for tide in sorted_high_low_list:
        if "tide" not in tide:
            tide["tide"] = "low"
    sorted_high_low_list = sorted(high_low_list, key=lambda d: d['date_time'])
    return sorted_high_low_list 


