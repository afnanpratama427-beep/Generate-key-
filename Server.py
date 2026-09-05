from flask import Flask, request, jsonify
import json
import random
import string
import os

app = Flask(__name__)
DB_FILE = 'database.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

@app.route('/')
def home():
    return "Key Server is Running!"

@app.route('/generate_key', methods=['POST'])
def generate():
    db = load_db()
    new_key = generate_key()
    db[new_key] = {"status": "unused"}
    save_db(db)
    return jsonify({"key": new_key})

@app.route('/verify_key', methods=['POST'])
def verify():
    data = request.get_json()
    key = data.get('key')
    db = load_db()

    if key in db and db[key]['status'] == 'unused':
        db[key]['status'] = 'used'
        save_db(db)
        return jsonify({"valid": True, "message": "Key accepted"})

    return jsonify({"valid": False, "message": "Invalid or used key"})
