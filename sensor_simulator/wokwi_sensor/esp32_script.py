import network
import time
from machine import Pin, ADC, I2C
import ssd1306
import dht
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "sensor1"
MQTT_BROKER    = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "wildfire-air-quality"

# ESP32 Pin assignment 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# OLED screen parameters
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

weatherSensor = dht.DHT22(Pin(15))

MIN_ADC = 0
MAX_ADC = 4095

dustSensor = ADC(Pin(34))
dustSensor.atten(ADC.ATTN_11DB)
MIN_PM2_5 = 0
MAX_PM2_5 = 1000

no2Sensor = ADC(Pin(32))
no2Sensor.atten(ADC.ATTN_11DB)
MIN_NO2 = 0
MAX_NO2 = 500

co2Sensor = ADC(Pin(33))
co2Sensor.atten(ADC.ATTN_11DB)
MIN_CO2 = 400
MAX_CO2 = 10000

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

prev_weather = ""
while True:
  # Read weather (temperature and humidity)
  weatherSensor.measure() 
  temperature = weatherSensor.temperature()
  humidity = weatherSensor.humidity()
  
  # Read air quality sensor values and map to the correct range
  rawDust = dustSensor.read()
  mappedDust = (rawDust - MIN_ADC) * (MAX_PM2_5 - MIN_PM2_5) / (MAX_ADC - MIN_ADC) + MIN_PM2_5
  mappedDust = round(max(min(mappedDust, MAX_PM2_5), MIN_PM2_5), 1)

  rawCO2 = co2Sensor.read()
  mappedCO2 = (rawCO2 - MIN_ADC) * (MAX_CO2 - MIN_CO2) / (MAX_ADC - MIN_ADC) + MIN_CO2
  mappedCO2 = round(max(min(mappedCO2, MAX_CO2), MIN_CO2), 1)

  rawNO2 = no2Sensor.read()
  mappedNO2 = (rawNO2 - MIN_ADC) * (MAX_NO2 - MIN_NO2) / (MAX_ADC - MIN_ADC) + MIN_NO2
  mappedNO2 = round(max(min(mappedNO2, MAX_NO2), MIN_NO2), 1)

  message = ujson.dumps({
    "id": MQTT_CLIENT_ID,
    "temperature": temperature,
    "humidity": humidity,
    "dust": mappedDust,
    "co2": mappedCO2,
    "no2": mappedNO2
  })

  if message != prev_weather:
    print(message)
    client.publish(MQTT_TOPIC, message)
    prev_weather = message

    # Clear the OLED display before showing the new message
    oled.fill(0)

    # Display the MQTT content on the OLED screen
    oled.text("{}C".format(temperature), 0, 0)
    oled.text("{}%".format(humidity), 64, 0)
    oled.text("Dust: {}ug/m3".format(mappedDust), 0, 15)
    oled.text("CO2: {}ppm".format(mappedCO2), 0, 30)
    oled.text("NO2: {}ug/m3".format(mappedNO2), 0, 45)

    # Show the updated display
    oled.show()

  time.sleep(1)