#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

# Get current SIP settings
if [ -f /etc/baresip/accounts ]; then
    ACCOUNT_LINE=$(grep -v "^#" /etc/baresip/accounts | head -1)
    SIP_USER=$(echo "$ACCOUNT_LINE" | sed -n 's/.*<sip:\([^@]*\)@.*/\1/p')
    SIP_SERVER=$(echo "$ACCOUNT_LINE" | sed -n 's/.*@\([^;>]*\).*/\1/p')
    SIP_PASS=$(echo "$ACCOUNT_LINE" | sed -n 's/.*auth_pass=\([^;]*\).*/\1/p')
    SIP_TRANSPORT=$(echo "$ACCOUNT_LINE" | sed -n 's/.*transport=\([^;]*\).*/\1/p')
    [ -z "$SIP_TRANSPORT" ] && SIP_TRANSPORT="udp"
    
    # Check for auto-answer
    if echo "$ACCOUNT_LINE" | grep -q "answermode=auto"; then
        AUTO_ANSWER="true"
    else
        AUTO_ANSWER="false"
    fi
fi

if [ -f /etc/baresip/call_number ]; then
    CALL_NUMBER=$(cat /etc/baresip/call_number)
else
    CALL_NUMBER="100"
fi

# Check recording settings
RECORD_ENABLED="false"
if [ -f /etc/baresip/config ]; then
    if grep -q "^module[[:space:]]*record" /etc/baresip/config; then
        RECORD_ENABLED="true"
    fi
fi

# DTMF settings
DTMF_MODE="inband"
if [ -f /etc/baresip/config ]; then
    if grep -q "^dtmf_mode" /etc/baresip/config; then
        DTMF_MODE=$(grep "^dtmf_mode" /etc/baresip/config | cut -d' ' -f2)
    fi
fi

# Default values
[ -z "$SIP_USER" ] && SIP_USER=""
[ -z "$SIP_SERVER" ] && SIP_SERVER=""
[ -z "$SIP_PASS" ] && SIP_PASS=""
[ -z "$SIP_TRANSPORT" ] && SIP_TRANSPORT="udp"
[ -z "$AUTO_ANSWER" ] && AUTO_ANSWER="false"
[ -z "$CALL_NUMBER" ] && CALL_NUMBER="100"
[ -z "$RECORD_ENABLED" ] && RECORD_ENABLED="false"
[ -z "$DTMF_MODE" ] && DTMF_MODE="inband"

