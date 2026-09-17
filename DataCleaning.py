import pandas as pd
import os
import json

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "flood_data.csv"))

# 1. Keep only what you need, with readable names
keep = {
    "id": "incident_id",
    "title": "title",
    "incidentOn": "incident_date",
    "reportedOn": "reported_date",
    "hazard": "hazard_id",
    "point.coordinates": "coords",
    "loss.peopleDeathCount": "deaths",
    "loss.peopleMissingCount": "missing",
    "loss.peopleInjuredCount": "injured",
    "loss.familyAffectedCount": "families_affected",
    "loss.infrastructureDestroyedHouseCount": "houses_destroyed",
    "snapshot_date": "snapshot_date",
}
df = df[list(keep)].rename(columns=keep)

# 2. Turn date text into real dates
df["incident_date"] = pd.to_datetime(df["incident_date"], utc=True).dt.tz_convert("Asia/Kathmandu")
df["reported_date"] = pd.to_datetime(df["reported_date"], utc=True).dt.tz_convert("Asia/Kathmandu")

# 3. How long between it happening and being reported
df["report_lag_hours"] = (df["reported_date"] - df["incident_date"]).dt.total_seconds() / 3600

# 4. Numbers -> names
df["hazard"] = df["hazard_id"].map({11: "Flood", 17: "Landslide", 14: "Heavy Rainfall"})

# 5. Split coordinates into latitude and longitude
def latlon(v):
    try:
        lon, lat = json.loads(str(v).replace("'", '"'))
        return pd.Series([lat, lon])
    except Exception:
        return pd.Series([None, None])

df[["latitude", "longitude"]] = df["coords"].apply(latlon)
df = df.drop(columns=["coords", "hazard_id"])

# 6. Blank counts become 0, not empty
for c in ["deaths", "missing", "injured", "families_affected", "houses_destroyed"]:
    df[c] = df[c].fillna(0).astype(int)

df["incident_date"] = df["incident_date"].dt.date

df.to_csv(os.path.join(folder, "flood_clean.csv"), index=False)
print("Cleaned:", len(df), "rows,", len(df.columns), "columns")