#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""
cat << 'HTML'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MQTT Devices Status</title>
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
        }
        .navbar-item:hover {
            background: rgba(255,255,255,0.2);
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
        }
        body {
            background: #f5f5f5;
            margin: 0;
            font-family: Arial, sans-serif;
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
        }
        .status-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .device-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .device-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #667eea;
        }
        .device-name {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .device-id {
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
            font-family: monospace;
        }
        .device-topic {
            font-size: 12px;
            background: #e9ecef;
            padding: 5px;
            border-radius: 4px;
            font-family: monospace;
            margin-bottom: 10px;
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }
        .badge-success {
            background: #4caf50;
            color: white;
        }
        .badge-warning {
            background: #ff9800;
            color: white;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
        .control-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-right: 10px;
        }
        .control-btn:hover {
            background: #5a67d8;
        }
        .notification {
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 12px 20px;
            background: white;
            border-radius: 5px;
            display: none;
            z-index: 1000;
            border-left: 4px solid #4caf50;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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
                <a href="/cgi-bin/p/mqtt.cgi" class="navbar-item active">MQTT</a>
                <a href="/cgi-bin/backup.cgi" class="navbar-item">Backups</a>
            </div>
            <a href="/cgi-bin/status.cgi" class="home-button">← Back to Home</a>
        </div>
    </nav>

    <div class="container">
        <div id="notification" class="notification"></div>
        
        <h1>MQTT Devices Status</h1>
        
        <!-- Connection Status -->
        <div class="status-card" id="connectionCard">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin:0 0 10px 0;">MQTT Connection</h3>
                    <div style="font-size: 20px; font-weight: bold;" id="connStatus">Checking...</div>
                    <div id="connDetails"></div>
                </div>
                <div style="font-size: 48px;">📡</div>
            </div>
        </div>

        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value" id="totalDevices">6</div>
                <div class="stat-label">Total Devices</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="publishedCount">0</div>
                <div class="stat-label">Published</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="discoveryStatus">✅</div>
                <div class="stat-label">Discovery</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="brokerStatus">✓</div>
                <div class="stat-label">Broker</div>
            </div>
        </div>

        <!-- Controls -->
        <div class="card">
            <h3>Controls</h3>
            <button class="control-btn" onclick="testRelay()">🔌 Test Relay</button>
            <button class="control-btn" onclick="resendDiscovery()">📢 Resend Discovery</button>
            <button class="control-btn" onclick="restartMQTT()">🔄 Restart MQTT</button>
        </div>

        <!-- Devices in Home Assistant -->
        <div class="card">
            <h3>Home Assistant Devices</h3>
            <p>Device ID: <code>openipc-hi3516cv300</code></p>
            
            <div class="device-grid">
                <!-- Door Sensor -->
                <div class="device-card">
                    <div class="device-name">🚪 Door Status</div>
                    <div class="device-id">openipc-hi3516cv300_door</div>
                    <div class="device-topic">doorphone/openipc-hi3516cv300/door</div>
                    <div><span class="badge badge-success">binary_sensor</span></div>
                </div>

                <!-- RFID Sensor -->
                <div class="device-card">
                    <div class="device-name">🔑 RFID Key</div>
                    <div class="device-id">openipc-hi3516cv300_rfid</div>
                    <div class="device-topic">doorphone/openipc-hi3516cv300/rfid</div>
                    <div><span class="badge badge-success">sensor</span></div>
                </div>

                <!-- Access Sensor -->
                <div class="device-card">
                    <div class="device-name">✅ Access Status</div>
                    <div class="device-id">openipc-hi3516cv300_access</div>
                    <div class="device-topic">doorphone/openipc-hi3516cv300/access</div>
                    <div><span class="badge badge-success">sensor</span></div>
                </div>

                <!-- Relay Switch -->
                <div class="device-card">
                    <div class="device-name">🔌 Door Relay</div>
                    <div class="device-id">openipc-hi3516cv300_relay</div>
                    <div class="device-topic">doorphone/openipc-hi3516cv300/relay</div>
                    <div><span class="badge badge-success">switch</span></div>
                </div>

                <!-- Exit Button -->
                <div class="device-card">
                    <div class="device-name">🚪 Exit Button</div>
                    <div class="device-id">openipc-hi3516cv300_button_exit</div>
                    <div class="device-topic">doorphone/openipc-hi3516cv300/button/exit</div>
                    <div><span class="badge badge-success">binary_sensor</span></div>
                </div>

                <!-- Call Button -->
                <div class="device-card">
                    <div class="device-name">🔔 Call Button</div>
                    <div class="device-id">openipc-hi3516cv300_button_call</div>
                    <div class="device-topic">doorphone/openipc-hi3516cv300/button/call</div>
                    <div><span class="badge badge-success">binary_sensor</span></div>
                </div>
            </div>
        </div>

        <!-- Recent Events -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin:0;">Recent MQTT Events</h3>
                <button class="btn btn-sm btn-info" onclick="refreshLog()">🔄 Refresh</button>
            </div>
            <div id="eventLog" style="max-height: 200px; overflow-y: auto; margin-top: 15px; background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 12px;">
                Loading...
            </div>
        </div>
    </div>

    <script>
        const DEVICE_ID = "openipc-hi3516cv300";
        
        function showNotification(msg, type) {
            let notif = document.getElementById('notification');
            notif.style.borderLeftColor = type === 'success' ? '#4caf50' : '#f44336';
            notif.innerHTML = msg;
            notif.style.display = 'block';
            setTimeout(() => notif.style.display = 'none', 3000);
        }

        function loadStatus() {
            fetch('/cgi-bin/p/mqtt_api.cgi?action=get_status')
                .then(r => r.json())
                .then(data => {
                    let connStatus = document.getElementById('connStatus');
                    let connDetails = document.getElementById('connDetails');
                    let connectionCard = document.getElementById('connectionCard');
                    
                    if (data.connected === 'true') {
                        connStatus.innerHTML = '✅ CONNECTED';
                        connDetails.innerHTML = `Broker: ${data.host}:${data.port}`;
                        document.getElementById('brokerStatus').innerHTML = '✅';
                    } else if (data.enabled === 'true') {
                        connStatus.innerHTML = '⏳ CONNECTING...';
                        document.getElementById('brokerStatus').innerHTML = '⏳';
                    } else {
                        connStatus.innerHTML = '❌ DISCONNECTED';
                        document.getElementById('brokerStatus').innerHTML = '❌';
                    }
                    
                    document.getElementById('publishedCount').innerHTML = data.sent || 0;
                    document.getElementById('discoveryStatus').innerHTML = data.discovery === 'true' ? '✅' : '❌';
                });
        }

        function testRelay() {
            fetch('/cgi-bin/p/mqtt_api.cgi?action=publish&topic=doorphone/' + DEVICE_ID + '/relay/set&message=ON')
                .then(r => r.json())
                .then(data => showNotification(data.message, data.status));
        }

        function resendDiscovery() {
            fetch('/cgi-bin/p/mqtt_api.cgi?action=send_discovery')
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status);
                    setTimeout(loadStatus, 1000);
                });
        }

        function restartMQTT() {
            if (confirm('Restart MQTT client?')) {
                fetch('/cgi-bin/p/mqtt_api.cgi?action=restart')
                    .then(r => r.json())
                    .then(data => {
                        showNotification(data.message, data.status);
                        setTimeout(loadStatus, 2000);
                    });
            }
        }

        function refreshLog() {
            fetch('/cgi-bin/p/mqtt_api.cgi?action=get_log&lines=20')
                .then(r => r.json())
                .then(data => {
                    let logDiv = document.getElementById('eventLog');
                    if (data.log && data.log.length) {
                        logDiv.innerHTML = data.log.map(e => 
                            `<div>${e.time} - ${e.message}</div>`
                        ).join('');
                    } else {
                        logDiv.innerHTML = 'No events';
                    }
                });
        }

        // Initial load
        loadStatus();
        refreshLog();

        // Refresh every 10 seconds
        setInterval(() => {
            loadStatus();
            refreshLog();
        }, 10000);
    </script>
</body>
</html>
HTML
