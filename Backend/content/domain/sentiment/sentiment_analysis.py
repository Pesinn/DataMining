import content.dblayer.dbservice as dbservice
import config
import json

def get_sentiment_analysis(search):
  data = []
  return_data = []
  for i in search["search"]:
    for a in [x for x in load_json() if x["search"] == i]:
      return_data.append(a)
  return return_data

# Temp data
def load_json():
  file = open('content/dblayer/mongodb/test_data/sentiment_analysis.json',)
  data = json.load(file)
  file.close()
  return data