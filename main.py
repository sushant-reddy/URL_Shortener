from flask import Flask, request, redirect
from waitress import serve
import random
import string
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://sushant:12345@cluster0.mkt9avr.mongodb.net/?retryWrites=true&w=majority")
db = cluster["URL_DB"]
collection = db["URL"]

app = Flask(__name__)

def generate_short_string(length=5):
    characters = string.ascii_letters + string.digits
    short_string = ''.join(random.choice(characters) for _ in range(length))
    return short_string

@app.route('/api/shorten', methods=['POST'])
def post_data():
    data = request.get_json()
    url = data.get('payload')
    auth_token = request.headers.get('Auth-Token')
    print(url)

    short_string = generate_short_string()
    short_url = f"http://localhost:8080/{short_string}"
    print(short_url)

    urldata = {"URL": url, "short_url": short_url}
    collection.insert_one(urldata)
    return short_url


@app.route('/<short_string>', methods=['GET'])
def redirect_to_url(short_string):
    urldata = collection.find_one({"short_url": f"http://localhost:8080/{short_string}"})
    if urldata:
        finalurl = urldata.get('URL')
        return redirect(finalurl)
    else:
        return "Invalid short URL."

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
