import math

def append_keywords(combined, data):
  for t in data:
    if t != "DET":
      for a in data[t]:
        for d in a:
          origin = d
          lemma = a[d]["l"]
          try:
            if combined[lemma]:
              combined[lemma]["count"] += 1
              combined[lemma]["origin"] = origin
            else:
              combined[lemma] = {
                "count": 1,
                "original": origin,
                "lemmatized": lemma,
                "type": t
              }
          except:
            combined[lemma] = {
              "count": 1,
              "original": origin,
              "lemmatized": lemma,
              "type": t
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
        "origin": i,
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
    i["total_count_ratio"] = math.trunc((i["count"] / total_count)*100)
    i["limited_count_ratio"] = math.trunc((i["count"] / limited_count)*100)
    i["count_ratio_normalized"] = math.trunc((i["count"] / highest_count)*100)

  return sorted_list