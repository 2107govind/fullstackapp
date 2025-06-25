
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Replace with your actual MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://vikasbadaltem123:<db_password>@cluster0.udqdqoq.mongodb.net/")
client = MongoClient(MONGO_URI)
db = client["portfolio"]

# Collections
projects_col = db["projects"]
clients_col = db["clients"]
contacts_col = db["contacts"]
newsletter_col = db["newsletter"]

# ---- Projects ----
@app.route("/api/projects", methods=["GET", "POST"])
def projects():
    if request.method == "GET":
        data = list(projects_col.find({}, {"_id": 0}))
        return jsonify(data)
    else:
        data = request.json
        projects_col.insert_one(data)
        return jsonify({"message": "Project added"}), 201

# ---- Clients ----
@app.route("/api/clients", methods=["GET", "POST"])
def clients():
    if request.method == "GET":
        data = list(clients_col.find({}, {"_id": 0}))
        return jsonify(data)
    else:
        data = request.json
        clients_col.insert_one(data)
        return jsonify({"message": "Client added"}), 201

# ---- Contact Form ----
@app.route("/api/contact", methods=["GET","POST"])
def contact():
    data = request.json
    contacts_col.insert_one(data)
    return jsonify({"message": "Contact saved"}), 201

@app.route("/api/contacts", methods=["GET"])
def get_contacts():
    data = list(contacts_col.find({}, {"_id": 0}))
    return jsonify(data)

# ---- Newsletter ----
@app.route("/api/newsletter", methods=["POST"])
def subscribe():
    email = request.json.get("email")
    if email:
        newsletter_col.insert_one({"email": email})
        return jsonify({"message": "Subscribed"}), 201
    return jsonify({"error": "Email is required"}), 400

@app.route("/api/newsletter", methods=["GET"])
def get_subscribers():
    data = list(newsletter_col.find({}, {"_id": 0}))
    return jsonify(data)

# ---- Main ----
if __name__ == "__main__":
    app.run(debug=True)
