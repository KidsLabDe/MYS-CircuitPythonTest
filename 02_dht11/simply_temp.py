import board
import adafruit_dht
import time

# Initialisiere den DHT11-Sensor
dht_device = adafruit_dht.DHT11(board.GP17)

while True:
    try:
        # Lese Temperatur und Luftfeuchtigkeit
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        
        print(f"Temperatur: {temperature:.1f} C, Luftfeuchtigkeit: {humidity:.1f} %")
    except RuntimeError as error:
        # Fehler beim Lesen des Sensors ignorieren
        print(f"Fehler beim Lesen des Sensors: {error.args[0]}")
    
    time.sleep(2.0)