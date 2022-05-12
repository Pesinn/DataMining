import requests
import config

def get_keywords(req):
  data = get_keywords_service(req)
  return data

def get_keywords_service(req):
  return requests.request("GET", f'{config.BACKEND_URL}/api/v1/keywords?{req}').json()