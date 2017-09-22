import dataHandler
from flask import Flask, send_from_directory, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("","index.html")

@app.route("/search")
def search():
    fromHour = int(request.args.get("from"))
    toHour = int(request.args.get("to"))
    return jsonify(dataHandler.FreeRooms(fromHour,toHour))

dataHandler.init()

if __name__=='__main__':
    ENV = "development"
    if "ENV" in os.environ:
        ENV = os.environ["ENV"]

    app.run(debug=(ENV != "production"), host="0.0.0.0")