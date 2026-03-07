#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""
cat << 'HTML'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MQTT Settings</title>
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
        .status-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-card.connected {
            background: linear-gradient(135deg, #4caf50, #45a049);
        }
        .status-card.connecting {
            background: linear-gradient(135deg, #ff9800, #f57c00);
        }
        .status-card.disconnected {
            background: linear-gradient(135deg, #f44336, #da190b);
        }
        .status-title {
            font-size: 20px;
            margin: 0 0 10px 0;
            opacity: 0.9;
        }
        .status-value {
            font-size: 32px;
            font-weight: bold;
            margin: 5px 0;
        }
        .status-icon {
            font-size: 64px;
            opacity: 0.5;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
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
            padding: 12px;
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
        .btn {
            padding: 12px 24px;
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
        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
            margin-right: 10px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .3s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .3s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #4caf50;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
        .switch-label {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
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
        .notification.info {
            border-left-color: #17a2b8;
        }
        .view-link {
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            color: white;
            text-decoration: none;
            font-size: 14px;
            margin-left: 15px;
        }
        .view-link:hover {
            background: rgba(255,255,255,0.3);
            color: white;
            text-decoration: none;
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
            .status-card {
                flex-direction: column;
                text-align: center;
            }
            .status-icon {
                margin-top: 20px;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
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
                <a href="/cgi-bin/p/mqtt.cgi" class="navbar-item active">MQTT</a>
                <a href="/cgi-bin/backup.cgi" class="navbar-item">Backups</a>
            </div>
            <a href="/cgi-bin/status.cgi" class="home-button">← Back to Home</a>
        </div>
    </nav>

    <div class="container">
        <div id="notification" class="notification"></div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h1 style="margin:0;">MQTT Settings</h1>
            <a href="/cgi-bin/p/mqtt_status.cgi" class="btn btn-info">📊 View Devices Status</a>
        </div>

        <!-- Status Card -->
        <div id="statusCard" class="status-card">
            <div>
                <div class="status-title">MQTT Connection</div>
                <div class="status-value" id="mqttState">Loading...</div>
                <div id="mqttDetails" style="margin-top: 5px;"></div>
            </div>
            <div class="status-icon" id="statusIcon">📡</div>
        </div>

        <!-- Quick Stats -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value" id="msgsSent">0</div>
                <div class="stat-label">Published</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="msgsReceived">0</div>
                <div class="stat-label">Received</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="haSensors">0</div>
                <div class="stat-label">HA Devices</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="clientStatus">✓</div>
                <div class="stat-label">Client</div>
            </div>
        </div>

        <!-- Main Settings -->
        <div class="card">
            <h3>Main Settings</h3>
            
            <div class="switch-label">
                <label class="switch">
                    <input type="checkbox" id="mqttEnabled">
                    <span class="slider"></span>
                </label>
                <span>Enable MQTT Client</span>
            </div>

            <div class="form-group">
                <label>Broker Address</label>
                <input type="text" class="form-control" id="mqttHost" placeholder="e.g., 192.168.1.30">
            </div>

            <div class="form-group">
                <label>Port</label>
                <input type="number" class="form-control" id="mqttPort" placeholder="1883">
            </div>

            <div class="form-group">
                <label>Username</label>
                <input type="text" class="form-control" id="mqttUser" placeholder="username">
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control" id="mqttPass" placeholder="••••••••">
            </div>

            <div class="form-group">
                <label>Client ID</label>
                <input type="text" class="form-control" id="mqttClientId" placeholder="openipc_doorphone">
            </div>

            <div class="form-group">
                <label>Topic Prefix</label>
                <input type="text" class="form-control" id="mqttTopicPrefix" placeholder="doorphone">
            </div>

            <button class="btn btn-primary" onclick="saveSettings()">💾 Save Settings</button>
        </div>

        <!-- Home Assistant Discovery -->
        <div class="card">
            <h3>Home Assistant Discovery</h3>
            
            <div class="switch-label">
                <label class="switch">
                    <input type="checkbox" id="mqttDiscovery">
                    <span class="slider"></span>
                </label>
                <span>Enable Discovery</span>
            </div>

            <div class="form-group">
                <label>Discovery Prefix</label>
                <input type="text" class="form-control" id="mqttDiscoveryPrefix" placeholder="homeassistant">
            </div>

            <button class="btn btn-success" onclick="sendDiscovery()">📢 Send Discovery Now</button>
            <button class="btn btn-info" onclick="testConnection()">🔌 Test Connection</button>
            <button class="btn btn-warning" onclick="restartMQTT()">🔄 Restart Client</button>
        </div>

        <!-- Device Info -->
        <div class="card">
            <h3>Device Information</h3>
            <p><strong>Device ID:</strong> <code id="deviceId">loading...</code></p>
            <p><strong>Status Topic:</strong> <code id="statusTopic">doorphone/[device_id]/status</code></p>
            <p><strong>Configuration:</strong> <code>/etc/mqtt.conf</code></p>
            <p><strong>Log File:</strong> <code>/var/log/mqtt.log</code></p>
        </div>
    </div>

    <script>
        let currentData = {};

        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.className = 'notification ' + type;
            notification.innerHTML = message;
            notification.style.display = 'block';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }

        function loadSettings() {
            fetch('/cgi-bin/p/mqtt_api.cgi?action=get_status')
                .then(r => r.json())
                .then(data => {
                    currentData = data;
                    console.log('Loaded settings:', data);
                    
                    // Update status card
                    const statusCard = document.getElementById('statusCard');
                    const stateEl = document.getElementById('mqttState');
                    const detailsEl = document.getElementById('mqttDetails');
                    const iconEl = document.getElementById('statusIcon');
                    
                    if (data.connected === 'true') {
                        stateEl.innerHTML = 'CONNECTED';
                        statusCard.className = 'status-card connected';
                        iconEl.innerHTML = '✅';
                        document.getElementById('clientStatus').innerHTML = '✅';
                    } else if (data.enabled === 'true') {
                        stateEl.innerHTML = 'CONNECTING...';
                        statusCard.className = 'status-card connecting';
                        iconEl.innerHTML = '⏳';
                        document.getElementById('clientStatus').innerHTML = '⏳';
                    } else {
                        stateEl.innerHTML = 'DISCONNECTED';
                        statusCard.className = 'status-card disconnected';
                        iconEl.innerHTML = '❌';
                        document.getElementById('clientStatus').innerHTML = '❌';
                    }
                    
                    if (data.host) {
                        detailsEl.innerHTML = `Broker: ${data.host}:${data.port}`;
                    }
                    
                    // Update stats
                    document.getElementById('msgsSent').innerHTML = data.sent || 0;
                    document.getElementById('msgsReceived').innerHTML = data.received || 0;
                    document.getElementById('haSensors').innerHTML = data.discovery_sensors || 0;
                    
                    // Fill form fields with ACTUAL values from API
                    document.getElementById('mqttEnabled').checked = (data.enabled === 'true');
                    document.getElementById('mqttHost').value = data.host || '';
                    document.getElementById('mqttPort').value = data.port || '1883';
                    document.getElementById('mqttUser').value = data.user || '';
                    document.getElementById('mqttClientId').value = data.client_id || 'openipc_doorphone';
                    document.getElementById('mqttTopicPrefix').value = data.topic_prefix || 'doorphone';
                    document.getElementById('mqttDiscovery').checked = (data.discovery === 'true');
                    document.getElementById('mqttDiscoveryPrefix').value = data.discovery_prefix || 'homeassistant';
                    
                    // Set device ID
                    const deviceId = 'openipc-hi3516cv300';
                    document.getElementById('deviceId').innerHTML = deviceId;
                    document.getElementById('statusTopic').innerHTML = `doorphone/${deviceId}/status`;
                })
                .catch(error => {
                    console.error('Error loading settings:', error);
                    showNotification('Error loading settings: ' + error, 'error');
                });
        }

        function saveSettings() {
            const params = new URLSearchParams({
                action: 'save_settings',
                enabled: document.getElementById('mqttEnabled').checked ? 'true' : 'false',
                host: document.getElementById('mqttHost').value,
                port: document.getElementById('mqttPort').value,
                user: document.getElementById('mqttUser').value,
                pass: document.getElementById('mqttPass').value,
                client_id: document.getElementById('mqttClientId').value,
                topic_prefix: document.getElementById('mqttTopicPrefix').value,
                discovery: document.getElementById('mqttDiscovery').checked ? 'true' : 'false',
                discovery_prefix: document.getElementById('mqttDiscoveryPrefix').value
            });
            
            showNotification('Saving settings...', 'info');
            
            fetch('/cgi-bin/p/mqtt_api.cgi?' + params)
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                    if (data.status === 'success') {
                        setTimeout(loadSettings, 1000);
                    }
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        function testConnection() {
            showNotification('Testing connection...', 'info');
            fetch('/cgi-bin/p/mqtt_api.cgi?action=test_connection')
                .then(r => r.json())
                .then(data => showNotification(data.message, data.status === 'success' ? 'success' : 'error'))
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        function sendDiscovery() {
            showNotification('Sending discovery...', 'info');
            fetch('/cgi-bin/p/mqtt_api.cgi?action=send_discovery')
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                    if (data.status === 'success') {
                        setTimeout(loadSettings, 2000);
                    }
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        function restartMQTT() {
            if (confirm('Restart MQTT client?')) {
                showNotification('Restarting MQTT client...', 'info');
                fetch('/cgi-bin/p/mqtt_api.cgi?action=restart')
                    .then(r => r.json())
                    .then(data => {
                        showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                        setTimeout(loadSettings, 2000);
                    })
                    .catch(error => showNotification('Error: ' + error, 'error'));
            }
        }

        // Load settings on page load
        document.addEventListener('DOMContentLoaded', loadSettings);
        
        // Refresh status every 10 seconds
        setInterval(loadSettings, 10000);
    </script>
</body>
</html>
HTML
