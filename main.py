from flask import Flask, request
from waitress import serve
import random
import string

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
    short_url = f"https://test.ly/{short_string}"
    print(short_url)
    
    return short_url

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
