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