from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request, jsonify
from flask import render_template
import os
import static.code.search as domain_articles
import static.code.factory.request as req

app = Flask(__name__)

@app.route('/index',  methods=["GET"])
@app.route('/',  methods=["GET"])
def index():

  # No results should be provided until use has entered a search query
  if request.args.get("search"):
    search_req = req.conv_req_to_query_string(request)
    art = domain_articles.get_news_data(search_req)
  else:
    art = []
  return render_template("articles.html", articles = art)

@app.route('/entities', methods=["GET"])
def entities():
  return render_template("entities.html")

@app.route('/sentiment', methods=["GET"])
def sentiment():
  return render_template("sentiment.html")


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
