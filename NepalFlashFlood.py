import requests
import pandas as pd
import os
from datetime import date

# Where the data comes from
URL = "https://bipadportal.gov.np/api/v1/incident/"

# 11 = Flood, 17 = Landslide, 14 = Heavy Rainfall
all_rows = []

for hazard_id in [11, 17, 14]:
    params = {
        "hazard": hazard_id,
        "incident_on__gt": "2026-08-26T00:00:00+05:45",
        "expand": "loss,wards",
        "limit": -1,
    }
    r = requests.get(URL, params=params, headers={"Accept": "application/json"})
    all_rows += r.json()["results"]

# Turn it into a table
df = pd.json_normalize(all_rows)

# Stamp today's date on every row
df["snapshot_date"] = date.today().isoformat()
cd
# Add to the same file every time
file_path = "flood_data.csv"
if os.path.exists(file_path):
    df.to_csv(file_path, mode="a", header=False, index=False)
else:
    df.to_csv(file_path, index=False)

print("Saved", len(df), "rows for", date.today())
D:\Python\nepal-flood-analysis