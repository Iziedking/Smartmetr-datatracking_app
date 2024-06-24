import requests
import json
import pandas as pd
import time
from datetime import datetime
import os

def getAbujaData():
    start_time = time.time()

    dt1 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dt1 = dt1.strftime("%Y-%m-%d %H:%M:%S")

    dt2 = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    dt2 = dt2.strftime("%Y-%m-%d %H:%M:%S")

    payload = {}
    url = "http://longi.abujaelectricity.com:10040/comm/login?username=Brian&password=c72a59e998163ccdbac5e0beb3b82778"
    headers = {}

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Abuja API connection failed: {e}")
        return

    try:
        resp = response.json()
    except json.JSONDecodeError:
        print("Failed to parse JSON response from Abuja API")
        return

    sid = resp.get("sessionID")
    if not sid:
        print("No sessionID in response from Abuja API")
        return

    payload = json.dumps({"sessionId": sid, "startdate": dt1, "enddate": dt2})

    headers = {"Content-Type": "application/json"}
    url = "http://longi.abujaelectricity.com:10040/comm/NERCSBTGetData"

    try:
        r = requests.post(url, headers=headers, data=payload)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch data from Abuja API: {e}")
        return

    try:
        data = r.json()
    except json.JSONDecodeError:
        print("Failed to parse JSON response from Abuja API")
        return

    if not data:
        print("No data returned from Abuja API")
        return

    res = data.get("data")
    if not res:
        print("No 'data' field in response from Abuja API")
        return

    df = pd.DataFrame(data=res)
    if df.empty:
        print("AEDC API response DataFrame is empty")
        return

    processed_data = df.to_dict(orient='records')

  
    output_directory = "C:\\Users\\IZIE.IZIE17\\Desktop\\Disco_API data"
    output_filename = "abuja_data.json"
    output_filepath = os.path.join(output_directory, output_filename)

  
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    end_time = time.time()
    execution_time = "{:.2f}".format(end_time - start_time)

    print(f"Data fetched, processed, and saved successfully in {execution_time} seconds")


getAbujaData()
