"""
Monitor UI Template
Contains the HTML5, CSS3 (macOS Glassmorphism Style), and Vanilla JavaScript
that powers the front-end dashboard.
"""
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG Manager - macOS Desktop</title>
    <style>
        :root {
            --apple-blue: #007aff;
            --apple-green: #34c759;
            --apple-orange: #ff9500;
            --apple-red: #ff3b30;
            --apple-gray: #8e8e93;
            --bg-glass: rgba(255, 255, 255, 0.7);
            --sidebar-glass: rgba(246, 246, 246, 0.8);
            --border-glass: rgba(0, 0, 0, 0.1);
            --text-main: #1d1d1f;
            --text-dim: #86868b;
            --shadow-soft: 0 8px 30px rgba(0,0,0,0.12);
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-glass: rgba(30, 30, 30, 0.7);
                --sidebar-glass: rgba(45, 45, 45, 0.8);
                --border-glass: rgba(255, 255, 255, 0.1);
                --text-main: #f5f5f7;
                --text-dim: #a1a1a6;
            }
        }

        * { box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            background-attachment: fixed;
            color: var(--text-main);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
        }

        @media (prefers-color-scheme: dark) {
            body { background: linear-gradient(135deg, #1e1e1e 0%, #2c3e50 100%); }
        }

        /* --- macOS Window Controls Decoration --- */
        .window-controls {
            display: flex;
            gap: 8px;
            padding: 15px 0 10px 20px;
        }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot-red { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green { background: #27c93f; }

        /* --- Sidebar (Finder Style) --- */
        .sidebar {
            width: 240px;
            background: var(--sidebar-glass);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border-right: 1px solid var(--border-glass);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
            transition: width 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
            z-index: 100;
        }

        .sidebar.collapsed { width: 0; overflow: hidden; border-right: none; }

        .sidebar-header {
            padding: 10px 20px;
            font-weight: 700;
            font-size: 13px;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 10px;
        }

        .nav-item {
            padding: 8px 16px 8px 35px;
            margin: 2px 10px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.2s;
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-main);
        }

        .nav-item:hover { background: rgba(0, 0, 0, 0.05); }
        @media (prefers-color-scheme: dark) { .nav-item:hover { background: rgba(255, 255, 255, 0.05); } }

        .nav-item.active {
            background: var(--apple-blue);
            color: white;
            font-weight: 500;
        }

        .sidebar-btn-group { padding: 5px 15px; display: flex; flex-direction: column; gap: 8px; }
        
        .sidebar-btn {
            border: none;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s;
        }
        .btn-primary { background: var(--apple-blue); color: white; }
        .btn-secondary { background: rgba(0,0,0,0.05); color: var(--text-main); }
        @media (prefers-color-scheme: dark) { .btn-secondary { background: rgba(255,255,255,0.1); } }
        
        .sidebar-btn:hover { filter: brightness(1.1); transform: scale(1.02); }

        /* --- Main Content --- */
        .main-container {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: var(--shadow-soft);
            overflow: hidden;
            position: relative;
        }

        .toolbar {
            height: 52px;
            border-bottom: 1px solid var(--border-glass);
            display: flex;
            align-items: center;
            padding: 0 24px;
            gap: 16px;
        }

        .toolbar-title { font-weight: 700; font-size: 18px; margin-right: auto; }

        .refresh-btn {
            background: none;
            border: 1px solid var(--border-glass);
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 13px;
            cursor: pointer;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .refresh-btn:hover { background: rgba(0,0,0,0.05); }

        .content-scroll {
            flex-grow: 1;
            padding: 24px;
            overflow-y: auto;
        }

        /* --- Table Styling (macOS List View) --- */
        .table-container {
            background: var(--sidebar-glass);
            border: 1px solid var(--border-glass);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 30px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        th {
            text-align: left;
            padding: 10px 16px;
            background: rgba(0,0,0,0.03);
            border-bottom: 1px solid var(--border-glass);
            color: var(--text-dim);
            font-weight: 600;
        }

        td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-glass);
            vertical-align: middle;
        }

        tr:last-child td { border-bottom: none; }
        tr:hover td { background: rgba(0, 122, 255, 0.05); }

        .model-cell { display: flex; flex-direction: column; gap: 2px; }
        .model-name { font-weight: 600; font-size: 14px; color: var(--apple-blue); }
        .model-path { font-size: 11px; color: var(--text-dim); }

        /* --- Badges & Actions --- */
        .badge {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-running { background: rgba(52, 199, 89, 0.15); color: var(--apple-green); border: 1px solid rgba(52, 199, 89, 0.2); }
        .badge-idle { background: rgba(142, 142, 147, 0.1); color: var(--apple-gray); border: 1px solid rgba(0,0,0,0.05); }

        .cap-tag {
            font-size: 10px;
            padding: 1px 6px;
            border-radius: 10px;
            margin-right: 4px;
            font-weight: 600;
            border: 1px solid transparent;
        }
        .cap-chat { background: #e1f5fe; color: #0288d1; border-color: #b3e5fc; }
        .cap-embed { background: #e8f5e9; color: #2e7d32; border-color: #c8e6c9; }
        .cap-rerank { background: #fff3e0; color: #ef6c00; border-color: #ffe0b2; }

        .btn-action {
            padding: 4px 12px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        .btn-action-start { background: var(--apple-blue); color: white; }
        .btn-action-stop { background: var(--apple-red); color: white; }
        .btn-action:hover { filter: brightness(1.1); transform: translateY(-1px); }

        /* --- Separator --- */
        .separator-row td {
            background: rgba(0,122,255,0.03);
            text-align: center;
            color: var(--apple-blue);
            font-weight: 700;
            font-size: 10px;
            letter-spacing: 2px;
            padding: 6px;
            text-transform: uppercase;
        }

        /* --- Download Panel (Full Page Mode) --- */
        .download-view {
            display: none; /* Hidden by default */
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: 40px;
        }
        .download-card {
            background: var(--sidebar-glass);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            padding: 30px 40px;
            width: 100%;
            max-width: 500px;
            box-shadow: var(--shadow-soft);
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .dl-header {
            text-align: center;
            font-size: 20px;
            font-weight: 700;
            color: var(--apple-blue);
            margin-bottom: 10px;
        }
        .dl-input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 100%;
        }
        .dl-input-group label {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-dim);
        }
        .dl-input {
            border: 1px solid var(--border-glass);
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 15px;
            background: rgba(255,255,255,0.6);
            color: var(--text-main);
            outline: none;
            transition: all 0.2s;
            width: 100%;
        }
        .dl-input:focus { border-color: var(--apple-blue); background: #fff; box-shadow: 0 0 0 3px rgba(0,122,255,0.1); }
        @media (prefers-color-scheme: dark) {
            .dl-input { background: rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.1); }
            .dl-input:focus { background: rgba(0,0,0,0.5); }
        }
        .btn-download-large {
            background: var(--apple-blue);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 10px;
            width: 100%;
        }
        .btn-download-large:hover { filter: brightness(1.1); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,122,255,0.3); }

        .metric-text { font-family: "SF Mono", "Menlo", monospace; font-weight: 500; }

        .sidebar-toggle-fixed {
            position: absolute;
            bottom: 20px;
            left: 20px;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--sidebar-glass);
            border: 1px solid var(--border-glass);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 102;
        }

        .loading-screen {
            position: absolute; top:0; left:0; right:0; bottom:0;
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(5px);
            z-index: 999;
            display: none;
            align-items: center; justify-content: center;
            font-weight: 600;
        }
        @media (prefers-color-scheme: dark) { .loading-screen { background: rgba(0,0,0,0.6); } }

        /* --- New Status Bar / Footer --- */
        .footer {
            height: 120px;
            background: var(--sidebar-glass);
            border-top: 1px solid var(--border-glass);
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 0 32px;
            font-size: 14px;
            color: var(--text-dim);
            font-weight: 500;
            gap: 12px;
            z-index: 101;
        }
        .status-item { display: flex; align-items: center; gap: 6px; }
        .status-value { color: var(--apple-blue); font-weight: 700; font-family: "SF Mono", monospace; }
        .copy-toast {
            position: absolute; bottom: 50px; left: 50%; transform: translateX(-50%);
            background: var(--apple-blue); color: white; padding: 6px 16px; border-radius: 20px;
            font-size: 12px; font-weight: 600; opacity: 0; transition: opacity 0.3s; pointer-events: none;
        }
        .copy-toast.show { opacity: 1; }
        .model-name { cursor: pointer; transition: opacity 0.2s; }
        .model-name:hover { opacity: 0.7; text-decoration: underline; }
    </style>
</head>
<body>

    <!-- macOS Sidebar -->
    <div class="sidebar" id="sidebar">
        <div class="window-controls">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
        </div>
        
        <div class="sidebar-header">Cluster Control</div>
        <div class="sidebar-btn-group">
            <button class="sidebar-btn btn-primary" onclick="actionSys('rag_start')">🚀 Start RAG System</button>
            <button class="sidebar-btn btn-secondary" onclick="if(confirm('Stop all cluster services?')) actionSys('rag_stop')">🛑 Stop Services</button>
        </div>

        <div class="sidebar-header">Engines</div>
        <div class="nav-item active" id="tab-llama" onclick="switchTab('llama')">🦊 LLaMA.cpp</div>
        <div class="nav-item" id="tab-ollama" onclick="switchTab('ollama')">🦙 Ollama</div>
        
        <div class="sidebar-header">Tools</div>
        <div class="nav-item" id="tab-gguf" onclick="switchTab('gguf')">⬇️ Download Models</div>
    </div>

    <!-- Main Window Content -->
    <div class="main-container">
        <div class="toolbar">
            <div class="toolbar-title" id="page-title">LLaMA.cpp Instances</div>
            <div id="service-status-container" style="display:none; align-items:center; gap:8px;">
                <span id="ollama-service-badge" class="badge">Checking...</span>
            </div>
            <button id="ollama-start-btn" class="refresh-btn" style="display:none; background:var(--apple-green); color:white; border:none;" onclick="actionOllamaService('start')">▶ Start Service</button>
            <button class="refresh-btn" onclick="fetchData()">⟳ Refresh</button>
        </div>

        <div class="content-scroll" id="main-scroll-area">
            
            <!-- Views Container -->
            <div id="table-view" style="display: block;">
                <div class="table-container">
                    <table id="main-table">
                        <thead>
                            <tr id="table-header">
                                <th style="width:80px">Action</th>
                                <th style="width:35%">Model Resource</th>
                                <th>Capability</th>
                                <th>Status</th>
                                <th>System RAM</th>
                                <th>GPU VRAM</th>
                                <th id="runtime-header">Runtime / Size</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">
                            <!-- Injected via JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- GGUF Downloader View (Full Page) -->
            <div id="gguf-view" class="download-view">
                <div class="download-card">
                    <div class="dl-header">⬇️ GGUF Model Downloader</div>
                    <div style="text-align:center; margin-bottom:10px;">
                        <a href="https://modelscope.cn/models?name=gguf&page=1&tabKey=task" target="_blank" 
                           style="color:var(--apple-blue); font-size:13px; text-decoration:none; font-weight:500;">
                           🔗 Browse GGUF Models on ModelScope
                        </a>
                    </div>
                    <div class="dl-input-group">
                        <label>Repository ID</label>
                        <input type="text" id="dl-model-id" class="dl-input" placeholder="e.g. unsloth/Qwen3.5-0.8B-GGUF">
                    </div>
                    <div class="dl-input-group">
                        <label>File Name</label>
                        <input type="text" id="dl-file" class="dl-input" placeholder="e.g. Qwen3.5-0.8B-Q8_0.gguf">
                    </div>
                    <div class="dl-input-group">
                        <label>Save Directory</label>
                        <input type="text" id="dl-dir" class="dl-input" placeholder="D:\\oLLM\\alone_models" value="D:\\oLLM\\alone_models">
                    </div>
                    <button class="btn-download-large" onclick="actionDownloadGGUF()">🚀 Start Download Task</button>
                </div>
            </div>
            
        </div>

        <!-- Footer / Status Bar -->
        <div class="footer">
            <div class="status-value" id="stat-name" style="font-size: 24px; margin-bottom: 5px;">None</div>
            <div class="status-value" id="stat-url" style="font-size: 18px; opacity: 0.8;">-</div>
        </div>

        <div class="copy-toast" id="copy-toast">Copied to Clipboard!</div>
        <div class="loading-screen" id="loading">Updating System Status...</div>
    </div>

    <button class="sidebar-toggle-fixed" onclick="toggleSidebar()">📂</button>

    <script>
        let currentTab = 'llama';

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('collapsed');
        }

        function switchTab(name) {
            currentTab = name;
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            document.getElementById(`tab-${name}`).classList.add('active');

            // View Toggling
            const tableView = document.getElementById('table-view');
            const ggufView = document.getElementById('gguf-view');
            const refreshBtn = document.getElementById('refresh-btn');
            
            if (name === 'gguf') {
                tableView.style.display = 'none';
                ggufView.style.display = 'flex';
                document.getElementById('page-title').innerText = 'GGUF Model Downloader';
                document.getElementById('service-status-container').style.display = 'none';
                document.getElementById('ollama-start-btn').style.display = 'none';
                if(refreshBtn) refreshBtn.style.display = 'none';
            } else {
                ggufView.style.display = 'none';
                tableView.style.display = 'block';
                if(refreshBtn) refreshBtn.style.display = 'flex';
                document.getElementById('page-title').innerText = name === 'llama' ? 'LLaMA.cpp Instances' : 'Ollama Management';
                document.getElementById('runtime-header').innerText = name === 'llama' ? 'Uptime' : 'Disk Size';
                fetchData();
            }
        }

        function renderTags(caps) {
            if (!caps || caps.length === 0) return '-';
            return `<div style="display: flex; gap: 4px; flex-wrap: wrap;">
                ${caps.map(cap => `<span class="badge" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); padding: 2px 6px; font-size: 10px;">${cap}</span>`).join('')}
            </div>`;
        }

        async function actionSys(t) {
            showLoading(true);
            try {
                const res = await fetch(`/api/sys_${t}`, {method:'POST'});
                const data = await res.json();
                if(!res.ok) throw new Error(data.msg);
                fetchData();
            } catch(e) { alert('System Error: ' + e.message); }
            finally { showLoading(false); }
        }

        async function actionLlama(act, tgt) {
            showLoading(true);
            try {
                const res = await fetch(`/api/llama_${act}`, {
                    method:'POST', 
                    headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({target: tgt})
                });
                const data = await res.json();
                if(!res.ok) throw new Error(data.msg);
                fetchData();
            } catch(e) { alert('Llama Error: ' + e.message); }
            finally { showLoading(false); }
        }

        async function actionOllama(act, model) {
            showLoading(true);
            try {
                const res = await fetch(`/api/ollama_${act}`, {
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({model: model})
                });
                const data = await res.json();
                if(!res.ok) throw new Error(data.msg);
                fetchData();
            } catch(e) { alert('Ollama Error: ' + e.message); }
            finally { showLoading(false); }
        }

        async function actionOllamaService(act) {
            showLoading(true);
            try {
                const res = await fetch(`/api/ollama_service_${act}`, { method:'POST' });
                const data = await res.json();
                if(!res.ok) throw new Error(data.msg);
                // Give it a moment to start
                setTimeout(fetchData, 2000);
            } catch(e) { alert('Service Error: ' + e.message); }
            finally { showLoading(false); }
        }

        async function actionDownloadGGUF() {
            const model_id = document.getElementById('dl-model-id').value.trim();
            const file = document.getElementById('dl-file').value.trim();
            const dir = document.getElementById('dl-dir').value.trim();

            if(!model_id || !file) {
                alert("Please fill in both Model ID and File Name.");
                return;
            }

            try {
                const res = await fetch('/api/gguf_download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ model_id, file, dir })
                });
                const data = await res.json();
                if(!res.ok) throw new Error(data.msg);
                alert(data.msg); // Show success message
            } catch(e) {
                alert('Download Error: ' + e.message);
            }
        }

        function showLoading(show) {
            document.getElementById('loading').style.display = show ? 'flex' : 'none';
        }

        function renderTags(caps) {
            if(!caps) return '';
            return caps.map(c => {
                let cls = 'cap-chat';
                if(c.includes('Embed')) cls = 'cap-embed';
                if(c.includes('Rerank')) cls = 'cap-rerank';
                return `<span class="cap-tag ${cls}">${c}</span>`;
            }).join('');
        }

        function copyEndpoint(fullName, port) {
            // Remove file extension (e.g., .gguf)
            const name = fullName.replace(/\.[^/.]+$/, "");
            const url = `host.docker.internal:${port || '?'}`;
            const textToCopy = `${name}    ${url}`;
            
            // Clipboard copy
            const el = document.createElement('textarea');
            el.value = textToCopy;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);

            // Update UI
            document.getElementById('stat-name').innerText = name;
            document.getElementById('stat-url').innerText = url;

            // Show Toast
            const toast = document.getElementById('copy-toast');
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }

        async function fetchData() {
            if (currentTab === 'gguf') return; // Do not fetch table data if in download view
            
            showLoading(true);
            try {
                const res = await fetch('/api/data');
                const data = await res.json();
                const tbody = document.getElementById('table-body');
                let html = '';
                
                // Update Ollama Service Status UI
                const statusContainer = document.getElementById('service-status-container');
                const startBtn = document.getElementById('ollama-start-btn');
                const badge = document.getElementById('ollama-service-badge');

                if (currentTab === 'ollama') {
                    statusContainer.style.display = 'flex';
                    if (data.ollama_live) {
                        badge.innerText = 'SERVICE: SERVING';
                        badge.className = 'badge badge-running';
                        startBtn.style.display = 'none';
                    } else {
                        badge.innerText = 'SERVICE: STOPPED';
                        badge.className = 'badge badge-idle';
                        startBtn.style.display = 'block';
                    }
                } else if (currentTab === 'llama') {
                    statusContainer.style.display = 'none';
                    startBtn.style.display = 'none';
                }

                if(currentTab === 'llama') {
                    let lastActive = null;
                    for(let m of data.llama_models) {
                        if(lastActive === true && m.running === false) {
                            html += `<tr class="separator-row"><td colspan="7">Available Offline Models</td></tr>`;
                        }
                        lastActive = m.running;
                        
                        let action = m.running 
                            ? `<button class="btn-action btn-action-stop" onclick="actionLlama('stop', ${m.pid})">Stop</button>`
                            : (m.service_type ? `<button class="btn-action btn-action-start" onclick="actionLlama('start', '${m.service_type}')">Run</button>` : '-');

                        html += `
                            <tr>
                                <td>${action}</td>
                                <td>
                                    <div class="model-cell">
                                        <span class="model-name" onclick="copyEndpoint('${m.name}', '${m.port || ''}')">${m.name}</span>
                                        <span class="model-path">/alone_models/${m.name}</span>
                                    </div>
                                </td>
                                <td>${renderTags(m.caps)}</td>
                                <td><span class="badge ${m.running ? 'badge-running' : 'badge-idle'}">${m.running ? 'Active ('+m.pid+')' : 'Idle'}</span></td>
                                <td class="metric-text">${(m.running ? m.ram_mb : 0).toFixed(2)} MB</td>
                                <td class="metric-text" style="color:var(--apple-orange)">${(m.running ? m.vram_mb : 0).toFixed(2)} MB</td>
                                <td class="metric-text">${m.running ? m.uptime : m.size_mb.toFixed(2) + ' MB'}</td>
                            </tr>
                        `;
                    }
                } else {
                    let lastActive = null;
                    if(data.ollama_error) {
                        html = `<tr><td colspan="7" style="text-align:center; padding:20px; color:red">${data.ollama_error}</td></tr>`;
                    } else {
                        for(let m of data.ollama_all) {
                            if(lastActive === true && m.running === false) {
                                html += `<tr class="separator-row"><td colspan="7">Cached Library Models</td></tr>`;
                            }
                            lastActive = m.running;
                            
                            let action = m.running 
                                ? `<button class="btn-action btn-action-stop" onclick="actionOllama('unload', '${m.name}')">Eject</button>`
                                : `<button class="btn-action btn-action-start" onclick="actionOllama('load', '${m.name}')">Load</button>`;

                            html += `
                                <tr>
                                    <td>${action}</td>
                                    <td>
                                        <div class="model-cell">
                                            <span class="model-name" onclick="copyEndpoint('${m.name}', '${m.port}')">${m.name}</span>
                                            <span class="model-path">Ollama Repository</span>
                                        </div>
                                    </td>
                                    <td>${renderTags(m.caps)}</td>
                                    <td><span class="badge ${m.running ? 'badge-running' : 'badge-idle'}">${m.running ? 'In VRAM' : 'On Disk'}</span></td>
                                    <td class="metric-text">${(m.running ? (m.total_mb - m.vram_mb) : 0).toFixed(2)} MB</td>
                                    <td class="metric-text" style="color:var(--apple-orange)">${(m.running ? m.vram_mb : 0).toFixed(2)} MB</td>
                                    <td class="metric-text">${m.disk_size_mb.toFixed(2)} MB</td>
                                </tr>
                            `;
                        }
                    }
                }
                tbody.innerHTML = html;
            } catch(e) { console.error(e); }
            finally { showLoading(false); }
        }

        setInterval(fetchData, 60000);
        fetchData();
    </script>
</body>
</html>
"""
