"""
RAG Manager - Entry Point
Orchestrates the Flask application, defines API routes, and maps requests to logic modules.
"""
import os
import json
import subprocess
from flask import Flask, render_template_string, jsonify, request

# Import decoupled components
from monitor_ui import HTML_TEMPLATE
import monitor_logic

app = Flask(__name__)

# --- Configuration Management ---
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error loading config.json: {e}")
    config = {}

OLLAMA_API = config.get("ollama", {}).get("api_url", "http://127.0.0.1:11434")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, config=config)

@app.route('/api/data')
def api_data():
    llama_models = monitor_logic.get_llama_models(config)
    ollama_all, ollama_err, ollama_live = monitor_logic.get_ollama_status(OLLAMA_API)
    return jsonify({
        "llama_models": llama_models,
        "ollama_all": ollama_all,
        "ollama_error": ollama_err,
        "ollama_live": ollama_live
    })

@app.route('/api/ollama_service_start', methods=['POST'])
def ollama_service_start():
    try:
        monitor_logic.start_ollama_service()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/sys_<target>', methods=['POST'])
def sys_control(target):
    try:
        result = monitor_logic.run_sys_control(config, target)
        if target == 'rag_start':
            os.startfile("http://rag.local")
        return jsonify({"status": "ok", "msg": result})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/llama_stop', methods=['POST'])
def llama_stop():
    try:
        pid = request.json.get('target')
        subprocess.run(['taskkill', '/F', '/T', '/PID', str(pid)], check=True, capture_output=True)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/llama_start', methods=['POST'])
def llama_start():
    try:
        target = request.json.get('target')
        monitor_logic.run_llama_start(config, target)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/ollama_unload', methods=['POST'])
def ollama_unload():
    import requests
    try:
        requests.post(f'{OLLAMA_API}/api/generate', json={"model": request.json.get('model'), "keep_alive": 0}, timeout=10)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/ollama_load', methods=['POST'])
def ollama_load():
    import requests
    try:
        requests.post(f'{OLLAMA_API}/api/generate', json={"model": request.json.get('model'), "keep_alive": "10m"}, timeout=60)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": f"Ollama Timeout/Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting Web Controller at http://127.0.0.1:8899")
    # Bind to 0.0.0.0 to allow LAN access
    app.run(host='0.0.0.0', port=8899, debug=False)
