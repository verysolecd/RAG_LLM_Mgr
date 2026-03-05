import os
import psutil
import re
import time
import subprocess

def is_ollama_service_running():
    # Helper to check if ollama process is active
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info.get('name')
            if name and ('ollama.exe' in name.lower() or 'ollama app' in name.lower()):
                return True
        except: pass
    return False

def start_ollama_service(config):
    # Launches Ollama serve in the background
    install_dir = config.get("paths", {}).get("ollama_dir", "")
    ollama_bin = os.path.join(install_dir, "ollama.exe") if install_dir else "ollama"
    
    DETACHED_PROCESS = 0x00000008
    subprocess.Popen([ollama_bin, "serve"], creationflags=DETACHED_PROCESS)
    return True

def get_llama_models(config):
    # 1. Scan disk for available .gguf models
    model_dir = config.get("paths", {}).get("model_dir", "")
    available_files = []
    if os.path.isdir(model_dir):
        available_files = [f for f in os.listdir(model_dir) if f.lower().endswith('.gguf')]
    
    print(f"DEBUG: model_dir = {model_dir}")
    print(f"DEBUG: available_files = {available_files}")
    print(f"DEBUG: config services found = {list(config.get('services', {}).keys())}")

    # 2. Get running llama-server processes
    running_instances = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info', 'create_time']):
        try:
            if proc.info['name'] and 'llama-server' in proc.info['name'].lower():
                cmd_str = ' '.join(proc.info.get('cmdline', []))
                match = re.search(r'-m\s+["\']?([^"\']+\.gguf)["\']?', cmd_str)
                if match:
                    path = match.group(1)
                    mem = proc.info['memory_info']
                    ram_mb = round(mem.rss / (1024 * 1024), 2)
                    vms_mb = round(mem.vms / (1024 * 1024), 2)
                    running_instances.append({
                        "filename": os.path.basename(path),
                        "pid": proc.info['pid'],
                        "ram_mb": ram_mb,
                        "vram_mb": max(0, vms_mb - ram_mb),
                        "uptime": format_uptime(time.time() - proc.info['create_time']),
                        "path": path
                    })
        except: pass

    # 3. Merge: One item per file, link running data if active
    merged = []
    for fname in available_files:
        active_proc = next((p for p in running_instances if p['filename'].lower() == fname.lower()), None)
        
        service_type = None
        port = None
        caps = []
        alias = None
        l_fname = fname.lower().strip()
        
        for s_name, s_cfg in config.get("services", {}).items():
            if not s_cfg: continue
            cfg_file = s_cfg.get("model_file", "").strip().lower()
            print(f"DEBUG: Comparing '{l_fname}' with config file '{cfg_file}' (Source service: {s_name})")
            if cfg_file == l_fname:
                service_type = s_name
                port = s_cfg.get("port")
                alias = s_cfg.get("alias") or s_name
                print(f"  -> SUCCESS: Match found for {s_name}, alias={alias}")
                # Use explicit capabilities list or fallback to service name
                if "capabilities" in s_cfg:
                    caps.extend(s_cfg["capabilities"])
                else:
                    caps.append(s_name.capitalize())
        
        if not caps:
            if "rerank" in l_fname: caps.append("Rerank")
            elif "embed" in l_fname or "m3" in l_fname: caps.append("Embedding")
            else: caps.append("Chat")
        
        # Unique capabilities
        caps = list(dict.fromkeys(caps))
        
        # Fallback alias: filename without extension
        if not alias:
            alias = fname.rsplit('.', 1)[0]

        full_path = os.path.join(model_dir, fname)
        size_mb = 0
        if os.path.exists(full_path):
            size_mb = round(os.path.getsize(full_path) / (1024 * 1024), 2)

        if active_proc:
            merged.append({
                "name": fname,
                "alias": alias,
                "running": True,
                "pid": active_proc['pid'],
                "ram_mb": active_proc['ram_mb'],
                "vram_mb": active_proc['vram_mb'],
                "uptime": active_proc['uptime'],
                "path": active_proc['path'],
                "size_mb": size_mb,
                "service_type": service_type,
                "port": port,
                "caps": caps
            })
        else:
            merged.append({
                "name": fname,
                "alias": alias,
                "running": False,
                "path": full_path,
                "size_mb": size_mb,
                "service_type": service_type,
                "port": port,
                "caps": caps
            })
            
    return sorted(merged, key=lambda x: (not x['running'], x['name']))

