import time

from flask import Flask, request, abort
from NLPBot.bot import bot
import BC.blockchain as bc
import pymysql
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

@app.route("/confirm_event")
def confirm_event():
    # должен передаваться ИД мероприятия
    data = request.json
    # подключаюсь к БД
    #Адрес, #Пользователь, #Пароль, #Имя БД
    connection = pymysql.connect(host="", user="", password="", database="")
    # делаем запрос к табличке EventCompetence
    curs = connection.cursor()
    # curs.execute("SELECT * FROM EventCompetence WHERE idevent=%s",  data["event_id"])
    curs.execute("Текст запроса")
    # сохраняем результат
    rows = curs.fetchall()
    # проходим по всем записям результата
    for row in rows:
        # будем вызывать функцию bc.append_blockchain()
        print(" {0} {1} {2} ".format(row[0], row[1], row[2]))


app.run()
