from flask import Flask, send_from_directory, jsonify
from influxdb import InfluxDBClient

app = Flask(__name__, static_folder=".")

config = {
    "influxdb_url": "http://influxdb:8086",
    "influxdb_user": "user",
    "influxdb_password": "password",
    "influxdb_db": "mydb",
}

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory("images", filename)

@app.route("/api/rate")
def rate():
    client = InfluxDBClient(host="influxdb", username=config["influxdb_user"], password=config["influxdb_password"], database=config["influxdb_db"])
    query = f"SELECT last(\"exchange_rate\") FROM \"gelrub_exchange_rate\" WHERE time >= now() - 10m"
    result = client.query(query).raw

    if not result["series"]:
        return jsonify({"rate": None, "increased": None})

    last_rate = result["series"][0]["values"][0][1]

    query_prev = f"SELECT last(\"exchange_rate\") FROM \"gelrub_exchange_rate\" WHERE time >= now() - 20m AND time < now() - 10m"
    result_prev = client.query(query_prev).raw

    if not result_prev["series"]:
        return jsonify({"rate": last_rate, "increased": None})

    prev_rate = result_prev["series"][0]["values"][0][1]
    increased = last_rate > prev_rate

    return jsonify({"rate": last_rate, "increased": increased})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

