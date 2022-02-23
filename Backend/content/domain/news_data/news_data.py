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
  display_article_counter = 0

  filter["articles"]["range"] = set_article_count(filter["articles"]["range"], data)

  for d in data:
    index += 1
    sentiment = get_sentiment_score(sentiment, d)
    ner = get_named_entities(ner, d, s["search"])

    if index in range(filter["articles"]["range"]["from"],
                  filter["articles"]["range"]["to"]+1, 1):
      display_article_counter += 1
      articles.append(create_article(d))

  final_obj = {
    "sentiment_analysis": sentiment,
    "entities": {
      "named": entity_factory.entity_dict_to_list(ner, s["named_entities"], s["search"])
    },
    "articles": articles,
    "search": s["search"],
    "articles_count_total": index,
    "articles_range": {
      "from": filter["articles"]["range"]["from"],
      "to": filter["articles"]["range"]["from"] + display_article_counter
    }
  }

  return final_obj

# Make sure to get correct article range
# If article_range=last, make sure to get
# the correct range for that case
def set_article_count(article_range, data):
  if(article_range["to"] == "last"):
    data_len = len(data)
    if(data_len < article_range["default"]):
      article_range["from"] = 0
      article_range["to"] = data_len
    else:
      article_range["from"] = data_len - article_range["default"]
      article_range["to"] = data_len
  return article_range

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
    # Copy is made so we can delete elements from 'd_copy'
    # while iteration though 'd'
    d_copy = dict(d)
    for i in d:
      # Remove named entities that are already in
      # the search string
      if(i in search_arr):
        del d_copy[i]

    return entity_factory.count_entities(
      combined, d_copy)
  except Exception as error:
    if(str(error) != "'entities'" and str(error) != "'annotations'"):
      print("Error:", str(error))
    return {}

def create_article(data):
  return {
    "title": data["title"]["text"],
    "description": data["description"]["text"],
    "language": data["article_language"],
    "source": data["source"],
    "publish_date": data["publish_date"]
  }