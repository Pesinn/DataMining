import content.dblayer.dbservice as dbservice
import content.domain.sentiment.sentiment_analysis_factory as factory
import config
import json

def get_sentiment_analysis(search):
  if(config.get_db_collection() == "None"):
    return get_sentiment_analysis_from_file(search)
  else:
    return get_sentiment_analysis_from_db(search)

def get_sentiment_analysis_from_file(search):
  s_analysis = []
  for i in search["search"]:
    for a in [x for x in load_json() if x["search"] == i]:
      s_analysis.append(a)
  return s_analysis

def get_sentiment_analysis_from_db(search):
  s_analysis = []
  for i in search:
    d = dbservice.get_sentiment_analysis(i)
    s_analysis.append(factory.convert_db_data_to_domain_data_obj(d, i["search"]))
  return s_analysis

# Temp data
def load_json():
  file = open('content/dblayer/mongodb/test_data/sentiment_analysis.json',)
  data = json.load(file)
  file.close()
  return data