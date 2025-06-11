import requests
from datetime import datetime, timezone, timedelta

class N2yoClient:
    def __init__(self, config):
        self.norad_id = config.norad_id
        self.latitude = config.latitude
        self.longitude = config.longitude
        self.observer_alt = 0
        self.days = config.days
        self.min_visibility = config.min_visibility
        self.api_key = config.api_key
        self.gmt = -3
    
    def fetch_data(self):
        response = requests.get(f"https://api.n2yo.com/rest/v1/satellite/visualpasses/{self.norad_id}/{self.latitude}/{self.longitude}/{self.observer_alt}/{self.days}/{self.min_visibility}/&apiKey={self.api_key}")
        return response.json()
    
    def display_passes(self):
        passes = self.fetch_data()["passes"]
        all_passes = []
        count = 1
        for p in passes:
            timestamp = int(p['startUTC'])
            dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            dt_local = dt_utc.astimezone(timezone(timedelta(hours=self.gmt)))
            all_passes.append({
                "id": count,
                "start": dt_local.strftime("%Y-%m-%dT%H:%M"),
                "duration": p['duration']
            })
            count += 1
        return all_passes

