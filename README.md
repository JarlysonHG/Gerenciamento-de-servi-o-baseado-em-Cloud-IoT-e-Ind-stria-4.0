### 1. Sistema de Gerenciamento de Serviços (Backend em Python)

Interface inicial (basica)
<div align="center">
<img src="https://raw.githubusercontent.com/JarlysonHG/Gerenciamento-de-servi-o-baseado-em-Cloud-IoT-e-Ind-stria-4.0/main/Img/ezgif-1-16c56df9b1.gif" width="400px" />
</div>
<div align="center">
<img src="https://raw.githubusercontent.com/JarlysonHG/Gerenciamento-de-servi-o-baseado-em-Cloud-IoT-e-Ind-stria-4.0/main/Img/ezgif-1-3f3418ccd6.gif" width="400px" />
</div>


#### a) Configuração do Servidor Backend

Para o backend, usaremos o framework Flask para criar uma API que permita gerenciar os serviços da oficina. 

**Instale o Flask:**
```bash
pip install flask
```

**Código do Servidor Backend:**

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workshop.db'
db = SQLAlchemy(app)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

@app.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services])

@app.route('/services', methods=['POST'])
def add_service():
    data = request.get_json()
    new_service = Service(description=data['description'], status=data['status'])
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_dict()), 201

@app.route('/services/<int:id>', methods=['PUT'])
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    service.description = data.get('description', service.description)
    service.status = data.get('status', service.status)
    db.session.commit()
    return jsonify(service.to_dict())

@app.route('/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

### 2. Sistema de Sensores IoT (Microcontroladores com Python)

Utilizaremos a placa ESP32 com MicroPython para simular o monitoramento de estoque de peças.

**Configuração do Ambiente MicroPython:**

1. Flash o firmware MicroPython na ESP32.
2. Conecte-se à placa usando uma ferramenta como o Thonny IDE.

**Código do Sensor IoT:**

```python
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
url = "http://<YOUR_BACKEND_IP>:5000/services"

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
```

### 3. Plataforma de Cloud (Servidor e Banco de Dados)

Para o banco de dados e servidor, podemos usar um servidor com Flask (já configurado acima) e SQLite para armazenamento local. Para uma implementação mais robusta, considere usar um banco de dados como PostgreSQL.

### 4. Dashboard de Gerenciamento (Frontend)

Para o frontend, usaremos HTML, CSS e JavaScript para criar um painel de gerenciamento simples.

**Estrutura do Dashboard (index.html):**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oficina de Moto Peças</title>
    <link rel="stylesheet" href="styles.css">
    <script src="script.js"></script>
    <style>
        body { font-family: Arial, sans-serif; }
        table { width: 100%; border-collapse: collapse; }
        table, th, td { border: 1px solid black; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="container">
    <h1>Gerenciamento de Serviços da Oficina</h1>
<section>
    <h2>Adicionar Serviço</h2>
    <form id="add-service-form">
        <div class="form-group">
            <label for="description">Descrição:</label>
            <input type="text" id="description" name="description" required>
        </div>
        <div class="form-group">
            <label for="status">Status:</label>
            <select id="status" name="status" required>
                <option value="Pendente">Pendente</option>
                <option value="Em Andamento">Em Andamento</option>
                <option value="Concluído">Concluído</option>
            </select>
        </div>
        <button type="submit">Adicionar</button>
    </form>
</section>
<section>
    <table id="services-table">
        <thead>
        <tr>
            <th>ID</th>
            <th>Descrição</th>
            <th>Status</th>
            <th>Criado em</th>
        </tr>
    </thead>
    <tbody></tbody>
    </table>
</section>
    <script>
        const servicesTable = document.getElementById('services-table');
        const addServiceForm = document.getElementById('add-service-form');

        function fetchServices() {
            fetch('backend/services')
                .then(response => response.json())
                .then(data => {
                    data.forEach(service => {
                        const row = servicesTable.insertRow();
                        row.insertCell(0).innerText = service.id;
                        row.insertCell(1).innerText = service.description;
                        row.insertCell(2).innerText = service.status;
                        row.insertCell(3).innerText = service.created_at;
                    });
                });
        }

        addServiceForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(addServiceForm);
            const data = {
                description: formData.get('description'),
                status: formData.get('status')
            };

            fetch('http://<YOUR_BACKEND_IP>:5000/services', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(service => {
                const row = servicesTable.insertRow();
                row.insertCell(0).innerText = service.id;
                row.insertCell(1).innerText = service.description;
                row.insertCell(2).innerText = service.status;
                row.insertCell(3).innerText = service.created_at;
                addServiceForm.reset();
            });
        });

        window.onload = fetchServices;
    </script>
</div>
</body>
</html>

```

### Conclusão
Com este código, temos um projeto completo que inclui um sistema de gerenciamento de serviços usando Python, integração com sensores IoT para monitoramento em tempo real e um frontend simples para visualização e gerenciamento dos serviços da oficina. Este projeto pode ser expandido e melhorado com mais funcionalidades, como notificações, relatórios avançados, e integração com outros sistemas.
