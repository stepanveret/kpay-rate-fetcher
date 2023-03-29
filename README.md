# kpay-rate-fetcher

## Installation
docker-compose up -d

### Install InfluxDB Flux plugin for Graphana
docker exec -it $(docker container ls | grep graphana | awk '{print $1}') /bin/bash
grafana-cli plugins install grafana-influxdb-flux-datasource

#### InfluxQL query to display the graph
'from(bucket: "mydb")
  |> range(start: -1d)
  |> filter(fn: (r) => r["_measurement"] == "gelrub_exchange_rate")
  |> filter(fn: (r) => r["_field"] == "exchange_rate")'

**probably needed**
influx config create --config-name default --org myorg --token user:password --active --host-url http://influxdb:8086