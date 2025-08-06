# IoT-miniplatform

Este projeto é uma miniplataforma web para monitoramento de dados de sensores IoT, construído com Python (Flask), MQTT e Docker, conforme os requisitos da atividade.

## Como Executar o Projeto

1.  **Pré-requisitos:** Docker e Docker Compose instalados.
2.  **Iniciar a Infraestrutura:** Na raiz do projeto, execute o comando:
    ```bash
    docker-compose up --build
    ```
3.  **Iniciar o Sensor:** Em um novo terminal, na raiz do projeto, execute:
    ```bash
    python sensor/sensor.py
    ```
4.  **Acessar o Frontend:** Abra o arquivo `frontend/index.html` no seu navegador.

## Documentação da API

A API segue os padrões REST e utiliza autenticação via Bearer Token.

### Endpoint Principal

-   **GET /api/data**
    -   Retorna as últimas 100 leituras dos sensores e uma análise contendo a média móvel de temperatura e um status de alerta.
    -   **Autenticação:** Requer um Bearer Token no cabeçalho `Authorization`.

#### Exemplo de Requisição (usando curl)

```bash
curl -X GET http://localhost:5001/api/data \
  -H "Authorization: Bearer my-super-secret-iot-token"
```

#### Exemplo de Resposta JSON

```json
{
  "analysis": {
    "high_temp_alert": false,
    "temperature_moving_average": 24.58
  },
  "sensor_readings": [
    {
      "sensor_id": "python-mqtt-sensor-451",
      "timestamp": 1678886400.123,
      "type": "temperature",
      "unit": "Celsius",
      "value": 24.1
    },
    {
      "sensor_id": "python-mqtt-sensor-451",
      "timestamp": 1678886405.456,
      "type": "temperature",
      "unit": "Celsius",
      "value": 25.0
    }
  ]
}
```