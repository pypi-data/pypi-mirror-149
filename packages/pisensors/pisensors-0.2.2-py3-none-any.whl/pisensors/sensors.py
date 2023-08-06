#from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb import InfluxDBClient, client
#from influxdb_client.client.write_api import SYNCHRONOUS
from baseutils_phornee import ManagedClass
from baseutils_phornee import Logger
from baseutils_phornee import Config
from datetime import datetime

class Sensors(ManagedClass):

    def __init__(self):
        super().__init__(execpath=__file__)

        self.logger = Logger({'modulename': self.getClassName(), 'logpath': 'log'})
        self.config = Config({'modulename': self.getClassName(), 'execpath': __file__})

        host = self.config['influxdbconn']['host']
        user = self.config['influxdbconn']['user']
        password = self.config['influxdbconn']['password']
        bucket = self.config['influxdbconn']['bucket']

        self.conn = InfluxDBClient(host=host, username=user, password=password, database=bucket)

    @classmethod
    def getClassName(cls):
        return "sensors"

    def sensorRead(self):
        """
        Read sensors information
        """
        have_readings = False

        if self.is_raspberry_pi():
            try:
                import adafruit_dht
                dhtSensor = adafruit_dht.DHT22(self.config['pin'])

                humidity = dhtSensor.humidity
                temp_c = dhtSensor.temperature

                have_readings = True
            except Exception as e:
                self.logger.error("Error reading sensor DHT22: {}".format(e))
        else:
                humidity = 50
                temp_c = 25
                have_readings = True

        if have_readings:
            try:
                #write_api = self.conn.write_api(write_options=SYNCHRONOUS)

                json_body = [
                    {
                        "measurement": "DHT22",
                        "tags": {
                            "sensorid": self.config['id']
                        },
                        "time": datetime.utcnow(),
                        "fields": {
                            "temp": float(temp_c),
                            "humidity": float(humidity)
                        }
                    }
                ]
                self.conn.write_points(json_body)

                self.logger.info("Temp: {} | Humid: {}".format(temp_c, humidity))

            except Exception as e:
                self.logger.error("RuntimeError: {}".format(e))
                self.logger.error("influxDBURL={} | influxDBToken={}".format(self.config['influxdbconn']['url'],
                                                                             self.config['influxdbconn']['token']))

if __name__ == "__main__":
    sensors_instance = Sensors()
    sensors_instance.sensorRead()





