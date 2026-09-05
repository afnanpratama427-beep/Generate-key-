    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import datetime, random, string, json, os

    app = Flask(__name__)
    CORS(app)
    DB_FILE = "database.json"

    def baca_db():
        if not os.path.exists(DB_FILE): return {}
        with open(DB_FILE, "r") as f: return json.load(f)

    def tulis_db(data):
        with open(DB_FILE, "w") as f: json.dump(data, f)

    def generate_key(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    def hitung_tanggal(periode):
        sekarang = datetime.datetime.now()
        if periode == "1h": return sekarang + datetime.timedelta(days=1)
        if periode == "7h": return sekarang + datetime.timedelta(days=7)
        if periode == "30h": return sekarang + datetime.timedelta(days=30)
        if periode == "1b": return sekarang + datetime.timedelta(days=30)
        if periode == "3b": return sekarang + datetime.timedelta(days=90)
        if periode == "perm": return datetime.datetime(2099, 12, 31)

    @app.route("/generate", methods=["POST"])
    def generate():
        data = request.json
        if data.get("password")!= "endxz123": return jsonify({"error": "Password salah"})
        db = baca_db()
        key_baru = generate_key()
        expired = hitung_tanggal(data.get("periode"))
        db[key_baru] = expired.strftime("%Y-%m-%d %H:%M:%S")
        tulis_db(db)
        return jsonify({"key": key_baru, "expired": db[key_baru]})

    @app.route("/cek", methods=["POST"])
    def cek():
        data = request.json
        db = baca_db()
        if data.get("key") in db:
            expired = datetime.datetime.strptime(db[data.get("key")], "%Y-%m-%d %H:%M:%S")
            if datetime.datetime.now() <= expired: return jsonify({"status": "AKTIF"})
        return jsonify({"status": "MATI"})

    if __name__ == "__main__": app.run(host="0.0.0.0", port=10000)
