import content.dblayer.dbservice as dbservice
import content.domain.sentiment.sentiment_analysis_factory as sentiment_factory
import content.domain.entities.entities_factory as entity_factory

"""
filter = {
  named_entities: true,
  sentiment_analysis: true,
  articles: {
    limit: 20,
    orderby: date
  }
}
"""
def get_news_data(search, filter):
  return_arr = []
  for i in search:
    return_arr.append(get_news_data_by_single_search(i, filter))
  return return_arr

def get_news_data_by_single_search(s, filter):
  data = dbservice.get_news_data(s, filter)
  articles = []
  index = 0
  sentiment = {}
  ner = {}
  
  for d in data:
    index += 1
    sentiment = get_sentiment_score(
      sentiment, d)
    ner = get_named_entities(
      ner, d, s["search"])

    if index <= int(filter["articles"]["limit"]):
      articles.append(create_article(d))

  final_obj = {
    "sentiment_analysis": sentiment,
    "entities": {
      "named": entity_factory.entity_dict_to_list(ner, 10, s["search"])
    },
    "articles": articles,
    "search": s["search"]
  }

  return final_obj

def get_sentiment_score(combined, data):
  try:
    d = data["annotations"]["sentiment_analysis"]
    return sentiment_factory.calculate_score(
      combined, d)
  except:
    return {}

def get_named_entities(combined, data, search_arr):
  try:
    d = data["annotations"]["entities"]["named"]
    for i in d:
      # Remove named entities that are already in
      # the search string
      if(i in search_arr):
        d.remove(i)
    return entity_factory.count_entities(
      combined, d)
  except:
    return {}

def create_article(data):
  return {
    "title": data["title"]["text"],
    "description": data["description"]["text"],
    "language": data["article_language"],
    "source": data["source"],
    "publish_date": data["publish_date"]
  }