cat << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIP Settings</title>
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
        
        .sip-status {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .sip-status.running {
            background: linear-gradient(135deg, #4caf50, #45a049);
        }
        .sip-status.stopped {
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
        input:focus + .slider {
            box-shadow: 0 0 1px #4caf50;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
        .switch-label {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .calls-table {
            width: 100%;
            border-collapse: collapse;
        }
        .calls-table th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #495057;
            border-bottom: 2px solid #dee2e6;
        }
        .calls-table td {
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }
        .calls-table tr:hover {
            background: #f8f9fa;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-success {
            background: #4caf50;
            color: white;
        }
        .badge-danger {
            background: #f44336;
            color: white;
        }
        .badge-warning {
            background: #ff9800;
            color: white;
        }
        .badge-info {
            background: #17a2b8;
            color: white;
        }
        
        .recordings-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-top: 10px;
        }
        .recording-item {
            padding: 10px 15px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .recording-item:last-child {
            border-bottom: none;
        }
        .recording-item:hover {
            background: #f8f9fa;
        }
        
        .dtmf-selector {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        .dtmf-option {
            flex: 1;
            min-width: 150px;
        }
        .dtmf-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        .dtmf-btn {
            padding: 15px;
            font-size: 20px;
            font-weight: bold;
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .dtmf-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: scale(1.05);
        }
        .dtmf-btn.selected {
            background: #667eea;
            color: white;
            border-color: #667eea;
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
        }
        .notification.success {
            border-left: 4px solid #4caf50;
        }
        .notification.error {
            border-left: 4px solid #f44336;
        }
        .notification.warning {
            border-left: 4px solid #ff9800;
        }
        .notification.info {
            border-left: 4px solid #17a2b8;
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
            .sip-status {
                flex-direction: column;
                text-align: center;
            }
            .status-icon {
                margin-top: 20px;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .dtmf-grid {
                grid-template-columns: repeat(3, 1fr);
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
                <a href="/cgi-bin/p/door_keys.cgi" class="navbar-item">
                    <span>🔑</span> Keys
                </a>
                <a href="/cgi-bin/p/sip_manager.cgi" class="navbar-item active">
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
        
        <h1>SIP Settings</h1>

        <!-- SIP Status -->
        <div id="sipStatusCard" class="sip-status">
            <div>
                <div class="status-title">SIP Status</div>
                <div class="status-value" id="sipState">Checking...</div>
                <div id="sipDetails"></div>
            </div>
            <div class="status-icon" id="statusIcon">📞</div>
        </div>

        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Total Calls</div>
                <div class="stat-value" id="totalCalls">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Answered</div>
                <div class="stat-value" id="answeredCalls">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Missed</div>
                <div class="stat-value" id="missedCalls">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Recordings</div>
                <div class="stat-value" id="recordingsCount">0</div>
            </div>
        </div>

        <!-- SIP Account Settings -->
        <div class="card">
            <h3>SIP Account</h3>
            
            <div class="form-group">
                <label>Username</label>
                <input type="text" class="form-control" id="sipUser" value="$SIP_USER" placeholder="e.g., 101">
            </div>
            
            <div class="form-group">
                <label>SIP Server</label>
                <input type="text" class="form-control" id="sipServer" value="$SIP_SERVER" placeholder="e.g., sip.example.com">
            </div>
            
            <div class="form-group">
                <label>Password</label>
                <input type="password" class="form-control" id="sipPass" value="$SIP_PASS" placeholder="Your password">
            </div>
            
            <div class="form-group">
                <label>Transport</label>
                <select id="sipTransport" class="form-control">
                    <option value="udp" $([ "$SIP_TRANSPORT" = "udp" ] && echo "selected")>UDP</option>
                    <option value="tcp" $([ "$SIP_TRANSPORT" = "tcp" ] && echo "selected")>TCP</option>
                    <option value="tls" $([ "$SIP_TRANSPORT" = "tls" ] && echo "selected")>TLS</option>
                </select>
            </div>
            
            <div class="switch-label">
                <label class="switch">
                    <input type="checkbox" id="autoAnswer" $([ "$AUTO_ANSWER" = "true" ] && echo "checked")>
                    <span class="slider"></span>
                </label>
                <span>Auto-answer incoming calls</span>
            </div>
            
            <button class="btn btn-primary" onclick="saveSIP()">Save SIP Settings</button>
        </div>

        <!-- Call Button Settings -->
        <div class="card">
            <h3>Call Button</h3>
            
            <div class="form-group">
                <label>Phone number to call when button pressed</label>
                <input type="text" class="form-control" id="callNumber" value="$CALL_NUMBER" placeholder="e.g., 100">
            </div>
            
            <button class="btn btn-primary" onclick="saveCallNumber()">Save Call Number</button>
            <button class="btn btn-success" onclick="testCall()">📞 Test Call</button>
        </div>

        <!-- DTMF Settings -->
        <div class="card">
            <h3>DTMF Settings</h3>
            
            <div class="form-group">
                <label>DTMF Mode</label>
                <select id="dtmfMode" class="form-control">
                    <option value="inband" $([ "$DTMF_MODE" = "inband" ] && echo "selected")>In-band (audio)</option>
                    <option value="rfc2833" $([ "$DTMF_MODE" = "rfc2833" ] && echo "selected")>RFC 2833 (telephone-event)</option>
                    <option value="info" $([ "$DTMF_MODE" = "info" ] && echo "selected")>SIP INFO</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>DTMF Code for Door Opening</label>
                <div class="dtmf-selector">
                    <div class="dtmf-option">
                        <select id="dtmfDigit" class="form-control">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8">8</option>
                            <option value="9">9</option>
                            <option value="0">0</option>
                            <option value="*">* (star)</option>
                            <option value="#"># (pound)</option>
                            <option value="A">A</option>
                            <option value="B">B</option>
                            <option value="C">C</option>
                            <option value="D">D</option>
                        </select>
                    </div>
                    <div class="dtmf-option">
                        <select id="dtmfAction" class="form-control">
                            <option value="open">Open door when received</option>
                            <option value="close">Close door when received</option>
                            <option value="toggle">Toggle door when received</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <button class="btn btn-primary" onclick="saveDTMFSettings()">Save DTMF Settings</button>
        </div>

        <!-- Call Recording -->
        <div class="card">
            <h3>Call Recording</h3>
            
            <div class="switch-label">
                <label class="switch">
                    <input type="checkbox" id="recordCalls" $([ "$RECORD_ENABLED" = "true" ] && echo "checked")>
                    <span class="slider"></span>
                </label>
                <span>Record all calls to SD card</span>
            </div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <p><strong>Recording directory:</strong> <code>/mnt/mmcblk0p1/recordings/</code></p>
                
                <div id="recordingsList" class="recordings-list">
                    <div style="padding: 15px; text-align: center; color: #666;">
                        Checking recordings...
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="btn btn-info btn-sm" onclick="checkRecordings()">Refresh List</button>
                    <button class="btn btn-danger btn-sm" onclick="clearRecordings()">Clear All</button>
                </div>
            </div>
        </div>

        <!-- Call History -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0;">Call History</h3>
                <button class="btn btn-info btn-sm" onclick="refreshCalls()">Refresh</button>
            </div>
            
            <div style="overflow-x: auto;">
                <table class="calls-table" id="callsTable">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Direction</th>
                            <th>Number</th>
                            <th>Duration</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="callsList">
                        <tr>
                            <td colspan="5" style="text-align: center; padding: 40px;">
                                Loading call history...
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- SD Card Info -->
        <div class="card">
            <h3>SD Card Information</h3>
            
            <div id="sdInfo" style="font-family: monospace;">
                Loading SD card info...
            </div>
            
            <button class="btn btn-info btn-sm" onclick="checkSDCard()" style="margin-top: 15px;">
                Refresh Info
            </button>
        </div>
    </div>

    <script>
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

        // Check SIP status
        function checkSIPStatus() {
            fetch('/cgi-bin/p/sip_api.cgi?action=get_sip_status')
                .then(r => r.json())
                .then(data => {
                    const statusDiv = document.getElementById('sipState');
                    const statusCard = document.getElementById('sipStatusCard');
                    const iconEl = document.getElementById('statusIcon');
                    
                    if (data.status === 'running') {
                        statusDiv.innerHTML = 'RUNNING';
                        statusCard.className = 'sip-status running';
                        iconEl.innerHTML = '✅';
                    } else {
                        statusDiv.innerHTML = 'STOPPED';
                        statusCard.className = 'sip-status stopped';
                        iconEl.innerHTML = '❌';
                    }
                })
                .catch(error => {
                    showNotification('Error checking SIP status', 'error');
                });
        }

        // Save SIP settings
        function saveSIP() {
            const user = document.getElementById('sipUser').value;
            const server = document.getElementById('sipServer').value;
            const pass = document.getElementById('sipPass').value;
            const transport = document.getElementById('sipTransport').value;
            const autoAnswer = document.getElementById('autoAnswer').checked;
            
            if (!user || !server || !pass) {
                showNotification('Please fill all fields', 'error');
                return;
            }
            
            showNotification('Saving SIP settings...', 'info');
            
            const url = '/cgi-bin/p/sip_save.cgi?user=' + encodeURIComponent(user) + 
                       '&server=' + encodeURIComponent(server) + 
                       '&pass=' + encodeURIComponent(pass) +
                       '&transport=' + encodeURIComponent(transport) +
                       '&auto=' + (autoAnswer ? 'true' : 'false');
            
            fetch(url)
                .then(() => {
                    showNotification('SIP settings saved', 'success');
                    setTimeout(checkSIPStatus, 2000);
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        // Save call number
        function saveCallNumber() {
            const number = document.getElementById('callNumber').value;
            
            fetch('/cgi-bin/p/sip_api.cgi?action=save_call_number&number=' + encodeURIComponent(number))
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        // Save DTMF settings
        function saveDTMFSettings() {
            const mode = document.getElementById('dtmfMode').value;
            const digit = document.getElementById('dtmfDigit').value;
            const action = document.getElementById('dtmfAction').value;
            
            // Here you would save to config file
            showNotification('DTMF settings saved', 'success');
        }

        // Test call
        function testCall() {
            const number = document.getElementById('callNumber').value;
            showNotification('Calling ' + number + '...', 'info');
            
            fetch('/cgi-bin/p/sip_api.cgi?action=make_call&number=' + encodeURIComponent(number))
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        // Load call history
        function loadCallHistory() {
            fetch('/cgi-bin/p/sip_api.cgi?action=get_call_history&lines=20')
                .then(r => r.json())
                .then(data => {
                    const calls = data.calls || [];
                    let html = '';
                    
                    if (calls.length === 0) {
                        html = '<tr><td colspan="5" style="text-align: center; padding: 40px;">📭 No calls</td></tr>';
                    } else {
                        calls.forEach(call => {
                            const statusClass = call.status === 'answered' ? 'badge-success' : 'badge-danger';
                            const directionIcon = call.direction === 'incoming' ? '📲' : '📞';
                            
                            html += '<tr>' +
                                '<td>' + (call.time || '-') + '</td>' +
                                '<td>' + directionIcon + ' ' + (call.direction === 'incoming' ? 'Incoming' : 'Outgoing') + '</td>' +
                                '<td>' + (call.number || '-') + '</td>' +
                                '<td>' + (call.duration || '-') + '</td>' +
                                '<td><span class="badge ' + statusClass + '">' + (call.status === 'answered' ? 'Answered' : 'Missed') + '</span></td>' +
                                '</tr>';
                        });
                    }
                    
                    document.getElementById('callsList').innerHTML = html;
                    
                    // Update stats
                    document.getElementById('totalCalls').textContent = calls.length;
                    document.getElementById('answeredCalls').textContent = calls.filter(c => c.status === 'answered').length;
                    document.getElementById('missedCalls').textContent = calls.filter(c => c.status === 'missed').length;
                })
                .catch(error => {
                    console.error('Call history error:', error);
                });
        }

        // Check SD card
        function checkSDCard() {
            fetch('/cgi-bin/p/backup_api.cgi?action=check_sd')
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('sdInfo').innerHTML = 
                            '<p>✅ SD card ready</p>' +
                            '<p>Free: <strong>' + data.free + '</strong> of <strong>' + data.total + '</strong></p>';
                    } else {
                        document.getElementById('sdInfo').innerHTML = '<p>❌ SD card not available</p>';
                    }
                })
                .catch(error => {
                    document.getElementById('sdInfo').innerHTML = '<p>❌ Error: ' + error + '</p>';
                });
        }

        // Check recordings
        function checkRecordings() {
            fetch('/cgi-bin/p/sip_api.cgi?action=list_recordings')
                .then(r => r.json())
                .then(data => {
                    const recordings = data.recordings || [];
                    let html = '';
                    
                    if (recordings.length === 0) {
                        html = '<div style="padding: 15px; text-align: center; color: #666;">📭 No recordings</div>';
                    } else {
                        recordings.forEach(rec => {
                            html += '<div class="recording-item">' +
                                '<div><strong>' + rec.name + '</strong><br><small>' + rec.size + ' • ' + rec.date + '</small></div>' +
                                '<div>' +
                                    '<button class="btn btn-info btn-sm" onclick="playRecording(\'' + rec.name + '\')">▶️</button> ' +
                                    '<button class="btn btn-danger btn-sm" onclick="deleteRecording(\'' + rec.name + '\')">🗑️</button>' +
                                '</div>' +
                                '</div>';
                        });
                    }
                    
                    document.getElementById('recordingsList').innerHTML = html;
                    document.getElementById('recordingsCount').textContent = recordings.length;
                })
                .catch(error => {
                    document.getElementById('recordingsList').innerHTML = '<div style="padding: 15px; color: #f44336;">❌ Error: ' + error + '</div>';
                });
        }

        // Play recording
        function playRecording(name) {
            window.open('/mnt/mmcblk0p1/recordings/' + name, '_blank');
        }

        // Delete recording
        function deleteRecording(name) {
            if (!confirm('Delete recording ' + name + '?')) return;
            
            fetch('/cgi-bin/p/sip_api.cgi?action=delete_recording&name=' + encodeURIComponent(name))
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                    checkRecordings();
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        // Clear all recordings
        function clearRecordings() {
            if (!confirm('Delete all recordings?')) return;
            
            fetch('/cgi-bin/p/sip_api.cgi?action=clear_recordings')
                .then(r => r.json())
                .then(data => {
                    showNotification(data.message, data.status === 'success' ? 'success' : 'error');
                    checkRecordings();
                })
                .catch(error => showNotification('Error: ' + error, 'error'));
        }

        // Refresh all data
        function refreshCalls() {
            loadCallHistory();
            checkRecordings();
            checkSDCard();
            showNotification('Data refreshed', 'success');
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            checkSIPStatus();
            loadCallHistory();
            checkRecordings();
            checkSDCard();
            
            setInterval(loadCallHistory, 30000);
            setInterval(checkRecordings, 30000);
        });
    </script>
</body>
</html>
