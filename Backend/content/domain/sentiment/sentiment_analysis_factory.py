def convert_db_data_to_domain_data_obj(db_data, search_str):
  obj = {
#    "search": search_str,
    "sentiment_analysis": calculate_analysis_score(db_data)
  }
  add_frequency(obj["sentiment_analysis"], "lowest", "freq", 0)
  add_frequency(obj["sentiment_analysis"], "low", "freq", 0)
  add_frequency(obj["sentiment_analysis"], "middle", "freq", 0)
  add_frequency(obj["sentiment_analysis"], "high", "freq", 0)
  add_frequency(obj["sentiment_analysis"], "highest", "freq", 0)

  return obj

"""
From
[
  {'annotations': {'sentiment_analysis': {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}}
  {'annotations': {'sentiment_analysis': {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}}
]
To
{
  "sentiment_analysis": { "all": { "freq": 2 }, "middle": { "freq": 2 } }
}
"""
def calculate_analysis_score(db_data):
  res = {}

  for i in db_data:
    comp = i["annotations"]["sentiment_analysis"]["compound"]
    if(comp <= -0.75):
      res = add_frequency(res, "lowest", "freq", 1)      
    if(comp > -0.75 and comp <= -0.25):
      res = add_frequency(res, "low", "freq", 1)      
    if(comp > -0.25 and comp < 0.25):
      res = add_frequency(res, "middle", "freq", 1)
    if(comp >= 0.25 and comp < 0.75):
      res = add_frequency(res, "high", "freq", 1)
    if(comp >= 0.75):
      res = add_frequency(res, "highest", "freq", 1)
    res = add_frequency(res, "all", "freq", 1)

  return res

def add_frequency(result, index, sub_index, value):
  try:
    result[index][sub_index] += value
  except:
    try:
      result[index] += {
        sub_index: value
      }
    except:
      result[index] = {
        sub_index: value
      }
  return result
