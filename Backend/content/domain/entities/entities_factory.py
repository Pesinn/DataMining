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
def entity_dict_to_list(dict):
  l = []
  for i in dict:
    l.append({
      "entity": i,
      "count": dict[i]["count"],
      "type": dict[i]["type"]
    })
  
  return sorted(l, key=lambda x: x["count"], reverse=True)
