from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
import os

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://lifeweb:It5~TPn04p1-eTAH@database:27017/appdb?authSource=admin"
)

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI

metrics = PrometheusMetrics(app)

mongo = PyMongo(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

@app.route("/data", methods=["GET", "POST"])
def data():
    collection = mongo.db.testdata
    if request.method == "POST":
        data = request.json
        collection.insert_one(data)
        return jsonify(message="Data inserted"), 201
    else:
        docs = list(collection.find({}, {"_id": 0}))
        return jsonify(docs), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

