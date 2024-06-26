import time
import dht
from machine import Pin
import network
import urequests

# Configuração WiFi
ssid = 'Wifiteste_5G'
password = '12345678'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

# Configuração do Sensor DHT11
sensor = dht.DHT11(Pin(14))

# URL da API do Backend
url = "/Backend/services"

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        # Enviar dados para o servidor
        data = {
            "description": f"Temp: {temp}C Hum: {hum}%",
            "status": "active"
        }
        
        response = urequests.post(url, json=data)
        print(response.text)
        
    except OSError as e:
        print('Failed to read sensor.')
    
    time.sleep(60)
