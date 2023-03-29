import time

import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from config import AppConfig

config = AppConfig()


def fetch_data():
    session = requests.Session()
    session.headers.update(config.SESSION_HEADERS)
    response = session.get(config.URL)
    response.raise_for_status()
    return response.json()


def save_to_influxdb(data):
    client = InfluxDBClient(url=config.INFLUXDB_URL, token=config.INFLUXDB_TOKEN, org=config.INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = (
        Point("gelrub_exchange_rate")
        .tag("sending_currency", data[0]["sendingCurrency"]["code"])
        .tag("receiving_currency", data[0]["receivingCurrency"]["code"])
        .field("exchange_rate", data[0]["exchangeRate"])
    )

    write_api.write(bucket=config.INFLUXDB_BUCKET, record=point)

    write_api.close()
    client.close()


if __name__ == "__main__":
    time.sleep(config.INTERVAL_STARTUP)
    i = 0
    while True:
        i += 1
        print(f'LOG request: {i}, CURR_TIME: {time.strftime("%H:%M:%S", time.localtime())}')
        try:
            data = fetch_data()
            print("LOG fetch success:", data)
            save_to_influxdb(data)
            print("LOG save success")
            time.sleep(config.INTERVAL_SUCCESS)
        except Exception as e:
            print(f"Error fetching data: {e}")
            time.sleep(config.INTERVAL_FAIL)
