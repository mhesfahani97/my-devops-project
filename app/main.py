from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
import os
import logging
import json
import socket

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://lifeweb:It5~TPn04p1-eTAH@database:27017/appdb?authSource=admin"
)

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI

metrics = PrometheusMetrics(app)

mongo = PyMongo(app)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "time": self.formatTime(record, self.datefmt),
            "path": record.pathname,
            "line": record.lineno
        })

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)

class TCPLogstashHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = self.format(record)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("logstash", 5000))  # Uses Docker service name
            sock.sendall((log_entry + "\n").encode("utf-8"))
            sock.close()
        except Exception as e:
            print(f"Logging to Logstash failed: {e}")

tcp_handler = TCPLogstashHandler()
tcp_handler.setFormatter(JSONFormatter())
logger.addHandler(tcp_handler)

@app.route("/health", methods=["GET"])
def health():
    logger.info("Health check accessed")
    return jsonify(status="ok"), 200

@app.route("/data", methods=["GET", "POST"])
def data():
    collection = mongo.db.testdata
    if request.method == "POST":
        data = request.json
        collection.insert_one(data)
        logger.info(f"Inserted data: {data}")
        return jsonify(message="Data inserted"), 201
    else:
        docs = list(collection.find({}, {"_id": 0}))
        logger.info(f"Retrieved {len(docs)} documents")
        return jsonify(docs), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

