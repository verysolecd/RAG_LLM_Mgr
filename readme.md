# RAG Manager - macOS Style AI Controller 🚀

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English Overview

**RAG Manager** is a premium, macOS-styled web interface designed to manage local AI inference engines. It provides real-time telemetry, service control, and model library management for both **LLaMA.cpp** and **Ollama**.

### ✨ Features
- 🍎 **macOS Aesthetics**: Beautiful glassmorphism UI with dark mode support.
- ⬇️ **GGUF Downloader**: Built-in ModelScope downloader with a dedicated sidebar tool, supporting YAML-based batch tasks.
- 🦊 **LLaMA.cpp Integration**: Scan local `.gguf` models, monitor RAM/VRAM, and control Embedding/Rerank nodes.
- 🦙 **Ollama Controller**: Manage core Ollama service status and individual model loading/unloading.
- 🐳 **Docker Management**: One-click Start/Stop for RAGFlow clusters and Nginx Proxy Manager.
- 📊 **Unified Telemetry**: Real-time monitoring of PIDs, RAM usage, GPU VRAM estimation, and model capabilities.

### 🛠 Quick Start
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/your-repo/rag-manager.git
   cd rag-manager
   ```
2. **Setup Environment**:
   Run the PowerShell script to automate `.venv` creation:
   ```powershell
   .\setup.ps1
   ```
3. **Configure**:
   Copy `webmonitor/config.example.json` to `webmonitor/config.json` and update your model paths.
4. **Run**:
   ```powershell
   .\start_web_monitor.bat
   ```
   Open `http://localhost:8899` in your browser.

---

<a name="chinese"></a>
## 中文简介

**RAG Manager** 是一款采用 macOS 桌面风格设计的本地 AI 控制面板。它为 **LLaMA.cpp** 和 **Ollama** 提供了实时状态监控、服务生命周期管理以及模型库可视化管理功能。

### ✨ 核心功能
- 🍎 **macOS 审美**：极致的毛玻璃 (Glassmorphism) UI 效果，支持系统级深色模式。
- ⬇️ **GGUF 下载器**：内置 ModelScope 模型下载工具，支持通过 YAML 配置进行可视化或批量下载。
- 🦊 **LLaMA.cpp 集成**：自动扫描本地 `.gguf` 模型库，实时查看显存占用，一键启停 Embedding/Rerank 节点。
- 🦙 **Ollama 控制器**：集成了 Ollama 核心服务状态监测与控制，支持单个模型的按需加载与卸载。
- 🐳 **Docker 管理**：一键管理 RAGFlow 容器集群与 Nginx 代理服务。
- 📊 **指标归一化**：统一展示进程 PID、内存、显存 (VRAM) 估算、运行时间及模型功能标签。

### 🛠 快速上手
1. **克隆项目**：
   ```bash
   git clone https://github.com/your-repo/rag-manager.git
   cd rag-manager
   ```
2. **初始化环境**：
   运行 PowerShell 脚本自动化创建虚拟环境：
   ```powershell
   .\setup.ps1
   ```
3. **配置文件**：
   将 `webmonitor/config.example.json` 复制并重命名为 `webmonitor/config.json`，修改为你的本地模型路径。
4. **启动**：
   ```powershell
   .\start_web_monitor.bat
   ```
   浏览器访问 `http://localhost:8899` 即可。

---

### 📄 License
Under the **MIT License**.