from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request, jsonify
from flask import render_template
import os
import static.code.search as domain_articles
import static.code.factory.request as req

app = Flask(__name__)



labels = [
    'Very negative', 'Negative', 'Neutral', 'Very positive',
    'Positive'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91
]

sentiment_analysis = """
[
  {
    "search": "Alibaba",
    "sentiment_analysis": {
      "lowers": {
        "freq": 50,
        "ratio": 0.13
      },
      "low": {
        "freq": 40,
        "ratio": 0.1
      },
      "middle": {
        "freq": 120,
        "ratio": 0.31
      },
      "high": {
        "freq": 130,
        "ratio": 0.34
      },
      "highest": {
        "freq": 45,
        "ratio": 0.12
      },
      "all": {
        "freq": 385,
        "ratio": 100
      }
    }
  }
]
"""

@app.route('/index',  methods=["GET"])
@app.route('/',  methods=["GET"])
def index():
  # No results should be provided until use has entered a search query
  if request.args.get("search"):
    search_req = req.conv_req_to_query_string(request)
    art = domain_articles.get_articles(search_req)
  else:
    art = []
  return render_template("articles.html", articles = art)

@app.route('/entities', methods=["GET"])
def entities():
  return render_template("entities.html")

@app.route('/sentiment', methods=["GET"])
def sentiment():
  bar_labels=labels
  bar_values=values
  return render_template("sentiment.html", title='Bitcoin Monthly Price in USD',
    max=17000, labels=bar_labels, values=bar_values, data=sentiment_analysis)


#@app.route('/books/', methods=["POST", "GET"])
#@app.route('/books/<id>', methods=["POST", "GET"])
#def books(id=None):
#    if(id!=None):
#        return render_template("books.html", books=getBookById(id))
#    return render_template("books.html", books=getBooks())


#def getBookById(id):
#    print("id: ", id)
#    response = requests.request("GET", f'http://192.168.8.105:8080/api/v1/resources/books?id={id}')
#    return response.json()

#def getBooks():
#    response = requests.request("GET", 'http://192.168.8.105:8080/api/v1/resources/books/all')
#    json_obj = response.json()
#    return json_obj

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
