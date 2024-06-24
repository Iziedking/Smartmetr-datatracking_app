from django.shortcuts import render
import requests
import json
import pandas as pd
import time
from datetime import datetime

def getAbujaData(request):
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
        return render(request, 'live_App/home.html', {"error": "Abuja API connection failed", "details": str(e)})

    try:
        resp = response.json()
    except json.JSONDecodeError:
        return render(request, 'live_App/home.html', {"error": "Failed to parse JSON response from Abuja API"})

    sid = resp.get("sessionID")
    if not sid:
        return render(request, 'live_App/home.html', {"error": "No sessionID in response from Abuja API"})

    payload = json.dumps({"sessionId": sid, "startdate": dt1, "enddate": dt2})

    headers = {"Content-Type": "application/json"}
    url = "http://longi.abujaelectricity.com:10040/comm/NERCSBTGetData"

    try:
        r = requests.post(url, headers=headers, data=payload)
        r.raise_for_status()
    except requests.RequestException as e:
        return render(request, 'live_App/home.html', {"error": "Failed to fetch data from Abuja API", "details": str(e)})

    try:
        data = r.json()
    except json.JSONDecodeError:
        return render(request, 'live_App/home.html', {"error": "Failed to parse JSON response from Abuja API"})

    if not data:
        return render(request, 'live_App/home.html', {"error": "No data returned from Abuja API"})

    res = data.get("data")
    if not res:
        return render(request, 'live_App/home.html', {"error": "No 'data' field in response from Abuja API"})

    df = pd.DataFrame(data=res)
    if df.empty:
        return render(request, 'live_App/home.html', {"error": "AEDC API response DataFrame is empty"})

    processed_data = df.to_dict(orient='records')

    end_time = time.time()
    execution_time = end_time - start_time
    execution_time = "{:.2f}".format(execution_time)

    response_data = {
        "message": "Data fetched and processed successfully",
        "execution_time": execution_time,
        "data": processed_data
    }

    return render(request, 'live_App/home.html', response_data)
