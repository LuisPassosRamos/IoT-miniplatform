import paho.mqtt.client as mqtt
import time
import json
import random

MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "iot/sensors"
CLIENT_ID = f"python-mqtt-sensor-{random.randint(0, 1000)}"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conectado ao Broker MQTT com sucesso!")
    else:
        print(f"Falha na conexão, código de retorno: {rc}\n")

def run_sensor():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    
    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    except ConnectionRefusedError:
        print("Erro: Conexão recusada. O broker MQTT (via Docker) está em execução?")
        return

    client.loop_start()
    print(f"Sensor simulado '{CLIENT_ID}' iniciado. Publicando no tópico '{MQTT_TOPIC}'.")
    print("Pressione Ctrl+C para parar.")

    try:
        while True:
            temperature = round(random.uniform(18.0, 28.0), 2)
            payload = {
                "sensor_id": CLIENT_ID,
                "type": "temperature",
                "value": temperature,
                "unit": "Celsius",
                "timestamp": time.time()
            }
            msg = json.dumps(payload)
            result = client.publish(MQTT_TOPIC, msg, qos=0)
            
            if result.rc == 0:
                print(f"Enviado `{msg}` para o tópico `{MQTT_TOPIC}`")
            else:
                print(f"Falha ao enviar mensagem para o tópico {MQTT_TOPIC}")

            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSensor parado pelo usuário.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Cliente MQTT desconectado.")

if __name__ == '__main__':
    run_sensor()