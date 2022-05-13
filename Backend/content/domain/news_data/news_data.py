import content.dblayer.dbservice as dbservice
import content.domain.sentiment.sentiment_analysis_factory as sentiment_factory
import content.domain.entities.entities_factory as entity_factory
import content.domain.keywords.keywords_factory as keywords_factory

"""
search = [
  {
    'languages': ['en', 'fr'],
    'date_from': '2020-01-01',
    'date_to': '2022-01-01',
    'sources': ['abc.net.au'],
    'named_entities': 10,
    'search': ['tesla']
  }
]
filter = {
    'named_entities': False,
    'sentiment_analysis': False,
    '_id': True,
    'description_text': True,
    'title_text': True,
    'article_language': True,
    'publish_date': True,
    'source': True,
    'articles': {
      'range': {
        'from': 0,
        'to': 11,
        'default': 10
      },
    'orderby': 'date'
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
  keywords = {}
  articles = []
  index = 0
  sentiment = sentiment_factory.create_sentiment_domain_object()
  sentiment_ratio = sentiment_factory.create_sentiment_ratio_domain_object()
  ner = {}
  filter_count = {"languages": {}, "sources": {}, "total": 0}
  display_article_counter = 0
  filter["articles"]["range"] = set_article_count(filter["articles"]["range"], data)

  for d in data:
    index += 1
    keywords = get_keywords(keywords, d, s["search"])
    sentiment = get_sentiment_score(sentiment, d)
    sentiment_ratio = get_sentiment_score_ratio(sentiment_ratio, d)
    ner = get_named_entities(ner, d, s["search"])
    append_filter_count(d, filter_count)

    if index in range(filter["articles"]["range"]["from"],
                  filter["articles"]["range"]["to"]+1, 1):
      display_article_counter += 1
      articles.append(create_article(d))

  final_obj = {
    "keywords": keywords_factory.keyword_dict_to_list(keywords, s["keywords"], s["search"]),
    "sentiment_analysis": {
      "compound": sentiment,
      "text_ratio": round_sentiment_score_ratio(sentiment_ratio, index)
    },
    "entities": {
      "named": entity_factory.entity_dict_to_list(ner, s["named_entities"], s["search"])
    },
    "articles": articles,
    "search": s["search"],
    "articles_range": {
      "from": filter["articles"]["range"]["from"],
      "to": filter["articles"]["range"]["from"] + display_article_counter-1
    },
    "articles_count": filter_count,
  }

  return final_obj

# Count articles that belong to each filter
def append_filter_count(article, filter_count):
  try:
    filter_count["total"] += 1
  except:
    filter_count["total"] = 1

  try:
    filter_count["languages"][article["article_language"]] += 1
  except:
    filter_count["languages"][article["article_language"]] = 1
    
  try:
    filter_count["sources"][article["source"]] += 1
  except:
    filter_count["sources"][article["source"]] = 1

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

def get_sentiment_score_ratio(combined, data):
  try:
    d = data["annotations"]["sentiment_analysis"]
    return sentiment_factory.calculate_ratio_score(
      combined, d)
  except:
    return {}

def round_sentiment_score_ratio(data, count):
  # No need to round any numbers unless we have sentiment data in our query
  if data != {}:
    return sentiment_factory.round_sentiment_score_ratio(data, count)

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

def get_keywords(combined, data, search_arr):
  try:
    d1 = data["description"]["keywords"]["categorized"]
    d2 = data["title"]["keywords"]["categorized"]
    d = combine_dictionaries(d1, d2)
    # Copy is made so we can delete elements from 'd_copy'
    # while iteration though 'd'
    d_copy = dict(d)
    for i in d:
      # Remove named entities that are already in
      # the search string
      for o in d[i]:
        for w in o:
          #accessing the lemmatized version of the word:
          # E.g. {'power': {'l': 'power'}} and compare to
          # the search array
          if(o[w]["l"] in search_arr):
            del d_copy[i]
    
    return keywords_factory.append_keywords(combined, d_copy)
  except Exception as error:
    if(str(error) != "'keywords'" and str(error) != "'annotations'"):
      print("Error:", str(error))
    return {}

def create_article(data):
  return {
    "title": data["title"]["text"],
    "description": data["description"]["text"],
    "language": data["article_language"],
    "source": data["source"],
    "publish_date": data["publish_date"],
    "link": data["link"]
  }
  
def combine_dictionaries(dict1, dict2):
  merged = dict()
  merged.update(dict1)
  merged.update(dict2)
  return merged