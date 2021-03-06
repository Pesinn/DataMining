import numpy as np

def isIgnore(t):
  ignore_arr = [
    "DET",
    "AUX",
    "INTJ",
    "X",
    "CCONJ",
    "SYM",
    "PRON"]
  
  if t in ignore_arr:
    return True
  return False
    

def append_keywords(combined, data, search_arr):
  for t in data:
    # Skip some trash that is in our database
    if isIgnore(t) == False:
      for a in data[t]:
        for d in a:
          origin = d
          ref = a[d]["l"] + "--" + t
          lemma = a[d]["l"]
          
          if(lemma not in search_arr):
            try:
              if combined[ref]:
                combined[ref]["count"] += 1
                combined[ref]["origin"] = origin
                combined[ref]["type"] = t
                combined[ref]["lemmatized"] = lemma
              else:
                combined[ref] = {
                  "count": 1,
                  "lemmatized": lemma,
                  "type": t,
                  "origin": origin
                }
            except:
              combined[ref] = {
                "count": 1,
                "lemmatized": lemma,
                "type": t,
                "origin": origin
              }
  return combined

def keyword_dict_to_list(dict, limit, search_arr):
  if dict == {}:
    return {}
  l = []
  total_count = 0

  for i in dict:
    if(i not in search_arr):
      l.append({
        "origin": dict[i]["origin"],
        "count": dict[i]["count"],
        "type": dict[i]["type"],
        "lemmatized": dict[i]["lemmatized"]
      })
      total_count = total_count + dict[i]["count"]

  sorted_list = sorted(l, key=lambda x: x["count"], reverse=True)[:limit]
  highest_count = sorted_list[0]["count"]
  limited_count = 0

  for i in sorted_list:
    limited_count = limited_count + i["count"]

  for i in sorted_list:
    i["total_count_ratio"] = np.round((float(i["count"]) / float(total_count))*100, 1)
    i["limited_count_ratio"] = np.round((float(i["count"]) / float(limited_count))*100, 1)
    i["count_ratio_normalized"] = np.round((float(i["count"]) / float(highest_count))*100, 1)

  return sorted_list