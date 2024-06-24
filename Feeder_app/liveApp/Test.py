import requests
import json
import pandas as pd
from datetime import datetime
import time

start_time = time.time()

dt1 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
dt1 = dt1.strftime("%Y-%m-%d %H:%M:%S")

dt2 = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
dt2 = dt2.strftime("%Y-%m-%d %H:%M:%S")

payload = {}

url = "http://longi.abujaelectricity.com:10040/comm/login?username=Brian&password=c72a59e998163ccdbac5e0beb3b82778"
headers = {}

try:
    response = requests.request("GET", url, headers=headers, data=payload)
except (TimeoutError, Exception):
    raise Exception("Abuja API connection timed out. Retrying...")

if response is None:
    print("Abuja API request failed after 3 retries.")

try:
    resp = response.json()
except (TimeoutError, Exception):
    raise Exception("Abuja API not available")

sid = resp["sessionID"]
credentials = [sid]

payload = json.dumps({"sessionId": sid, "startdate": dt1, "enddate": dt2})

headers = {"Content-Type": "application/json"}

url = "http://longi.abujaelectricity.com:10040/comm/NERCSBTGetData"

try:
    r = requests.request("POST", url, headers=headers, data=payload)
except (TimeoutError, Exception):
    raise Exception("Abuja API not available at this time")

data = r.json()

try:
    if r.status_code != 200:
        raise Exception(
            f"Abuja API request failed with status code {r.status_code}"
        )
except (TimeoutError, Exception) as e:
    raise Exception("Abuja API not available at this time")

try:
    if not data:
        raise Exception("No data returned from Abuja API.")
except Exception as e:
    raise Exception(e)

res = data.get("data")

df = pd.DataFrame(res)

df.head()
