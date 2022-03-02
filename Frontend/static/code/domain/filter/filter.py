import requests

def get_filter_data():
  return requests.request("GET", f'http://192.168.8.105:8080/api/v1/filters').json()