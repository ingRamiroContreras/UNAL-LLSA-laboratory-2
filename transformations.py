import os
# ─────────────────────────────────────────────
# T1 — Presentation
# ─────────────────────────────────────────────


def generate_web_interface(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'index.html'), 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head><title>{name} — Passenger Portal</title></head>
<body>
  <h1>ERTMS Passenger Portal</h1>
  <p>Component: {name}</p>
</body>
</html>
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM nginx:alpine\nCOPY index.html /usr/share/nginx/html/index.html\n")


def generate_operator_ui(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'dashboard.html'), 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head><title>{name} — Operator Dashboard</title></head>
<body>
  <h1>ERTMS Operator Dashboard</h1>
  <p>Component: {name}</p>
  <p>Status: Monitoring active routes...</p>
</body>
</html>
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM nginx:alpine\nCOPY dashboard.html /usr/share/nginx/html/index.html\n")


def generate_driver_ui(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'driver.html'), 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head><title>{name} — Driver Interface</title></head>
<body>
  <h1>ERTMS Driver Interface</h1>
  <p>Component: {name}</p>
  <p>Movement Authority: PENDING</p>
</body>
</html>
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM nginx:alpine\nCOPY driver.html /usr/share/nginx/html/index.html\n")


# ─────────────────────────────────────────────
# T2 — Communication
# ─────────────────────────────────────────────


def generate_api_gateway(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(f"""from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ROUTES = {{
    '/passengers': 'http://passengers_ms:80',
    '/routes': 'http://routes_ms:80',
    '/trains': 'http://trains_ms:80',
    '/tickets': 'http://tickets_ms:80',
    '/authority': 'http://mas:80',
}}


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(path):
    for prefix, target in ROUTES.items():
        full = '/' + path
        if full.startswith(prefix):
            rest = full[len(prefix):]
            url = target + (rest if rest else full)
            resp = requests.request(
                method=request.method,
                url=url,
                json=request.get_json(silent=True)
            )
            try:
                return jsonify(resp.json()), resp.status_code
            except Exception:
                return resp.text, resp.status_code
    return jsonify(error='Route not found'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install flask requests\nCMD [\"python\", \"app.py\"]\n")


def generate_gprs_modem(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'gprs_modem.py'), 'w') as f:
        f.write(f"""# GPRS Unit ({name}) — ERTMS T5
import time


def read_comm():
    return {{
        'communication_message': 'message comm',
        'communication_state': 'OK'
    }}


def send_to_ground(data):
    print(f'[GPRS {name}] Sending to EVC: {{data}}')


def receive_command(cmd):
    print(f'[GPRS {name}] Command received: {{cmd}}')
    if cmd.get('action') == 'BRAKE':
        send_command(cmd.get('message', 'unspecified'))


def send_command(message):
    print(f'[GPRS {name}] Sending command: {{message}}')


if __name__ == '__main__':
    while True:
        send_to_ground(read_comm())
        time.sleep(1)
""")


# ─────────────────────────────────────────────
# T3 — Logic
# ─────────────────────────────────────────────


def generate_microservice(name, database=None):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    db_host = database if database else f'{name}-db'
    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(f"""from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


def get_conn():
    import time
    for _ in range(10):
        try:
            return mysql.connector.connect(
                host='{db_host}',
                user='root',
                password='root',
                database='{db_host}'
            )
        except mysql.connector.Error:
            time.sleep(2)
    raise RuntimeError('Could not connect to database')


@app.route('/health')
def health():
    return jsonify(status='ok', service='{name}')


@app.route('/records')
def get_records():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records=rows)


@app.route('/records', methods=['POST'])
def create_record():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (name) VALUES (%s)",
        (data.get('name', 'unknown'),)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(status='created'), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install flask mysql-connector-python\nCMD [\"python\", \"app.py\"]\n")


def generate_authority_service(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(f"""from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify(status='ok', service='{name}')


@app.route('/authority', methods=['POST'])
def request_authority():
    data = request.json
    train_id = data.get('train_id')
    corridor = data.get('corridor')
    granted = True
    return jsonify(
        train_id=train_id,
        corridor=corridor,
        movement_authority='GRANTED' if granted else 'DENIED'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install flask\nCMD [\"python\", \"app.py\"]\n")


def generate_interlocking_service(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(f"""from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify(status='ok', service='{name}')


@app.route('/interlocking', methods=['POST'])
def request_interlocking():
    data = request.json
    train_id = data.get('train_id')
    corridor = data.get('corridor')
    granted = True
    return jsonify(
        train_id=train_id,
        corridor=corridor,
        movement_authority='GRANTED' if granted else 'DENIED'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install flask\nCMD [\"python\", \"app.py\"]\n")


def generate_radio_block_service(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'app.py'), 'w') as f:
        f.write(f"""from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify(status='ok', service='{name}')


@app.route('/radio_block', methods=['POST'])
def request_radio_block():
    data = request.json
    train_id = data.get('train_id')
    corridor = data.get('corridor')
    granted = True
    return jsonify(
        train_id=train_id,
        corridor=corridor,
        movement_authority='GRANTED' if granted else 'DENIED'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
""")
    with open(os.path.join(path, 'Dockerfile'), 'w') as f:
        f.write("FROM python:3.11-slim\nWORKDIR /app\nCOPY . .\nRUN pip install flask\nCMD [\"python\", \"app.py\"]\n")


# ─────────────────────────────────────────────
# T4 — Data
# ─────────────────────────────────────────────


def generate_database(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'init.sql'), 'w') as f:
        f.write("CREATE TABLE IF NOT EXISTS records (\n    id INT AUTO_INCREMENT PRIMARY KEY,\n    name VARCHAR(255) NOT NULL\n);\n")


def generate_data_lake(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'README.md'), 'w') as f:
        f.write(f"# {name} — ERTMS Data Lake\nAggregated operational and historical data lake.\n")
    with open(os.path.join(path, 'ingest.py'), 'w') as f:
        f.write(f"""# ERTMS Data Lake ingestion — {name}
import json
import datetime


def ingest(event: dict):
    record = {{
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'payload': event
    }}
    print(json.dumps(record))


if __name__ == '__main__':
    ingest({{'train_id': 'T-001', 'position': '48.8566,2.3522', 'speed_kmh': 220}})
""")


# ─────────────────────────────────────────────
# T5 — Physical
# ─────────────────────────────────────────────


def generate_onboard_unit(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'obu.py'), 'w') as f:
        f.write(f"""# Onboard Unit ({name}) — ERTMS T5
import time
import random


def read_sensors():
    return {{
        'speed_kmh': round(random.uniform(0, 300), 1),
        'position': f'{{random.uniform(40, 55):.4f}}, {{random.uniform(-5, 25):.4f}}'
    }}


def send_to_ground(data):
    print(f'[OBU {name}] Sending to ground: {{data}}')


def receive_command(cmd):
    print(f'[OBU {name}] Command: {{cmd}}')
    if cmd.get('action') == 'BRAKE':
        apply_brake(cmd.get('intensity', 1.0))


def apply_brake(intensity):
    print(f'[OBU {name}] Brake intensity {{intensity}}')


if __name__ == '__main__':
    while True:
        send_to_ground(read_sensors())
        time.sleep(1)
""")


