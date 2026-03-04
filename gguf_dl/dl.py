import os
import sys
import yaml

try:
    from modelscope.hub.file_download import model_file_download
except ImportError:
    print("请先安装依赖: pip install modelscope")
    sys.exit(1)

def main():
    yaml_path = os.path.join(os.path.dirname(__file__), "download_list.yaml")
    
    # 向后兼容 JSON
    json_path = os.path.join(os.path.dirname(__file__), "download_list.json")
    
    data = {}
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
    elif os.path.exists(json_path):
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print(f"[X] 未找到配置文件: {yaml_path}")
        return

    # 支持直接作为列表，或作为对象（带有全局 dir）
    tasks = data.get('models', []) if isinstance(data, dict) else data
    base_dir = data.get('dir', r"D:\oLLM\alone_models") if isinstance(data, dict) else r"D:\oLLM\alone_models"

    for task in tasks:
        file_name = task['file']
        model_id = task['model_id']
        save_dir = task.get('dir', base_dir)
        
        os.makedirs(save_dir, exist_ok=True)
        print(f"\n[*] 正在下载: {file_name} (来自 {model_id})")

        try:
            downloaded = model_file_download(model_id=model_id, file_path=file_name, local_dir=save_dir)
            print(f"[√] 下载成功: {downloaded}")
        except Exception as e:
            print(f"[X] 无法下载 '{file_name}'。请检查模型ID和名字。错误: {e}")

if __name__ == "__main__":
    main()
