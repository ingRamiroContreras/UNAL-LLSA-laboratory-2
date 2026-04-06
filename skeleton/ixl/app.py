from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify(status='ok', service='ixl')


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
