# pisensors
Raspberry Pi Sensors script for Temperature & Humidity.
Reads from a DHT22 temperature/humidity sensor, and insert info into a InfluxDB, so that it can be later used by Grafana or whatever

It needs to be executed every x minutes (i.e. cron) 