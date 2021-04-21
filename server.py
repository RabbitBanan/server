import time

from flask import Flask, request, abort
from NLPBot.bot import bot
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/status")
def status():
    return {
        "status": True,

        "name": "API Adaptation",
        "time": time.asctime(),
    }

#@app.route("/send", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)
    name = data["name"]
    text = data["text"]
    if not isinstance(name, str) or not isinstance(text, str):
        abort(400)
    if name == '' or text == '':
        abort(400)
    return {
        'Answer' : bot(text),
    }

@app.route("/message")
def get_message():
    try:
        text = str(request.args['text'])
    except:
        return abort(400)
    return {
        'Answer': bot(text),
    }



app.run()