"""
Monitor Logic Module
Handles system process monitoring, model filesystem scanning, and direct service controls.
This module is decoupled from the web framework for better portability.
"""
import psutil
import requests
import re
import os
import subprocess
import time

def format_uptime(seconds):
    """Converts a duration in seconds to a human-readable string (e.g., 2h 30m)."""
    if seconds < 60: return f"{int(seconds)}s"
    m, s = divmod(seconds, 60)
    if m < 60: return f"{int(m)}m {int(s)}s"
    h, m = divmod(m, 60)
    return f"{int(h)}h {int(m)}m"

def is_ollama_service_running():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and ('ollama.exe' in proc.info['name'].lower() or 'ollama app.exe' in proc.info['name'].lower()):
                return True
        except: pass
    return False

def start_ollama_service():
    # Launches Ollama serve in the background
    DETACHED_PROCESS = 0x00000008
    subprocess.Popen(["ollama", "serve"], creationflags=DETACHED_PROCESS)
    return True

def get_llama_models(config):
    # 1. Scan disk for available .gguf models
    model_dir = config.get("paths", {}).get("model_dir", "")
    available_files = []
    if os.path.isdir(model_dir):
        available_files = [f for f in os.listdir(model_dir) if f.lower().endswith('.gguf')]
    
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
        l_fname = fname.lower()
        
        for s_name, s_cfg in config.get("services", {}).items():
            if s_cfg.get("model_file", "").lower() == l_fname:
                service_type = s_name
                port = s_cfg.get("port")
                caps.append(s_name.capitalize())
        
        if not caps:
            if "rerank" in l_fname: caps.append("Rerank")
            elif "embed" in l_fname or "m3" in l_fname: caps.append("Embedding")
            else: caps.append("Chat")

        full_path = os.path.join(model_dir, fname)
        size_mb = 0
        if os.path.exists(full_path):
            size_mb = round(os.path.getsize(full_path) / (1024 * 1024), 2)

        if active_proc:
            merged.append({
                "name": fname,
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
                "running": False,
                "path": full_path,
                "size_mb": size_mb,
                "service_type": service_type,
                "port": port,
                "caps": caps
            })
            
    return sorted(merged, key=lambda x: (not x['running'], x['name']))

def get_ollama_status(api_url):
    try:
        r_ps = requests.get(f'{api_url}/api/ps', timeout=2)
        r_ps.raise_for_status()
        active_dict = {
            m.get('name'): {
                "total_mb": m.get('size', 0) / (1024 * 1024),
                "vram_mb": m.get('size_vram', 0) / (1024 * 1024)
            } for m in r_ps.json().get('models', [])
        }
            
        r_tags = requests.get(f'{api_url}/api/tags', timeout=2)
        r_tags.raise_for_status()
        
        merged = []
        for m in r_tags.json().get('models', []):
            name = m.get('name')
            l_name = name.lower()
            is_active = name in active_dict
            
            caps = []
            if "embed" in l_name or "m3" in l_name: caps.append("Embedding")
            else: caps.append("Chat")

            merged.append({
                "name": name,
                "disk_size_mb": round(m.get('size', 0) / (1024 * 1024), 2),
                "running": is_active,
                "total_mb": round(active_dict[name]['total_mb'], 2) if is_active else 0,
                "vram_mb": round(active_dict[name]['vram_mb'], 2) if is_active else 0,
                "port": 11434,
                "caps": caps
            })
        return sorted(merged, key=lambda x: (not x['running'], x['name'])), None, is_ollama_service_running()
    except Exception as e:
        return [], f"Cannot connect to Ollama: {str(e)}", is_ollama_service_running()

def run_llama_start(config, target):
    service_cfg = config.get("services", {}).get(target)
    if not service_cfg:
        raise ValueError(f"Config for {target} not found")
        
    model_dir = config.get("paths", {}).get("model_dir", "")
    llama_exe_cfg = config.get("paths", {}).get("llama_server", "llama-server.exe")
    
    if os.path.isabs(llama_exe_cfg) and os.path.exists(llama_exe_cfg):
        llama_exe = llama_exe_cfg
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate = os.path.join(project_root, "llamacpp", os.path.basename(llama_exe_cfg))
        if os.path.exists(candidate):
            llama_exe = candidate
        else:
            llama_exe = llama_exe_cfg

    model_path = os.path.join(model_dir, service_cfg["model_file"])
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    cmd = [
        llama_exe, 
        "-m", model_path,
        "--host", service_cfg["host"],
        "--port", str(service_cfg["port"]),
        "-t", str(service_cfg["threads"])
    ] + service_cfg.get("extra_args", [])
    
    DETACHED_PROCESS = 0x00000008
    subprocess.Popen(cmd, creationflags=DETACHED_PROCESS, cwd=os.path.dirname(llama_exe) if os.path.isabs(llama_exe) else None)
    return True

def run_sys_control(config, target):
    rag_dir = config.get("docker", {}).get("ragflow_dir")
    nginx_dir = config.get("docker", {}).get("nginx_pm_dir")
    
    if not rag_dir or not nginx_dir:
        raise ValueError("Docker paths not configured in config.json")
        
    if target == 'rag_start':
        subprocess.run(["docker-compose", "down"], cwd=rag_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["docker-compose", "down"], cwd=nginx_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        subprocess.run(["docker-compose", "up", "-d"], cwd=nginx_dir, check=True)
        subprocess.run(["docker-compose", "up", "-d"], cwd=rag_dir, check=True)
        subprocess.run(["docker-compose", "up", "-d"], cwd=nginx_dir, check=True)
        return "Started"
        
    elif target == 'rag_stop':
        subprocess.run(['taskkill', '/F', '/IM', 'llama-server.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["docker-compose", "down"], cwd=rag_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["docker-compose", "down"], cwd=nginx_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Stopped"
    
    return "Unknown action"