def generate_sensor(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'sensor.py'), 'w') as f:
        f.write(f"""# Train Sensor ({name}) — ERTMS T5
import time
import random


def read():
    return {{
        'speed_kmh': round(random.uniform(0, 300), 1),
        'position': f'{{random.uniform(40, 55):.4f}}, {{random.uniform(-5, 25):.4f}}',
        'door_closed': random.choice([True, True, True, False]),
        'pantograph': 'UP'
    }}


if __name__ == '__main__':
    while True:
        print(f'[SENSOR {name}]', read())
        time.sleep(0.5)
""")


def generate_actuator(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'actuator.py'), 'w') as f:
        f.write(f"""# Brake Actuator ({name}) — ERTMS T5


def execute(command):
    action = command.get('action')
    intensity = command.get('intensity', 1.0)
    if action == 'BRAKE':
        print(f'[ACTUATOR {name}] Brake intensity {{intensity}}')
    elif action == 'RELEASE':
        print(f'[ACTUATOR {name}] Brake released')
    else:
        print(f'[ACTUATOR {name}] Unknown command: {{action}}')


if __name__ == '__main__':
    execute({{'action': 'BRAKE', 'intensity': 0.8}})
""")


def generate_balise(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'balise.py'), 'w') as f:
        f.write(f"""# Balise ({name}) — ERTMS T5
BALISE_ID = '{name}'
POSITION_M = 12500


def transmit():
    return {{
        'balise_id': BALISE_ID,
        'position_m': POSITION_M,
        'track_id': 'CORRIDOR-A',
        'signal': 'EUROBALISE-STM'
    }}


if __name__ == '__main__':
    print('[BALISE]', transmit())
""")


def generate_lineside_electronic(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'lineside_electronic.py'), 'w') as f:
        f.write(f"""# Lineside Electronic ({name}) — ERTMS T5
LINE_ID = '{name}'
IXL_STATE = 'CLEAR'


def transmit():
    return {{
        'line_id': LINE_ID,
        'ixl_state': IXL_STATE,
        'track_id': 'CORRIDOR-A',
        'signal': 'EUROBALISE-IDENTIFIER'
    }}


if __name__ == '__main__':
    print('[LINESIDE ELECTRONIC]', transmit())
""")


