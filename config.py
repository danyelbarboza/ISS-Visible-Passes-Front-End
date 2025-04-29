import os
from dotenv import load_dotenv
from nominatim_client import NominatimClient


class Config:
    def __init__(self, latitude, longitude):
        load_dotenv() 
        self.norad_id = 25544
        self.latitude = float(latitude)
        self.longitude = float(longitude) 
        self.observer_alt = 0
        self.days = 10
        self.min_visibility = 60
        self.api_key = "CFDGBD-XW7A27-6LQ69Y-5GJ7"
        self.gmt = -3