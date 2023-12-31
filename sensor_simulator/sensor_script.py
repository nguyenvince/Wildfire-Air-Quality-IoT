import random
import time
import json
import paho.mqtt.client as mqtt

# MQTT Server Parameters
MQTT_CLIENT_ID = "simulated_python_sensor"
MQTT_BROKER = "mqtt_broker"
MQTT_PORT = 1883
MQTT_TOPIC = "wildfire-air-quality"

# Initial coordinates
INITIAL_LAT = 42.411567
INITIAL_LONG = 13.397309
# Previous coordinates
prev_lat = INITIAL_LAT
prev_long = INITIAL_LONG
# Max amount to move lat and long
MOVE_AMOUNT = 0.001

# Sensor measurement range constants
MIN_PM2_5 = 0
MAX_PM2_5 = 1000
MIN_NO2 = 0
MAX_NO2 = 500
MIN_CO2 = 400
MAX_CO2 = 10000

# Function to get coordinates with slight random variations
def getCoordinates():
    new_lat = round(random.gauss(prev_lat, MOVE_AMOUNT), 6)
    new_long = round(random.gauss(prev_long, MOVE_AMOUNT), 6)

    return new_lat, new_long

# Simulate DHT22 weather sensor
class SimulatedDHT22:
    def __init__(self, mean_temp, temp_deviation, mean_humid, humid_deviation):
        self.mean_temp = mean_temp
        self.temp_deviation = temp_deviation
        self.mean_humid = mean_humid
        self.humid_deviation = humid_deviation

    def measure(self):
        pass

    def temperature(self):
        return round(random.gauss(self.mean_temp, self.temp_deviation), 1)

    def humidity(self):
        return round(random.gauss(self.mean_humid, self.humid_deviation), 1)

weatherSensor = SimulatedDHT22(mean_temp=25, temp_deviation=2, mean_humid=50, humid_deviation=5)

# Simulate ADC for air quality sensors
class SimulatedADC:
    def __init__(self, mean_value, deviation):
        self.mean_value = mean_value
        self.deviation = deviation

    def read(self):
        return round(random.gauss(self.mean_value, self.deviation), 1)

dustSensor = SimulatedADC(mean_value=20, deviation=5)
no2Sensor = SimulatedADC(mean_value=50, deviation=10)
co2Sensor = SimulatedADC(mean_value=500, deviation=50)

prev_weather = ""

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload}")

# Create an MQTT client instance
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop in the background
client.loop_start()

# Main loop for publishing simulated sensor data
while True:
    # Get coordinates with slight random variations
    lat, long = getCoordinates()

    # Read simulated weather (temperature and humidity)
    temperature = weatherSensor.temperature()
    humidity = weatherSensor.humidity()

    # Generate random air quality sensor values in the correct range
    mappedDust = dustSensor.read()
    mappedCO2 = co2Sensor.read()
    mappedNO2 = no2Sensor.read()

    message = json.dumps({
        "sensorId": MQTT_CLIENT_ID,
        "latitude": lat, 
        "longitude": long,
        "temperature": temperature,
        "humidity": humidity,
        "dust": mappedDust,
        "co2": mappedCO2,
        "no2": mappedNO2
    })

    if message != prev_weather:
        print(message)
        # Publish the message to the MQTT broker
        client.publish(MQTT_TOPIC, message)

        prev_weather = message

    # Update previous coordinates
    prev_lat, prev_long = lat, long

    # Wait for 1 second before sending the next message
    time.sleep(1)
