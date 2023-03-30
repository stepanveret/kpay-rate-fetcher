from flask import Flask, send_from_directory, jsonify
from influxdb_client import InfluxDBClient

app = Flask(__name__, static_folder=".")

config = {
    "influxdb_url": "http://influxdb:8086",
    "influxdb_token": "user:password",
    "influxdb_org": "myorg",
    "influxdb_bucket": "mydb",
}

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory("images", filename)

@app.route("/api/rate")
def rate():
    client = InfluxDBClient(url=config["influxdb_url"], token=config["influxdb_token"], org=config["influxdb_org"])
    query_api = client.query_api()

    query = f'from(bucket: "{config["influxdb_bucket"]}") |> range(start: -10m) |> filter(fn: (r) => r["_measurement"] == "gelrub_exchange_rate") |> last()'
    result = query_api.query(query)

    if not result:
        return jsonify({"rate": None, "increased": None})

    last_record = result[0].records[0]
    last_rate = last_record.get_value()
    last_time = last_record.get_time()

    query_prev = f'from(bucket: "{config["influxdb_bucket"]}") |> range(start: -20m, stop: -10m) |> filter(fn: (r) => r["_measurement"] == "gelrub_exchange_rate") |> last()'
    result_prev = query_api.query(query_prev)

    if not result_prev:
        return jsonify({"rate": last_rate, "increased": None})

    prev_rate = result_prev[0].records[0].get_value()
    increased = last_rate > prev_rate

    return jsonify({"rate": last_rate, "increased": increased})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)