def generate_gps(name):
    path = f'skeleton/{name}'
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, 'gps.py'), 'w') as f:
        f.write(f"""# GPS ({name}) — ERTMS T5
GPS_ID = '{name}'
LATITUDE = '-121212121'
LONGITUDE = '-3434343434'


def transmit():
    return {{
        'gps_id': GPS_ID,
        'latitude': LATITUDE,
        'longitude': LONGITUDE
    }}


if __name__ == '__main__':
    print('[GPS]', transmit())
""")


# ─────────────────────────────────────────────
# docker-compose
# ─────────────────────────────────────────────
TIER_ORDER = {
    'data': 0,
    'physical': 1,
    'logic': 2,
    'communication': 3,
    'presentation': 4,
}


def generate_docker_compose(components):
    """components: { name: (tier, type) }"""
    path = 'skeleton/'
    os.makedirs(path, exist_ok=True)
    sorted_items = sorted(
        components.items(),
        key=lambda kv: TIER_ORDER.get(kv[1][0], 5)
    )
    db_names = [n for n, (t, ct) in sorted_items if ct == 'database']
    with open(os.path.join(path, 'docker-compose.yml'), 'w') as f:
        f.write("services:\n")
        http_port = 8000
        for name, (tier, ctype) in sorted_items:
            f.write(f"  {name}:\n")
            if ctype == 'database':
                f.write("    image: mysql:8\n")
                f.write("    environment:\n")
                f.write("      - MYSQL_ROOT_PASSWORD=root\n")
                f.write(f"      - MYSQL_DATABASE={name}\n")
                f.write("    volumes:\n")
                f.write(f"      - ./{name}/init.sql:/docker-entrypoint-initdb.d/init.sql\n")
            elif ctype == 'data_lake':
                f.write("    image: python:3.11-slim\n")
                f.write(f"    volumes:\n      - ./{name}:/app\n")
                f.write("    working_dir: /app\n")
                f.write("    command: python ingest.py\n")
            elif ctype in {'onboard_unit', 'sensor', 'actuator', 'balise',
                           'lineside_electronic', 'gps', 'gprs_modem'}:
                f.write("    image: python:3.11-slim\n")
                script = {
                    'onboard_unit': 'obu.py',
                    'sensor': 'sensor.py',
                    'actuator': 'actuator.py',
                    'balise': 'balise.py',
                    'lineside_electronic': 'lineside_electronic.py',
                    'gps': 'gps.py',
                    'gprs_modem': 'gprs_modem.py',
                }[ctype]
                f.write(f"    volumes:\n      - ./{name}:/app\n")
                f.write("    working_dir: /app\n")
                f.write(f"    command: python {script}\n")
            else:
                f.write(f"    build: ./{name}\n")
                f.write(f"    ports:\n      - '{http_port}:80'\n")
                http_port += 1
                if ctype == 'microservice' and db_names:
                    f.write("    depends_on:\n")
                    for db in db_names:
                        f.write(f"      - {db}\n")
        f.write("\nnetworks:\n  default:\n    driver: bridge\n")


# ─────────────────────────────────────────────
# Dispatcher
# ─────────────────────────────────────────────
GENERATORS = {
    'web_interface': generate_web_interface,
    'operator_ui': generate_operator_ui,
    'driver_ui': generate_driver_ui,
    'api_gateway': generate_api_gateway,
    'microservice': generate_microservice,
    'authority_service': generate_authority_service,
    'interlocking_service': generate_interlocking_service,
    'radio_block_service': generate_radio_block_service,
    'database': generate_database,
    'data_lake': generate_data_lake,
    'onboard_unit': generate_onboard_unit,
    'sensor': generate_sensor,
    'actuator': generate_actuator,
    'balise': generate_balise,
    'gprs_modem': generate_gprs_modem,
    'lineside_electronic': generate_lineside_electronic,
    'gps': generate_gps,
}


def apply_transformations(model):
    components = {}
    db_map = {}
    _tier_by_class = {
        'PresentationComponent': 'presentation',
        'CommunicationComponent': 'communication',
        'LogicComponent': 'logic',
        'DataComponent': 'data',
        'PhysicalComponent': 'physical',
    }
    for e in model.elements:
        tier = _tier_by_class.get(e.__class__.__name__)
        if tier is not None:
            components[e.name] = (tier, e.type)
    db_names = [n for n, (t, ct) in components.items() if ct == 'database']
    for name, (tier, ctype) in components.items():
        if ctype == 'microservice':
            for db in db_names:
                if db.replace('-db', '').replace('_db', '') in name:
                    db_map[name] = db
                    break
    for name, (tier, ctype) in components.items():
        gen = GENERATORS.get(ctype)
        if gen:
            if ctype == 'microservice':
                gen(name, database=db_map.get(name))
            else:
                gen(name)
    generate_docker_compose(components)
