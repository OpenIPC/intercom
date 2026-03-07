#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

cat << 'EOFH'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backup Manager</title>
    <link rel="stylesheet" href="/a/bootstrap.min.css">
    <style>
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 0;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .navbar-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar-brand {
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-decoration: none;
        }
        .navbar-brand:hover {
            color: rgba(255,255,255,0.9);
        }
        .navbar-menu {
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        .navbar-item {
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            transition: all 0.3s;
        }
        .navbar-item:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }
        .navbar-item.active {
            background: rgba(255,255,255,0.3);
            font-weight: bold;
        }
        .home-button {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 14px;
            transition: all 0.3s;
        }
        .home-button:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            color: white;
            text-decoration: none;
        }
        body {
            background: #f5f5f5;
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .card:hover {
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            color: white;
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5a67d8;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(102,126,234,0.3);
        }
        .btn-success {
            background: #4caf50;
            color: white;
        }
        .btn-success:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(76,175,80,0.3);
        }
        .btn-danger {
            background: #f44336;
            color: white;
        }
        .btn-danger:hover {
            background: #da190b;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(244,67,54,0.3);
        }
        .btn-info {
            background: #17a2b8;
            color: white;
        }
        .btn-info:hover {
            background: #138496;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(23,162,184,0.3);
        }
        .btn-warning {
            background: #ff9800;
            color: white;
        }
        .btn-warning:hover {
            background: #e68900;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255,152,0,0.3);
        }
        .btn-sm {
            padding: 6px 12px;
            font-size: 12px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #495057;
            font-weight: 500;
        }
        .form-control {
            width: 100%;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
            box-sizing: border-box;
        }
        .form-control:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        .storage-option {
            display: flex;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .storage-option:hover {
            border-color: #667eea;
            background: #f8f9fa;
        }
        .storage-option.selected {
            border-color: #667eea;
            background: #e3f2fd;
        }
        .storage-option.disabled {
            opacity: 0.6;
            cursor: not-allowed;
            background: #f8f9fa;
        }
        .storage-icon {
            font-size: 24px;
            margin-right: 15px;
        }
        .storage-details {
            flex: 1;
        }
        .storage-name {
            font-weight: bold;
            font-size: 16px;
        }
        .storage-path {
            color: #666;
            font-size: 12px;
        }
        .storage-space {
            color: #28a745;
            font-size: 12px;
        }
        .backup-list {
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-top: 20px;
        }
        .backup-item {
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .backup-item:last-child {
            border-bottom: none;
        }
        .backup-item:hover {
            background: #f8f9fa;
        }
        .backup-info {
            flex: 1;
        }
        .backup-name {
            font-weight: 500;
            margin-bottom: 5px;
        }
        .backup-meta {
            font-size: 12px;
            color: #666;
        }
        .component-selector {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .component-item {
            padding: 8px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .component-item input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        .component-item label {
            cursor: pointer;
            flex: 1;
        }
        .upload-area {
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 30px;
            text-align: center;
            background: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s;
            margin: 20px 0;
        }
        .upload-area:hover {
            background: #e3f2fd;
            border-color: #5a67d8;
        }
        .upload-area.dragover {
            background: #bbdefb;
            border-color: #4c51bf;
        }
        .progress {
            margin-top: 15px;
            display: none;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
        }
        .notification {
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 15px 20px;
            background: white;
            border-radius: 8px;
            display: none;
            z-index: 1000;
            border-left: 4px solid;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .notification.success {
            border-left-color: #4caf50;
        }
        .notification.error {
            border-left-color: #f44336;
        }
        @media (max-width: 768px) {
            .navbar-container {
                flex-direction: column;
                gap: 10px;
            }
            .navbar-menu {
                width: 100%;
                justify-content: center;
            }
            .backup-item {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-container">
            <a href="/cgi-bin/status.cgi" class="navbar-brand">OpenIPC Doorphone</a>
            <div class="navbar-menu">
                <a href="/cgi-bin/status.cgi" class="navbar-item">Home</a>
                <a href="/cgi-bin/p/door_keys.cgi" class="navbar-item">Keys</a>
                <a href="/cgi-bin/p/sip_manager.cgi" class="navbar-item">SIP</a>
                <a href="/cgi-bin/p/qr_generator.cgi" class="navbar-item">QR</a>
                <a href="/cgi-bin/p/temp_keys.cgi" class="navbar-item">Temporary</a>
                <a href="/cgi-bin/p/sounds.cgi" class="navbar-item">Sounds</a>
                <a href="/cgi-bin/p/door_history.cgi" class="navbar-item">History</a>
                <a href="/cgi-bin/p/mqtt.cgi" class="navbar-item">MQTT</a>
                <a href="/cgi-bin/backup.cgi" class="navbar-item active">Backups</a>
            </div>
            <a href="/cgi-bin/status.cgi" class="home-button">← Back to Home</a>
        </div>
    </nav>

    <div class="container">
        <div id="notification" class="notification"></div>
        
        <h1>Backup Manager</h1>

        <!-- Storage Selection -->
        <div class="card">
            <h3>Storage Location</h3>
            <div id="storageOptions" class="storage-options">
                <div class="text-center py-3">Loading storage devices...</div>
            </div>
            <div id="selectedStorageInfo" class="storage-info mt-3" style="display: none;"></div>
        </div>

        <!-- Component Selection -->
        <div class="card">
            <h3>Backup Components</h3>
            <div class="component-selector">
                <div class="component-item">
                    <input type="checkbox" id="backup_cgi" checked>
                    <label for="backup_cgi"><strong>CGI Scripts</strong> - All web interface files (/var/www/cgi-bin/p/*.cgi)</label>
                </div>
                <div class="component-item">
                    <input type="checkbox" id="backup_baresip" checked>
                    <label for="backup_baresip"><strong>SIP Configuration</strong> - SIP accounts and settings (/etc/baresip/)</label>
                </div>
                <div class="component-item">
                    <input type="checkbox" id="backup_keys" checked>
                    <label for="backup_keys"><strong>Key Database</strong> - All RFID and QR keys (/etc/door_keys.conf)</label>
                </div>
                <div class="component-item">
                    <input type="checkbox" id="backup_mqtt" checked>
                    <label for="backup_mqtt"><strong>MQTT Configuration</strong> - MQTT broker settings (/etc/mqtt.conf)</label>
                </div>
                <div class="component-item">
                    <input type="checkbox" id="backup_scripts" checked>
                    <label for="backup_scripts"><strong>System Scripts</strong> - door_monitor.sh, mqtt_client.sh, start scripts</label>
                </div>
                <div class="component-item">
                    <input type="checkbox" id="backup_init" checked>
                    <label for="backup_init"><strong>Init Scripts</strong> - Autostart scripts (/etc/init.d/S99door)</label>
                </div>
                <div class="component-item">
                    <input type="checkbox" id="backup_majestic" checked>
                    <label for="backup_majestic"><strong>Majestic Config</strong> - Camera settings (/etc/majestic.yaml)</label>
                </div>
                <div class="component-item">
                    <input type="checkbox" id="backup_uart" checked>
                    <label for="backup_uart"><strong>UART Settings</strong> - Serial port configuration</label>
                </div>
            </div>
            <div>
                <button class="btn btn-sm btn-info" onclick="selectAll(true)">Select All</button>
                <button class="btn btn-sm btn-warning" onclick="selectAll(false)">Deselect All</button>
            </div>
        </div>

        <!-- Actions -->
        <div class="card">
            <h3>Actions</h3>
            <button class="btn btn-primary" onclick="createBackup()">Create Backup</button>
            <button class="btn btn-info" onclick="scanStorage()">Scan Storage</button>
            <button class="btn btn-secondary" onclick="loadBackups()">Refresh List</button>
        </div>

        <!-- Upload Backup -->
        <div class="card">
            <h3>Upload Backup</h3>
            <div class="upload-area" id="uploadArea">
                <div style="font-size: 48px; margin-bottom: 10px;">📤</div>
                <p>Click or drag backup file here</p>
                <p class="text-muted small">Supported formats: .tar, .tar.gz</p>
                <input type="file" id="fileInput" style="display: none;" accept=".tar,.tar.gz,.tgz">
            </div>
            <div id="uploadProgress" class="progress">
                <div class="progress-bar">
                    <div class="progress-fill" id="uploadProgressFill"></div>
                </div>
                <p class="text-center mt-2" id="progressText">Uploading...</p>
            </div>
        </div>

        <!-- Backup List -->
        <div class="card">
            <h3>Existing Backups</h3>
            <div id="backupList" class="backup-list">
                <div class="text-center py-4">Loading backups...</div>
            </div>
            <div class="mt-3 text-muted small">
                * Last 10 backups are kept, older ones are automatically deleted
            </div>
        </div>
    </div>

    <script>
        let selectedStorage = null;
        let currentBackupComponents = {
            cgi: true,
            baresip: true,
            keys: true,
            mqtt: true,
            scripts: true,
            init: true,
            majestic: true,
            uart: true
        };

        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.className = 'notification ' + type;
            notification.innerHTML = message;
            notification.style.display = 'block';
            setTimeout(() => notification.style.display = 'none', 3000);
        }

        function selectAll(select) {
            document.getElementById('backup_cgi').checked = select;
            document.getElementById('backup_baresip').checked = select;
            document.getElementById('backup_keys').checked = select;
            document.getElementById('backup_mqtt').checked = select;
            document.getElementById('backup_scripts').checked = select;
            document.getElementById('backup_init').checked = select;
            document.getElementById('backup_majestic').checked = select;
            document.getElementById('backup_uart').checked = select;
            updateComponents();
        }

        function updateComponents() {
            currentBackupComponents = {
                cgi: document.getElementById('backup_cgi').checked,
                baresip: document.getElementById('backup_baresip').checked,
                keys: document.getElementById('backup_keys').checked,
                mqtt: document.getElementById('backup_mqtt').checked,
                scripts: document.getElementById('backup_scripts').checked,
                init: document.getElementById('backup_init').checked,
                majestic: document.getElementById('backup_majestic').checked,
                uart: document.getElementById('backup_uart').checked
            };
        }

        document.getElementById('backup_cgi').addEventListener('change', updateComponents);
        document.getElementById('backup_baresip').addEventListener('change', updateComponents);
        document.getElementById('backup_keys').addEventListener('change', updateComponents);
        document.getElementById('backup_mqtt').addEventListener('change', updateComponents);
        document.getElementById('backup_scripts').addEventListener('change', updateComponents);
        document.getElementById('backup_init').addEventListener('change', updateComponents);
        document.getElementById('backup_majestic').addEventListener('change', updateComponents);
        document.getElementById('backup_uart').addEventListener('change', updateComponents);

        // Upload area handlers
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');

        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const file = e.dataTransfer.files[0];
            if (file) uploadBackup(file);
        });
        fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) uploadBackup(e.target.files[0]);
        });

        function scanStorage() {
            const storageDiv = document.getElementById('storageOptions');
            storageDiv.innerHTML = '<div class="text-center py-3">Scanning storage devices...</div>';
            
            fetch('/cgi-bin/p/backup_api.cgi?action=scan_storage')
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success' && data.devices && data.devices.length > 0) {
                        let html = '';
                        data.devices.forEach((device, index) => {
                            const isSelected = (selectedStorage && selectedStorage.path === device.path) || (index === 0 && device.available && !selectedStorage);
                            const selectedClass = isSelected ? 'selected' : '';
                            const disabledClass = device.available ? '' : 'disabled';
                            
                            html += `
                                <div class="storage-option ${selectedClass} ${disabledClass}" onclick="${device.available ? 'selectStorage(\'' + device.path + '\', \'' + device.name + '\', \'' + device.mount + '\', \'' + device.free + '\')' : ''}">
                                    <span class="storage-icon">${device.icon}</span>
                                    <div class="storage-details">
                                        <div class="storage-name">${device.name}</div>
                                        <div class="storage-path">${device.mount || 'Not mounted'}</div>
                                        ${device.available 
                                            ? '<div class="storage-space">Free: ' + device.free + '</div>'
                                            : '<div class="storage-space" style="color:#f44336;">⚠️ ' + (device.error || 'Unavailable') + '</div>'
                                        }
                                    </div>
                                </div>
                            `;
                            
                            if (isSelected && device.available) {
                                selectedStorage = {
                                    path: device.path,
                                    name: device.name,
                                    mount: device.mount,
                                    free: device.free
                                };
                            }
                        });
                        storageDiv.innerHTML = html;
                        
                        if (selectedStorage) {
                            loadBackups();
                        } else {
                            const firstAvailable = data.devices.find(d => d.available);
                            if (firstAvailable) {
                                selectStorage(firstAvailable.path, firstAvailable.name, firstAvailable.mount, firstAvailable.free);
                            }
                        }
                    } else {
                        storageDiv.innerHTML = '<div class="text-center py-3">⚠️ No storage devices available</div>';
                    }
                })
                .catch(error => {
                    storageDiv.innerHTML = '<div class="text-center py-3">❌ Scan error</div>';
                    console.error('Scan error:', error);
                });
        }

        function selectStorage(path, name, mount, free) {
            document.querySelectorAll('.storage-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            
            selectedStorage = { path, name, mount, free };
            loadBackups();
        }

        function uploadBackup(file) {
            if (!selectedStorage) {
                showNotification('Please select storage location first', 'warning');
                return;
            }

            const progress = document.getElementById('uploadProgress');
            const progressFill = document.getElementById('uploadProgressFill');
            const progressText = document.getElementById('progressText');
            progress.style.display = 'block';
            progressFill.style.width = '0%';
            progressText.textContent = 'Preparing...';

            const formData = new FormData();
            formData.append('backup', file);

            const xhr = new XMLHttpRequest();
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percent = (e.loaded / e.total) * 100;
                    progressFill.style.width = percent + '%';
                    progressText.textContent = `Uploading: ${Math.round(percent)}%`;
                }
            });

            xhr.addEventListener('load', () => {
                progress.style.display = 'none';
                if (xhr.status === 200) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        showNotification(response.message, response.status === 'success' ? 'success' : 'error');
                        if (response.status === 'success') loadBackups();
                    } catch (e) {
                        showNotification('Upload successful', 'success');
                        loadBackups();
                    }
                } else {
                    showNotification('Upload error', 'error');
                }
            });

            xhr.addEventListener('error', () => {
                progress.style.display = 'none';
                showNotification('Connection error', 'error');
            });

            xhr.open('POST', '/cgi-bin/p/upload_final.cgi?storage=' + encodeURIComponent(selectedStorage.path));
            xhr.send(formData);
        }

        function createBackup() {
            if (!selectedStorage) {
                showNotification('Please select storage location', 'warning');
                return;
            }

            updateComponents();
            
            const components = [];
            if (currentBackupComponents.cgi) components.push('cgi');
            if (currentBackupComponents.baresip) components.push('baresip');
            if (currentBackupComponents.keys) components.push('keys');
            if (currentBackupComponents.mqtt) components.push('mqtt');
            if (currentBackupComponents.scripts) components.push('scripts');
            if (currentBackupComponents.init) components.push('init');
            if (currentBackupComponents.majestic) components.push('majestic');
            if (currentBackupComponents.uart) components.push('uart');

            if (components.length === 0) {
                showNotification('Please select at least one component', 'warning');
                return;
            }

            showNotification('Creating backup...', 'info');

            fetch('/cgi-bin/p/backup_api.cgi?action=create_backup&storage=' + 
                  encodeURIComponent(selectedStorage.path) + 
                  '&components=' + components.join(','))
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                    if (data.status === 'success') loadBackups();
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        function loadBackups() {
            if (!selectedStorage) {
                document.getElementById('backupList').innerHTML = '<div class="text-center py-4">Please select a storage device first</div>';
                return;
            }

            const listDiv = document.getElementById('backupList');
            listDiv.innerHTML = '<div class="text-center py-4">Loading backups...</div>';

            fetch('/cgi-bin/p/backup_api.cgi?action=list_backups&storage=' + encodeURIComponent(selectedStorage.path))
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        if (!data.backups || data.backups.length === 0) {
                            listDiv.innerHTML = '<div class="text-center py-4">📭 No backups found</div>';
                            return;
                        }

                        let html = '';
                        data.backups.forEach(backup => {
                            const dateStr = backup.date.replace(/_/g, ' ');
                            const displayDate = dateStr.substring(0, 4) + '-' + 
                                                dateStr.substring(4, 6) + '-' + 
                                                dateStr.substring(6, 8) + ' ' + 
                                                dateStr.substring(9, 11) + ':' + 
                                                dateStr.substring(11, 13) + ':' + 
                                                dateStr.substring(13, 15);
                            
                            html += '<div class="backup-item">' +
                                '<div class="backup-info">' +
                                    '<div class="backup-name">📁 ' + backup.file + '</div>' +
                                    '<div class="backup-meta">' + displayDate + ' • ' + backup.size + '</div>' +
                                '</div>' +
                                '<div>' +
                                    '<button class="btn btn-info btn-sm" onclick="downloadBackup(\'' + backup.file + '\')">📥 Download</button> ' +
                                    '<button class="btn btn-success btn-sm" onclick="restoreBackup(\'' + backup.file + '\')">⟲ Restore</button> ' +
                                    '<button class="btn btn-danger btn-sm" onclick="deleteBackup(\'' + backup.file + '\')">🗑️ Delete</button>' +
                                '</div>' +
                                '</div>';
                        });
                        listDiv.innerHTML = html;
                    } else {
                        listDiv.innerHTML = '<div class="text-center py-4">❌ Error loading backups</div>';
                    }
                })
                .catch(error => {
                    listDiv.innerHTML = '<div class="text-center py-4">❌ Connection error</div>';
                });
        }

        function downloadBackup(file) {
            if (!selectedStorage) return;
            
            const form = document.createElement('form');
            form.method = 'GET';
            form.action = '/cgi-bin/p/backup_api.cgi';
            form.style.display = 'none';
            
            const actionInput = document.createElement('input');
            actionInput.type = 'hidden';
            actionInput.name = 'action';
            actionInput.value = 'download_backup';
            
            const storageInput = document.createElement('input');
            storageInput.type = 'hidden';
            storageInput.name = 'storage';
            storageInput.value = selectedStorage.path;
            
            const fileInput = document.createElement('input');
            fileInput.type = 'hidden';
            fileInput.name = 'file';
            fileInput.value = file;
            
            form.appendChild(actionInput);
            form.appendChild(storageInput);
            form.appendChild(fileInput);
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);
        }

        function restoreBackup(file) {
            if (!selectedStorage) return;
            
            if (!confirm('⚠️ Restore backup ' + file + '?\n\nThis will overwrite current files!\nReboot recommended after restore.')) return;
            
            showNotification('Restoring...', 'info');
            
            fetch('/cgi-bin/p/backup_api.cgi?action=restore_backup&storage=' + 
                  encodeURIComponent(selectedStorage.path) + 
                  '&file=' + encodeURIComponent(file))
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                    if (data.status === 'success') loadBackups();
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        function deleteBackup(file) {
            if (!selectedStorage) return;
            
            if (!confirm('🗑️ Delete backup ' + file + '?')) return;
            
            fetch('/cgi-bin/p/backup_api.cgi?action=delete_backup&storage=' + 
                  encodeURIComponent(selectedStorage.path) + 
                  '&file=' + encodeURIComponent(file))
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                    if (data.status === 'success') loadBackups();
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            scanStorage();
            updateComponents();
        });

        // Auto-refresh backup list
        setInterval(loadBackups, 30000);
    </script>
</body>
</html>
EOFH
