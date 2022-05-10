import numpy as np

"""
obj : {
  "all": {
    "freq": 3926
  },
  "high": {
    "freq": 353
  },
  "highest": {
    "freq": 4
  },
  "low": {
    "freq": 479
  },
  "lowest": {
    "freq": 19
  },
  "middle": {
    "freq": 3071
  }
},
data : {
  neg: 0,
  neu: 0.863,
  pos: 0.137,
  compound: 0.26335
}
"""
def calculate_score(obj, data):
  res = {}
  if obj == {}:
    obj = create_sentiment_domain_object()

  comp = data["compound"]
  if(comp <= -0.75):
    res = add_frequency(obj, "lowest", "freq", 1)
  if(comp > -0.75 and comp <= -0.05):
    res = add_frequency(obj, "low", "freq", 1)
  if(comp > -0.05 and comp < 0.05):
    res = add_frequency(obj, "middle", "freq", 1)
  if(comp >= 0.05 and comp < 0.75):
    res = add_frequency(obj, "high", "freq", 1)
  if(comp >= 0.75):
    res = add_frequency(obj, "highest", "freq", 1)
  res = add_frequency(obj, "all", "freq", 1)
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

def create_sentiment_domain_object():
  return {
    "all": {
      "freq": 0
    },
    "high": {
      "freq": 0
    },
    "highest": {
      "freq": 0
    },
    "low": {
      "freq": 0
    },
    "lowest": {
      "freq": 0
    },
    "middle": {
      "freq": 0
    }
  }
  
def calculate_ratio_score(obj, data):
  if obj == {}:
    obj = create_sentiment_ratio_domain_object()

  obj["negative"] += data["neg"]
  obj["neutral"] += data["neu"]
  obj["positive"] += data["pos"]

  return obj

def create_sentiment_ratio_domain_object():
  return {
    "negative": 0.0,
    "neutral": 0.0,
    "positive": 0.0,
  }
  
def round_sentiment_score_ratio(data, count):
  if(count > 0):
    data["negative"] = float(np.round((data["negative"]/count), 2)) * 100
    data["neutral"] = float(np.round((data["neutral"]/count), 2)) * 100
    data["positive"] = float(np.round((data["positive"]/count), 2)) * 100
  
    data["negative"] = int(data["negative"])
    data["neutral"] = int(data["neutral"])
    data["positive"] = int(data["positive"])
  
  return data