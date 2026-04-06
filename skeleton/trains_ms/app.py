from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


def get_conn():
    import time
    for _ in range(10):
        try:
            return mysql.connector.connect(
                host='trains_db',
                user='root',
                password='root',
                database='trains_db'
            )
        except mysql.connector.Error:
            time.sleep(2)
    raise RuntimeError('Could not connect to database')


@app.route('/health')
def health():
    return jsonify(status='ok', service='trains_ms')


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
