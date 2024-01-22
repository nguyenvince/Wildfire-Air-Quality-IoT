# Wildfire Detection System
## Leveraging IOT to monitor, analyse, visualize and disseminate information about Air Quality anomalies for detecting wildfires

Project report can be found [here](https://docs.google.com/document/d/1phrDKMYYtAXYEQdH9UnePnNoacv5Urh0gi-Fay7SNWg/edit?usp=sharing).

Steps to run the project:

1. Clone the repository
2. ```docker compose build```
3. ```docker compose up```
4. To visit the Grafana port, visit [http://localhost:3000/dashboards](http://localhost:3000/dashboards) and click on 'wildfire'. Username: admin, password: admin
5. You can visit the Wokwi project [here](https://wokwi.com/projects/383803266172777473) to simulate other sensors by changing the string ```MQTT_CLIENT_ID``` and restarting the Wokwi simulation (e.g., changing the string value to 'wokwi_sensor2')
6. To visit the node-red port, visit [http://localhost:1880](http://localhost:1880)
7. To visit the InfluxDB port, visit [http://localhost:8086/](http://localhost:8086/). Username: admin, password: password.
8. Once you are done, run ```docker compose down```
