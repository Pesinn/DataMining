import numpy as np

"""
combined: {
  "ENTITY": FREQUENCY
}
ent: {
  'Justin Bieber': 'PERSON',
  Yummy: 'NORP',
  'CBC Music': 'ORG',
  Canadian: 'NORP',
  'a busy year': 'DATE'
}

"""
def count_entities(combined, ent):
  for e in ent:
    try:
      combined[e]["count"] += 1
      combined[e]["type"] = ent[e]
    except:
      combined[e] = {
        "count": 1,
        "type": ent[e]
      }
  return combined

"""
Input:
"Rolls Royce":
{
  "count": 1,
  "type": "ORG"
},
"TESLA": {
  "count": 2,
  "type": "ORG"
}

Output:
[
  {
    "count": 2,
    "entity": "TESLA",
    "type": "ORG"
  },
  {
    "count": 1,
    "entity": "Rolls Royce",
    "type": "ORG"
  }
]
"""
def entity_dict_to_list(dict, limit, search_arr):
  if dict == {}:
    return {}
  
  l = []
  total_count = 0
  for i in dict:
    if(i not in search_arr):
      l.append({
        "entity": i,
        "count": dict[i]["count"],
        "type": dict[i]["type"]
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
