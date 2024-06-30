from flask import Flask, request, jsonify

app = Flask(__name__)

# Словарь для хранения команд для клиентов
commands = {}
# Словарь для хранения результатов от клиентов
results = {}

@app.route('/send_result', methods=['POST'])
def send_result():
    data = request.json
    client_id = data['client_id']
    result = data['result']
    
    if client_id in results:
        results[client_id].append(result)
    else:
        results[client_id] = [result]
    
    return jsonify({"message": "Result received"}), 200

@app.route('/get_command', methods=['GET'])
def get_command():
    client_id = request.args.get('client_id')
    
    if client_id in commands and commands[client_id]:
        command = commands[client_id].pop(0)
        return jsonify({"command": command}), 200
    else:
        return jsonify({"command": ""}), 200

@app.route('/admin/send_command', methods=['POST'])
def admin_send_command():
    data = request.json
    client_id = data['client_id']
    command = data['command']
    
    if client_id in commands:
        commands[client_id].append(command)
    else:
        commands[client_id] = [command]
    
    return jsonify({"message": "Command sent"}), 200

@app.route('/admin/get_results', methods=['GET'])
def admin_get_results():
    client_id = request.args.get('client_id')
    
    if client_id in results:
        return jsonify({"results": results[client_id]}), 200
    else:
        return jsonify({"results": []}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
