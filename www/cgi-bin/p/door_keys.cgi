#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

# Получаем список доступных звуков
SOUND_DIR="/usr/share/sounds/doorphone"
SOUNDS=""
if [ -d "$SOUND_DIR" ]; then
    SOUNDS=$(ls "$SOUND_DIR"/*.pcm 2>/dev/null | xargs -n1 basename | sed 's/\.pcm$//')
fi

# Текущие настройки звуков (можно хранить в отдельном конфиге)
SOUND_CONFIG="/etc/doorphone_sounds.conf"
SOUND_KEY_ACCEPT="beep"
SOUND_KEY_DENY="denied"
SOUND_QR_ACCEPT="beep"
SOUND_QR_DENY="denied"
SOUND_DOOR_OPEN="door_open"
SOUND_DOOR_CLOSE="door_close"
SOUND_BUTTON="beep"

if [ -f "$SOUND_CONFIG" ]; then
    . "$SOUND_CONFIG" 2>/dev/null
fi

cat << 'EOFH'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Key Management</title>
    <link rel="stylesheet" href="/a/bootstrap.min.css">
    <style>
        /* Navigation Bar */
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
            transition: all 0.3s;
            font-size: 14px;
        }
        .navbar-item:hover {
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
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
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s;
            font-size: 14px;
        }
        .home-button:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            color: white;
            text-decoration: none;
        }
        
        body { background: #f5f5f5; padding: 0; margin: 0; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        
        .card { 
            background: white; 
            border-radius: 10px; 
            padding: 25px; 
            margin-bottom: 25px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .card:hover { box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
        
        /* Door Status Card */
        .door-status-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            position: relative;
            overflow: hidden;
        }
        .door-status-card::before {
            content: '🚪';
            position: absolute;
            right: 20px;
            bottom: -20px;
            font-size: 120px;
            opacity: 0.1;
            transform: rotate(-10deg);
        }
        .door-status {
            display: flex;
            align-items: center;
            gap: 30px;
            flex-wrap: wrap;
        }
        .door-indicator {
            width: 120px;
            height: 120px;
            border-radius: 60px;
            background: rgba(255,255,255,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            backdrop-filter: blur(10px);
            border: 3px solid white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .door-info {
            flex: 1;
        }
        .door-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .door-state {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .door-last-change {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .control-panel {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .door-btn {
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .door-btn.open {
            background: #4caf50;
            color: white;
        }
        .door-btn.open:hover {
            background: #45a049;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(76,175,80,0.4);
        }
        .door-btn.close {
            background: #f44336;
            color: white;
        }
        .door-btn.close:hover {
            background: #da190b;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(244,67,54,0.4);
        }
        .door-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }
        
        .esp-status {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        .esp-status.connected {
            background: #4caf50;
            color: white;
        }
        .esp-status.disconnected {
            background: #f44336;
            color: white;
        }
        .esp-status.detected {
            background: #ff9800;
            color: white;
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
        
        .keys-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .keys-table th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #495057;
            border-bottom: 2px solid #dee2e6;
        }
        .keys-table td {
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
            vertical-align: middle;
        }
        .keys-table tr:hover {
            background: #f8f9fa;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-permanent {
            background: #4caf50;
            color: white;
        }
        .badge-temporary {
            background: #ff9800;
            color: white;
        }
        .badge-expired {
            background: #f44336;
            color: white;
        }
        
        .connection-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        .connection-indicator.connected {
            background: #4caf50;
            box-shadow: 0 0 10px #4caf50;
        }
        .connection-indicator.disconnected {
            background: #f44336;
            box-shadow: 0 0 10px #f44336;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .sound-settings {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .sound-row {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        .sound-row label {
            min-width: 150px;
            font-weight: 500;
        }
        .sound-select {
            flex: 1;
            min-width: 200px;
        }
        .sound-preview {
            display: flex;
            gap: 5px;
        }
        
        .add-key-form {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .form-row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: flex-end;
        }
        .form-group {
            flex: 1;
            min-width: 200px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #495057;
            font-size: 14px;
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
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
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
        .btn-warning {
            background: #ff9800;
            color: white;
        }
        .btn-warning:hover {
            background: #e68900;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255,152,0,0.3);
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
        .btn-sm {
            padding: 8px 16px;
            font-size: 12px;
        }
        
        .door-history {
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            max-height: 150px;
            overflow-y: auto;
        }
        .history-item {
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: white;
        }
        .history-item:last-child {
            border-bottom: none;
        }
        .history-time {
            color: rgba(255,255,255,0.7);
            min-width: 80px;
        }
        
        .search-box {
            position: relative;
            margin-bottom: 20px;
        }
        .search-box input {
            width: 100%;
            padding: 12px 20px;
            padding-right: 40px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
            box-sizing: border-box;
        }
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
        }
        .search-box i {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #6c757d;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal.active {
            display: flex;
        }
        .modal-content {
            background: white;
            border-radius: 10px;
            padding: 30px;
            max-width: 400px;
            width: 90%;
            animation: modalSlideIn 0.3s ease;
        }
        @keyframes modalSlideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        .modal-title {
            font-size: 20px;
            margin-bottom: 20px;
            color: #333;
        }
        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-top: 20px;
        }
        
        .notification {
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 15px 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: none;
            z-index: 1000;
            animation: slideIn 0.3s ease;
            border-left: 4px solid;
        }
        .notification.success {
            border-left-color: #4caf50;
        }
        .notification.error {
            border-left-color: #f44336;
        }
        .notification.warning {
            border-left-color: #ff9800;
        }
        .notification.info {
            border-left-color: #17a2b8;
        }
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
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
            .door-status {
                flex-direction: column;
                text-align: center;
            }
            .door-indicator {
                margin: 0 auto;
            }
            .control-panel {
                justify-content: center;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .form-row {
                flex-direction: column;
            }
            .form-group {
                width: 100%;
            }
            .sound-row {
                flex-direction: column;
                align-items: stretch;
            }
            .sound-row label {
                min-width: auto;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar">
        <div class="navbar-container">
            <a href="/cgi-bin/status.cgi" class="navbar-brand">
                <span style="font-size: 28px;">🏠</span>
                <span>OpenIPC Doorphone</span>
            </a>
            
            <div class="navbar-menu">
                <a href="/cgi-bin/status.cgi" class="navbar-item">
                    <span>🏠</span> Home
                </a>
                <a href="/cgi-bin/p/door_keys.cgi" class="navbar-item active">
                    <span>🔑</span> Keys
                </a>
                <a href="/cgi-bin/p/sip_manager.cgi" class="navbar-item">
                    <span>📞</span> SIP
                </a>
                <a href="/cgi-bin/p/qr_generator.cgi" class="navbar-item">
                    <span>🎯</span> QR
                </a>
                <a href="/cgi-bin/p/temp_keys.cgi" class="navbar-item">
                    <span>⏱️</span> Temporary
                </a>
                <a href="/cgi-bin/p/sounds.cgi" class="navbar-item">
                    <span>🔊</span> Sounds
                </a>
                <a href="/cgi-bin/p/door_history.cgi" class="navbar-item">
                    <span>📋</span> History
                </a>
                <a href="/cgi-bin/p/mqtt.cgi" class="navbar-item">
                    <span>📡</span> MQTT
                </a>
                <a href="/cgi-bin/backup.cgi" class="navbar-item">
                    <span>💾</span> Backups
                </a>
            </div>
            
            <a href="/cgi-bin/status.cgi" class="home-button">
                <span>⬅️</span> Back to Home
            </a>
        </div>
    </nav>

    <div class="container">
        <!-- Notification -->
        <div id="notification" class="notification"></div>
        
        <!-- Door Status and Control -->
        <div class="card door-status-card">
            <div class="door-status">
                <div class="door-indicator" id="doorIndicator">
                    🚪
                </div>
                <div class="door-info">
                    <div class="door-title">🚪 Door Status</div>
                    <div class="door-state" id="doorState">Loading...</div>
                    <div class="door-last-change" id="doorLastChange"></div>
                    
                    <div class="control-panel">
                        <button class="door-btn open" onclick="controlDoor('open')" id="openDoorBtn">
                            <span>🔓</span> Open Door
                        </button>
                        <button class="door-btn close" onclick="controlDoor('close')" id="closeDoorBtn">
                            <span>🔒</span> Close Door
                        </button>
                        <button class="btn btn-info" onclick="toggleDoor()" id="toggleDoorBtn">
                            <span>🔄</span> Toggle
                        </button>
                    </div>
                    
                    <div style="margin-top: 15px;">
                        <span id="espStatus" class="esp-status disconnected">
                            <span class="connection-indicator disconnected"></span>
                            ESP: Checking...
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Recent Door Actions -->
            <div class="door-history" id="doorHistory">
                <div style="text-align: center;">Loading history...</div>
            </div>
        </div>
        
        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Total Keys</div>
                <div class="stat-value" id="totalKeys">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Permanent</div>
                <div class="stat-value" style="color: #4caf50;" id="permanentKeys">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Temporary</div>
                <div class="stat-value" style="color: #ff9800;" id="temporaryKeys">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Opens Today</div>
                <div class="stat-value" style="color: #17a2b8;" id="openToday">0</div>
            </div>
        </div>

        <!-- Sound Settings -->
        <div class="card">
            <h3>🔊 Sound Settings</h3>
            <div class="sound-settings">
                <div class="sound-row">
                    <label>RFID Key Accepted:</label>
                    <div class="sound-select">
                        <select id="soundKeyAccept" class="form-control">
                            <option value="beep">Beep</option>
                            <option value="door_open">Door Open</option>
                            <option value="door_close">Door Close</option>
                            <option value="denied">Denied</option>
                            <option value="ring">Ring</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                    <div class="sound-preview">
                        <button class="btn btn-sm btn-info" onclick="playSound('keyAccept')">▶️ Test</button>
                    </div>
                </div>
                
                <div class="sound-row">
                    <label>RFID Key Denied:</label>
                    <div class="sound-select">
                        <select id="soundKeyDeny" class="form-control">
                            <option value="denied">Denied</option>
                            <option value="beep">Beep</option>
                            <option value="door_open">Door Open</option>
                            <option value="door_close">Door Close</option>
                            <option value="ring">Ring</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                    <div class="sound-preview">
                        <button class="btn btn-sm btn-info" onclick="playSound('keyDeny')">▶️ Test</button>
                    </div>
                </div>
                
                <div class="sound-row">
                    <label>QR Code Accepted:</label>
                    <div class="sound-select">
                        <select id="soundQRAccept" class="form-control">
                            <option value="beep">Beep</option>
                            <option value="door_open">Door Open</option>
                            <option value="door_close">Door Close</option>
                            <option value="denied">Denied</option>
                            <option value="ring">Ring</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                    <div class="sound-preview">
                        <button class="btn btn-sm btn-info" onclick="playSound('qrAccept')">▶️ Test</button>
                    </div>
                </div>
                
                <div class="sound-row">
                    <label>QR Code Denied:</label>
                    <div class="sound-select">
                        <select id="soundQRDeny" class="form-control">
                            <option value="denied">Denied</option>
                            <option value="beep">Beep</option>
                            <option value="door_open">Door Open</option>
                            <option value="door_close">Door Close</option>
                            <option value="ring">Ring</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                    <div class="sound-preview">
                        <button class="btn btn-sm btn-info" onclick="playSound('qrDeny')">▶️ Test</button>
                    </div>
                </div>
                
                <div class="sound-row">
                    <label>Door Open:</label>
                    <div class="sound-select">
                        <select id="soundDoorOpen" class="form-control">
                            <option value="door_open">Door Open</option>
                            <option value="beep">Beep</option>
                            <option value="door_close">Door Close</option>
                            <option value="denied">Denied</option>
                            <option value="ring">Ring</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                    <div class="sound-preview">
                        <button class="btn btn-sm btn-info" onclick="playSound('doorOpen')">▶️ Test</button>
                    </div>
                </div>
                
                <div class="sound-row">
                    <label>Door Close:</label>
                    <div class="sound-select">
                        <select id="soundDoorClose" class="form-control">
                            <option value="door_close">Door Close</option>
                            <option value="beep">Beep</option>
                            <option value="door_open">Door Open</option>
                            <option value="denied">Denied</option>
                            <option value="ring">Ring</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                    <div class="sound-preview">
                        <button class="btn btn-sm btn-info" onclick="playSound('doorClose')">▶️ Test</button>
                    </div>
                </div>
                
                <div class="sound-row">
                    <label>Button Press:</label>
                    <div class="sound-select">
                        <select id="soundButton" class="form-control">
                            <option value="beep">Beep</option>
                            <option value="door_open">Door Open</option>
                            <option value="door_close">Door Close</option>
                            <option value="denied">Denied</option>
                            <option value="ring">Ring</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                    <div class="sound-preview">
                        <button class="btn btn-sm btn-info" onclick="playSound('button')">▶️ Test</button>
                    </div>
                </div>
                
                <div style="margin-top: 15px;">
                    <button class="btn btn-primary" onclick="saveSoundSettings()">💾 Save Sound Settings</button>
                </div>
            </div>
        </div>
        
        <!-- Search -->
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Search by key, owner or date...">
            <i>🔍</i>
        </div>
        
        <!-- Add Key Form -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">➕ Add New Key</h3>
            <div class="add-key-form">
                <div class="form-row">
                    <div class="form-group">
                        <label>Key Number *</label>
                        <input type="text" id="keyValue" class="form-control" placeholder="e.g., 12345678">
                    </div>
                    <div class="form-group">
                        <label>Owner Name *</label>
                        <input type="text" id="ownerName" class="form-control" placeholder="e.g., John Doe">
                    </div>
                    <div class="form-group">
                        <label>Key Type</label>
                        <select id="keyType" class="form-control">
                            <option value="permanent">🔒 Permanent</option>
                            <option value="temporary">⏱️ Temporary (24 hours)</option>
                            <option value="temporary_week">📅 Temporary (7 days)</option>
                            <option value="temporary_month">📆 Temporary (30 days)</option>
                        </select>
                    </div>
                    <div>
                        <button class="btn btn-success" onclick="addKey()">
                            ✨ Add Key
                        </button>
                    </div>
                </div>
                <div id="addProgress" class="progress" style="display: none; margin-top: 15px;">
                    <div class="progress-bar" style="width: 0%;" id="addProgressBar"></div>
                </div>
            </div>
        </div>
        
        <!-- Keys Table -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0;">📋 Key List</h3>
                <div>
                    <button class="btn btn-primary btn-sm" onclick="refreshKeys()">
                        🔄 Refresh
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="showClearModal()">
                        🗑️ Clear Expired
                    </button>
                </div>
            </div>
            
            <div style="overflow-x: auto;">
                <table class="keys-table" id="keysTable">
                    <thead>
                        <tr>
                            <th>Key</th>
                            <th>Owner</th>
                            <th>Type</th>
                            <th>Added Date</th>
                            <th>Expiry</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="keysList">
                        <tr>
                            <td colspan="7" style="text-align: center; padding: 40px;">
                                <p style="color: #666;">Loading keys...</p>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Confirmation Modal -->
    <div class="modal" id="confirmModal">
        <div class="modal-content">
            <h3 class="modal-title" id="modalTitle">Confirmation</h3>
            <p id="modalMessage">Are you sure?</p>
            <div class="modal-buttons">
                <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button class="btn btn-danger" id="modalConfirmBtn">Confirm</button>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let keys = [];
        let filteredKeys = [];
        let lastESPStatus = 'disconnected';
        let doorState = 'unknown';
        let doorHistory = [];
        let deleteCallback = null;
        let statusInterval = null;
        
        // Sound settings
        let soundSettings = {
            keyAccept: 'beep',
            keyDeny: 'denied',
            qrAccept: 'beep',
            qrDeny: 'denied',
            doorOpen: 'door_open',
            doorClose: 'door_close',
            button: 'beep'
        };
        
        // Load on start
        document.addEventListener('DOMContentLoaded', function() {
            loadStatus();
            loadKeys();
            loadDoorHistory();
            loadDoorStats();
            loadSoundSettings();
            
            // Update every 3 seconds
            statusInterval = setInterval(updateDoorStatus, 3000);
            
            // Search
            document.getElementById('searchInput').addEventListener('input', filterKeys);
        });
        
        // Load sound settings
        function loadSoundSettings() {
            // Здесь можно загрузить из конфига
            // Пока используем значения по умолчанию
            document.getElementById('soundKeyAccept').value = 'beep';
            document.getElementById('soundKeyDeny').value = 'denied';
            document.getElementById('soundQRAccept').value = 'beep';
            document.getElementById('soundQRDeny').value = 'denied';
            document.getElementById('soundDoorOpen').value = 'door_open';
            document.getElementById('soundDoorClose').value = 'door_close';
            document.getElementById('soundButton').value = 'beep';
        }
        
        // Save sound settings
        function saveSoundSettings() {
            soundSettings = {
                keyAccept: document.getElementById('soundKeyAccept').value,
                keyDeny: document.getElementById('soundKeyDeny').value,
                qrAccept: document.getElementById('soundQRAccept').value,
                qrDeny: document.getElementById('soundQRDeny').value,
                doorOpen: document.getElementById('soundDoorOpen').value,
                doorClose: document.getElementById('soundDoorClose').value,
                button: document.getElementById('soundButton').value
            };
            
            // Здесь можно сохранить в конфиг через API
            showNotification('Sound settings saved', 'success');
        }
        
        // Play test sound
        function playSound(type) {
            let sound = '';
            switch(type) {
                case 'keyAccept':
                    sound = document.getElementById('soundKeyAccept').value;
                    break;
                case 'keyDeny':
                    sound = document.getElementById('soundKeyDeny').value;
                    break;
                case 'qrAccept':
                    sound = document.getElementById('soundQRAccept').value;
                    break;
                case 'qrDeny':
                    sound = document.getElementById('soundQRDeny').value;
                    break;
                case 'doorOpen':
                    sound = document.getElementById('soundDoorOpen').value;
                    break;
                case 'doorClose':
                    sound = document.getElementById('soundDoorClose').value;
                    break;
                case 'button':
                    sound = document.getElementById('soundButton').value;
                    break;
            }
            
            if (sound && sound !== 'none') {
                fetch('/cgi-bin/p/play_sound.cgi?name=' + sound)
                    .then(() => showNotification('Playing: ' + sound, 'info'))
                    .catch(() => showNotification('Failed to play sound', 'error'));
            }
        }
        
        // Notifications
        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.className = 'notification ' + type;
            notification.innerHTML = message;
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }
        
        // Modal
        function showModal(title, message, onConfirm) {
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalMessage').textContent = message;
            document.getElementById('confirmModal').classList.add('active');
            deleteCallback = onConfirm;
        }
        
        function closeModal() {
            document.getElementById('confirmModal').classList.remove('active');
            deleteCallback = null;
        }
        
        function confirmAction() {
            if (deleteCallback) {
                deleteCallback();
                closeModal();
            }
        }
        
        // Door control
        function controlDoor(action) {
            const espStatus = document.getElementById('espStatus');
            
            if (lastESPStatus !== 'connected') {
                showNotification('❌ ESP not connected', 'error');
                return;
            }
            
            const btn = action === 'open' ? 'openDoorBtn' : 'closeDoorBtn';
            document.getElementById(btn).disabled = true;
            
            fetch('/cgi-bin/p/door_api.cgi?action=control_door&cmd=' + action)
                .then(r => r.json())
                .then(data => {
                    document.getElementById(btn).disabled = false;
                    
                    if (data.status === 'success') {
                        showNotification('✅ ' + data.message, 'success');
                        updateDoorStatus();
                        loadDoorHistory();
                    } else {
                        showNotification('❌ ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    document.getElementById(btn).disabled = false;
                    showNotification('❌ Error: ' + error, 'error');
                });
        }
        
        // Toggle door
        function toggleDoor() {
            if (doorState === 'open') {
                controlDoor('close');
            } else if (doorState === 'closed') {
                controlDoor('open');
            } else {
                showNotification('❌ Unknown door state', 'error');
            }
        }
        
        // Update door status
        function updateDoorStatus() {
            fetch('/cgi-bin/p/door_api.cgi?action=get_door_status')
                .then(r => r.json())
                .then(data => {
                    // Update ESP status
                    fetch('/cgi-bin/p/door_api.cgi?action=get_status')
                        .then(r => r.json())
                        .then(statusData => {
                            const espDiv = document.getElementById('espStatus');
                            const indicator = espDiv.querySelector('.connection-indicator');
                            
                            if (statusData.esp === 'connected') {
                                espDiv.className = 'esp-status connected';
                                indicator.className = 'connection-indicator connected';
                                espDiv.innerHTML = '<span class="connection-indicator connected"></span> ESP: Connected ✅';
                                lastESPStatus = 'connected';
                                
                                document.getElementById('openDoorBtn').disabled = false;
                                document.getElementById('closeDoorBtn').disabled = false;
                                document.getElementById('toggleDoorBtn').disabled = false;
                            } else {
                                espDiv.className = 'esp-status disconnected';
                                indicator.className = 'connection-indicator disconnected';
                                espDiv.innerHTML = '<span class="connection-indicator disconnected"></span> ESP: Not Connected ❌';
                                lastESPStatus = 'disconnected';
                                
                                document.getElementById('openDoorBtn').disabled = true;
                                document.getElementById('closeDoorBtn').disabled = true;
                                document.getElementById('toggleDoorBtn').disabled = true;
                            }
                        });
                    
                    // Update door state
                    if (data.door) {
                        doorState = data.door;
                        const doorElement = document.getElementById('doorState');
                        const indicatorElement = document.getElementById('doorIndicator');
                        
                        if (data.door === 'open') {
                            doorElement.innerHTML = '🚪 Door OPEN';
                            doorElement.style.color = '#4caf50';
                            indicatorElement.innerHTML = '🔓';
                        } else if (data.door === 'closed') {
                            doorElement.innerHTML = '🚪 Door CLOSED';
                            doorElement.style.color = '#f44336';
                            indicatorElement.innerHTML = '🔒';
                        } else {
                            doorElement.innerHTML = '🚪 Unknown';
                            doorElement.style.color = '#ff9800';
                            indicatorElement.innerHTML = '❓';
                        }
                    }
                    
                    if (data.last_change) {
                        document.getElementById('doorLastChange').innerHTML = `Last change: ${data.last_change}`;
                    }
                })
                .catch(error => {
                    console.error('Door status error:', error);
                });
        }
        
        // Load ESP status
        function loadStatus() {
            fetch('/cgi-bin/p/door_api.cgi?action=get_status')
                .then(r => r.json())
                .then(data => {
                    const espDiv = document.getElementById('espStatus');
                    const indicator = espDiv.querySelector('.connection-indicator');
                    
                    if (data.esp === 'connected') {
                        espDiv.className = 'esp-status connected';
                        indicator.className = 'connection-indicator connected';
                        espDiv.innerHTML = '<span class="connection-indicator connected"></span> ESP: Connected ✅';
                        lastESPStatus = 'connected';
                        
                        document.getElementById('openDoorBtn').disabled = false;
                        document.getElementById('closeDoorBtn').disabled = false;
                        document.getElementById('toggleDoorBtn').disabled = false;
                    } else {
                        espDiv.className = 'esp-status disconnected';
                        indicator.className = 'connection-indicator disconnected';
                        espDiv.innerHTML = '<span class="connection-indicator disconnected"></span> ESP: Not Connected ❌';
                        lastESPStatus = 'disconnected';
                        
                        document.getElementById('openDoorBtn').disabled = true;
                        document.getElementById('closeDoorBtn').disabled = true;
                        document.getElementById('toggleDoorBtn').disabled = true;
                    }
                    
                    document.getElementById('totalKeys').textContent = data.keys || 0;
                })
                .catch(error => {
                    console.error('Status error:', error);
                });
        }
        
        // Load door history
        function loadDoorHistory() {
            fetch('/cgi-bin/p/door_api.cgi?action=get_door_history&lines=10')
                .then(r => r.json())
                .then(data => {
                    const events = data.events || [];
                    let html = '';
                    
                    events.forEach(event => {
                        const time = event.time || '';
                        const action = event.action || '';
                        
                        html += '<div class="history-item">' +
                            '<span class="history-time">' + time + '</span>' +
                            '<span>' + action + '</span>' +
                            '</div>';
                    });
                    
                    if (html === '') {
                        html = '<div style="text-align: center;">📭 No history</div>';
                    }
                    
                    document.getElementById('doorHistory').innerHTML = html;
                })
                .catch(error => {
                    console.error('Door history error:', error);
                });
        }
        
        // Load door stats
        function loadDoorStats() {
            fetch('/cgi-bin/p/door_api.cgi?action=get_door_stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('openToday').textContent = data.open_today || 0;
                })
                .catch(error => {
                    console.error('Door stats error:', error);
                });
        }
        
        // Load keys
        function loadKeys() {
            fetch('/cgi-bin/p/door_api.cgi?action=list_keys')
                .then(r => r.json())
                .then(data => {
                    keys = data.keys || [];
                    filterKeys();
                    updateStats();
                })
                .catch(error => {
                    console.error('Keys error:', error);
                    document.getElementById('keysList').innerHTML = `
                        <tr>
                            <td colspan="7" style="text-align: center; padding: 40px; color: #f44336;">
                                ❌ Error loading keys
                            </td>
                        </tr>
                    `;
                });
        }
        
        // Filter keys
        function filterKeys() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            filteredKeys = keys.filter(key => {
                return key.key.toLowerCase().includes(searchTerm) ||
                       (key.owner || '').toLowerCase().includes(searchTerm) ||
                       (key.date || '').includes(searchTerm);
            });
            
            renderKeys();
        }
        
        // Update key statistics
        function updateStats() {
            const now = Math.floor(Date.now() / 1000);
            let permanent = 0;
            let temporary = 0;
            
            keys.forEach(key => {
                if (key.expiry) {
                    temporary++;
                } else {
                    permanent++;
                }
            });
            
            document.getElementById('permanentKeys').textContent = permanent;
            document.getElementById('temporaryKeys').textContent = temporary;
        }
        
        // Format date
        function formatDate(dateStr) {
            if (!dateStr) return '-';
            try {
                const date = new Date(dateStr);
                return date.toLocaleString('en-US', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            } catch (e) {
                return dateStr;
            }
        }
        
        // Format expiry
        function formatExpiry(expiry) {
            if (!expiry) return '<span class="badge badge-permanent">Permanent</span>';
            
            const now = Math.floor(Date.now() / 1000);
            const expiryNum = parseInt(expiry);
            
            if (expiryNum < now) {
                return '<span class="badge badge-expired">Expired</span>';
            }
            
            const daysLeft = Math.ceil((expiryNum - now) / 86400);
            const hoursLeft = Math.ceil((expiryNum - now) / 3600);
            
            if (daysLeft > 1) {
                return `<span class="badge badge-temporary">${daysLeft} days left</span>`;
            } else {
                return `<span class="badge badge-temporary">${hoursLeft} hours left</span>`;
            }
        }
        
        // Render keys
        function renderKeys() {
            if (filteredKeys.length === 0) {
                document.getElementById('keysList').innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align: center; padding: 40px; color: #666;">
                            🔍 No keys found
                        </td>
                    </tr>
                `;
                return;
            }
            
            let html = '';
            filteredKeys.forEach(key => {
                html += '<tr>' +
                    '<td><strong>' + key.key + '</strong></td>' +
                    '<td>' + (key.owner || 'Unknown') + '</td>' +
                    '<td>' + (key.expiry ? '⏱️ Temporary' : '🔒 Permanent') + '</td>' +
                    '<td>' + formatDate(key.date) + '</td>' +
                    '<td>' + formatExpiry(key.expiry) + '</td>' +
                    '<td><span class="badge badge-permanent">Active</span></td>' +
                    '<td>' +
                        '<button class="btn btn-danger btn-sm" onclick="deleteKey(\'' + key.key + '\')">🗑️</button>' +
                    '</td>' +
                    '</tr>';
            });
            
            document.getElementById('keysList').innerHTML = html;
        }
        
        // Add key
        function addKey() {
            const key = document.getElementById('keyValue').value.trim();
            const owner = document.getElementById('ownerName').value.trim();
            const type = document.getElementById('keyType').value;
            
            if (!key || !owner) {
                showNotification('❌ Please fill all fields', 'error');
                return;
            }
            
            const progress = document.getElementById('addProgress');
            const progressBar = document.getElementById('addProgressBar');
            progress.style.display = 'block';
            progressBar.style.width = '50%';
            
            let expiry = '';
            const now = Math.floor(Date.now() / 1000);
            
            if (type === 'temporary') {
                expiry = now + 86400;
            } else if (type === 'temporary_week') {
                expiry = now + 604800;
            } else if (type === 'temporary_month') {
                expiry = now + 2592000;
            }
            
            const body = `action=add_key&key=${encodeURIComponent(key)}&owner=${encodeURIComponent(owner)}${expiry ? '&expiry=' + expiry : ''}`;
            
            fetch('/cgi-bin/p/door_api.cgi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: body
            })
            .then(r => r.json())
            .then(data => {
                progressBar.style.width = '100%';
                setTimeout(() => {
                    progress.style.display = 'none';
                    progressBar.style.width = '0%';
                }, 500);
                
                if (data.status === 'success') {
                    showNotification('✅ ' + data.message, 'success');
                    document.getElementById('keyValue').value = '';
                    document.getElementById('ownerName').value = '';
                    loadKeys();
                    
                    // Play sound based on result
                    playSound('keyAccept');
                } else {
                    showNotification('❌ ' + data.message, 'error');
                    playSound('keyDeny');
                }
            })
            .catch(error => {
                progress.style.display = 'none';
                showNotification('❌ Error: ' + error, 'error');
                playSound('keyDeny');
            });
        }
        
        // Delete key
        function deleteKey(key) {
            showModal(
                'Delete Key',
                `Are you sure you want to delete key ${key}?`,
                function() {
                    fetch('/cgi-bin/p/door_api.cgi', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: 'action=remove_key&key=' + encodeURIComponent(key)
                    })
                    .then(r => r.json())
                    .then(data => {
                        if (data.status === 'success') {
                            showNotification('✅ ' + data.message, 'success');
                            loadKeys();
                        } else {
                            showNotification('❌ ' + data.message, 'error');
                        }
                    })
                    .catch(error => {
                        showNotification('❌ Error: ' + error, 'error');
                    });
                }
            );
        }
        
        // Clear expired keys
        function showClearModal() {
            const now = Math.floor(Date.now() / 1000);
            let expiredCount = 0;
            
            keys.forEach(key => {
                if (key.expiry && parseInt(key.expiry) < now) {
                    expiredCount++;
                }
            });
            
            if (expiredCount === 0) {
                showNotification('ℹ️ No expired keys', 'info');
                return;
            }
            
            showModal(
                'Clear Expired Keys',
                `Delete ${expiredCount} expired key(s)?`,
                function() {
                    fetch('/cgi-bin/p/door_api.cgi?action=clean_temp_keys')
                        .then(r => r.json())
                        .then(data => {
                            if (data.status === 'success') {
                                showNotification(`✅ Removed ${data.removed} expired keys`, 'success');
                                loadKeys();
                            } else {
                                showNotification('❌ ' + data.message, 'error');
                            }
                        })
                        .catch(error => {
                            showNotification('❌ Error: ' + error, 'error');
                        });
                }
            );
        }
        
        // Refresh keys
        function refreshKeys() {
            loadKeys();
            loadStatus();
            loadDoorHistory();
            loadDoorStats();
            showNotification('🔄 Data refreshed', 'success');
        }
    </script>
</body>
</html>
EOFH
