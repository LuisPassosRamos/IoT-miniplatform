from flask import Flask, jsonify, request
from flask_mqtt import Mqtt
from functools import wraps
from collections import deque
import json
import time

# --- CONFIGURAÇÃO ---
app = Flask(__name__)

# Configuração do Broker MQTT
app.config = 'mqtt-broker'  # Nome do serviço no docker-compose
app.config = 1883
app.config = ''
app.config = ''
app.config = 5
app.config = False

MQTT_TOPIC = "iot/sensors"
SECRET_TOKEN = "my-super-secret-iot-token"

# Armazenamento em memória para as últimas 100 leituras
sensor_data = deque(maxlen=100)

mqtt_client = Mqtt(app)

# --- LÓGICA DE AUTENTICAÇÃO ---
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"message": "Token malformado!"}), 401
        
        if not token:
            return jsonify({"message": "Token é obrigatório!"}), 401
        
        if token!= SECRET_TOKEN:
            return jsonify({"message": "Token inválido!"}), 401

        return f(*args, **kwargs)
    return decorated_function

# --- LÓGICA MQTT ---
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Conectado ao Broker MQTT!')
       mqtt_client.subscribe(MQTT_TOPIC)
   else:
       print('Falha na conexão, código de retorno: %d\n', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(f'Recebida mensagem do tópico "{message.topic}": {payload}')
    try:
        data = json.loads(payload)
        sensor_data.append(data)
    except json.JSONDecodeError:
        print("Erro: Payload recebido não é um JSON válido.")

# --- LÓGICA DE ANÁLISE ---
def calculate_moving_average(data, window_size=5):
    temperatures = [d['value'] for d in data if d.get('type') == 'temperature']
    if len(temperatures) < window_size:
        return None
    return round(sum(temperatures[-window_size:]) / window_size, 2)

def check_consecutive_alerts(data, threshold=25.0, count=2):
    temperatures = [d['value'] for d in data if d.get('type') == 'temperature']
    if len(temperatures) < count:
        return False
    return all(reading > threshold for reading in temperatures[-count:])

# --- ENDPOINTS DA API ---
@app.route('/api/data')
@token_required
def get_sensor_data():
    data_list = list(sensor_data)
    moving_avg = calculate_moving_average(data_list)
    alert_status = check_consecutive_alerts(data_list)
    
    response = {
        "sensor_readings": data_list,
        "analysis": {
            "temperature_moving_average": moving_avg,
            "high_temp_alert": alert_status
        }
    }
    return jsonify(response)

@app.route('/')
def index():
    return "Servidor da API está no ar. Use o endpoint /api/data para obter os dados."

if __name__ == '__main__':
    # O host '0.0.0.0' é crucial para rodar dentro do Docker
    app.run(host='0.0.0.0', port=5001)