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
def load_config():
    CONFIG_YAML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    CONFIG_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

    config = {}
    if os.path.exists(CONFIG_YAML):
        import yaml
        try:
            with open(CONFIG_YAML, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config.yaml: {e}")
    elif os.path.exists(CONFIG_JSON):
        try:
            with open(CONFIG_JSON, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading config.json: {e}")
    return config

@app.route('/')
def index():
    config = load_config()
    return render_template_string(HTML_TEMPLATE, config=config)

@app.route('/api/data')
def api_data():
    config = load_config()
    ollama_api = config.get("ollama", {}).get("api_url", "http://127.0.0.1:11434")
    llama_models = monitor_logic.get_llama_models(config)
    ollama_all, ollama_err, ollama_live = monitor_logic.get_ollama_status(ollama_api)
    return jsonify({
        "llama_models": llama_models,
        "ollama_all": ollama_all,
        "ollama_error": ollama_err,
        "ollama_live": ollama_live
    })

@app.route('/api/ollama_service_start', methods=['POST'])
def ollama_service_start():
    config = load_config()
    try:
        monitor_logic.start_ollama_service(config)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/sys_<target>', methods=['POST'])
def sys_control(target):
    config = load_config()
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
    config = load_config()
    try:
        target = request.json.get('target')
        monitor_logic.run_llama_start(config, target)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/ollama_unload', methods=['POST'])
def ollama_unload():
    config = load_config()
    ollama_api = config.get("ollama", {}).get("api_url", "http://127.0.0.1:11434")
    import requests
    try:
        requests.post(f'{ollama_api}/api/generate', json={"model": request.json.get('model'), "keep_alive": 0}, timeout=10)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/ollama_load', methods=['POST'])
def ollama_load():
    config = load_config()
    ollama_api = config.get("ollama", {}).get("api_url", "http://127.0.0.1:11434")
    import requests
    try:
        requests.post(f'{ollama_api}/api/generate', json={"model": request.json.get('model'), "keep_alive": "10m"}, timeout=60)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "msg": f"Ollama Timeout/Error: {str(e)}"}), 500

@app.route('/api/gguf_download', methods=['POST'])
def gguf_download():
    import yaml
    try:
        data = request.json
        model_id = data.get('model_id')
        file_name = data.get('file')
        save_dir = data.get('dir')

        if not model_id or not file_name:
            return jsonify({"status": "error", "msg": "Missing model_id or file"}), 400

        yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gguf_dl", "download_list.yaml")
        
        # Create a clean YAML structure
        yaml_data = {
            "dir": save_dir if save_dir else r"D:\oLLM\alone_models",
            "models": [
                {
                    "model_id": model_id,
                    "file": file_name
                }
            ]
        }
        
        # Write to YAML with comments
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write("# 自动生成的下载配置 (来自 Web 监控界面)\n")
            f.write("# 支持单模型对象，或模型列表\n\n")
            yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        # Launch the download script in a new visible CMD window
        dl_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gguf_dl", "dl.py")
        venv_python = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".venv", "Scripts", "python.exe")
        
        # Use 'start' to open a new command prompt window
        subprocess.Popen(f'start "ModelScope Downloader" cmd /c "{venv_python} {dl_script} & pause"', shell=True)
        
        return jsonify({"status": "ok", "msg": "下载任务已在新的命令行窗口中启动！"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    print("Starting Web Controller at http://127.0.0.1:8899")
    # Bind to 0.0.0.0 to allow LAN access
    app.run(host='0.0.0.0', port=8899, debug=False)
