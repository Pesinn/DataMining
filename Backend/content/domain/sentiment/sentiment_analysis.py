import content.dblayer.dbservice as dbservice
import config
import json

def get_sentiment_analysis(search):
  return load_json()
    



# Temp data
def load_json():
  file = open('content/dblayer/mongodb/test_data/sentiment_analysis.json',)
  data = json.load(file)
  file.close()
  return data