def format_uptime(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    if minutes > 0:
        return f"{minutes}m {secs}s"
    return f"{secs}s"

def get_ollama_status(api_url):
    import requests
    try:
        # Check active models
        res_ps = requests.get(f"{api_url}/api/ps", timeout=2)
        running_names = []
        running_data = {}
        if res_ps.ok:
            for m in res_ps.json().get("models", []):
                name = m.get("name")
                running_names.append(name)
                running_data[name] = {
                    "vram_mb": round(m.get("size_vram", 0) / (1024*1024), 2),
                    "total_mb": round(m.get("size", 0) / (1024*1024), 2)
                }

        # Check all models
        res_tags = requests.get(f"{api_url}/api/tags", timeout=2)
        all_models = []
        if res_tags.ok:
            for m in res_tags.json().get("models", []):
                name = m.get("name")
                is_running = name in running_names
                all_models.append({
                    "name": name,
                    "running": is_running,
                    "vram_mb": running_data.get(name, {}).get("vram_mb", 0) if is_running else 0,
                    "total_mb": running_data.get(name, {}).get("total_mb", 0) if is_running else 0,
                    "disk_size_mb": round(m.get("size", 0) / (1024*1024), 2),
                    "caps": ["Chat"] # Ollama models are typically chat
                })
        
        is_live = is_ollama_service_running()
        return all_models, None, is_live
    except Exception as e:
        return [], str(e), is_ollama_service_running()

def run_sys_control(config, target):
    import os
    import subprocess
    
    if target == 'rag_start':
        docker_dir = config.get("docker", {}).get("ragflow_dir", "")
        if not os.path.isdir(docker_dir): raise Exception(f"Invalid RAGFlow directory: {docker_dir}")
        subprocess.Popen(["docker-compose", "up", "-d"], cwd=docker_dir, shell=True)
        return "RAGFlow clusters starting..."
    
    if target == 'rag_stop':
        docker_dir = config.get("docker", {}).get("ragflow_dir", "")
        if not os.path.isdir(docker_dir): raise Exception(f"Invalid RAGFlow directory: {docker_dir}")
        subprocess.Popen(["docker-compose", "stop"], cwd=docker_dir, shell=True)
        return "RAGFlow clusters stopping..."

    if target == 'npm_start':
        npm_dir = config.get("docker", {}).get("nginx_pm_dir", "")
        if not os.path.isdir(npm_dir): raise Exception(f"Invalid NginxPM directory: {npm_dir}")
        subprocess.Popen(["docker-compose", "up", "-d"], cwd=npm_dir, shell=True)
        return "Nginx Proxy Manager starting..."
        
    if target == 'npm_stop':
        npm_dir = config.get("docker", {}).get("nginx_pm_dir", "")
        if not os.path.isdir(npm_dir): raise Exception(f"Invalid NginxPM directory: {npm_dir}")
        subprocess.Popen(["docker-compose", "stop"], cwd=npm_dir, shell=True)
        return "Nginx Proxy Manager stopping..."

    return "Unknown command"

def run_llama_start(config, service_id):
    import subprocess
    import os
    
    s_cfg = config.get("services", {}).get(service_id)
    if not s_cfg: raise Exception(f"Service configuration not found: {service_id}")
    
    model_dir = config.get("paths", {}).get("model_dir", "")
    model_path = os.path.join(model_dir, s_cfg.get("model_file"))
    llama_bin = config.get("paths", {}).get("llama_server", "llama-server.exe")
    
    alias = s_cfg.get("alias") or service_id
    cmd = [
        llama_bin,
        "-m", model_path,
        "--alias", alias,
        "--host", s_cfg.get("host", "0.0.0.0"),
        "--port", str(s_cfg.get("port", 8080)),
        "-t", str(s_cfg.get("threads", 4))
    ]
    
    # Add extra args if any
    extra = s_cfg.get("extra_args", [])
    cmd.extend(extra)
    
    # Use Windows Terminal (wt) to open in a new tab within the existing window
    # -w 0 targets the first (current) Windows Terminal window
    cmd_str = ' '.join([f'"{c}"' if ' ' in c else c for c in cmd])
    full_cmd = f'wt -w 0 new-tab --title "{service_id}" cmd /k {cmd_str}'
    print(f"Launching: {full_cmd}")
    subprocess.Popen(full_cmd, shell=True)
    return True
