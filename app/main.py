from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import os

# Read directly from environment or use default
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017/appdb")

# Initialize app
app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI

# Initialize MongoDB
mongo = PyMongo(app)

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok"), 200

# Data endpoint
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

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

