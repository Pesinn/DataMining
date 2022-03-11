import requests
import config

def get_filter_data():
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/filters').json()