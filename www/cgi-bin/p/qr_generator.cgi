#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

cat << 'EOFH'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Key Generator</title>
    <link rel="stylesheet" href="/a/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js"></script>
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
            margin-right: 5px;
            margin-bottom: 5px;
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
        
        #qrContainer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            min-height: 300px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .share-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .qr-preview {
            background: white;
            padding: 20px;
            border-radius: 10px;
            display: inline-block;
            margin-bottom: 20px;
        }
        
        .recent-keys {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-top: 20px;
        }
        .recent-key-item {
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .recent-key-item:last-child {
            border-bottom: none;
        }
        .recent-key-item:hover {
            background: #f8f9fa;
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
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .share-buttons {
                flex-direction: column;
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
                <a href="/cgi-bin/p/sip_manager.cgi" class="navbar-item">
                    <span>📞</span> SIP
                </a>
                <a href="/cgi-bin/p/qr_generator.cgi" class="navbar-item active">
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
        
        <h1>QR Key Generator</h1>

        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">QR Keys</div>
                <div class="stat-value" id="qrKeysCount">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Telegram</div>
                <div class="stat-value" id="telegramStatus">✅</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Last Share</div>
                <div class="stat-value" id="lastShare">-</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Bot Ready</div>
                <div class="stat-value" id="botReady">✓</div>
            </div>
        </div>

        <!-- Generate QR Code -->
        <div class="card">
            <h3>Generate QR Key</h3>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Key Value *</label>
                        <input type="text" class="form-control" id="keyValue" placeholder="e.g., 12345678 or qrdemo">
                    </div>
                    
                    <div class="form-group">
                        <label>Owner Name *</label>
                        <input type="text" class="form-control" id="ownerName" placeholder="e.g., John Doe">
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
                    
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <button class="btn btn-primary" onclick="generateQR()">🎯 Generate QR</button>
                        <button class="btn btn-success" onclick="saveKey()">💾 Save Key</button>
                        <button class="btn btn-info" onclick="generateRandomKey()">🎲 Random Key</button>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div id="qrContainer">
                        <p style="color: #666;">Enter key and click Generate</p>
                    </div>
                    
                    <!-- Share Buttons -->
                    <div class="share-buttons" id="shareButtons" style="display: none;">
                        <button class="btn btn-info" onclick="shareTelegram()" id="telegramShareBtn">
                            <span>🤖</span> Send to Telegram
                        </button>
                        <button class="btn btn-success" onclick="shareWeChat()">
                            <span>💬</span> WeChat
                        </button>
                        <button class="btn btn-secondary" onclick="copyQRCode()">
                            <span>📋</span> Copy
                        </button>
                        <button class="btn btn-danger" onclick="downloadQR()">
                            <span>📥</span> Download
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
            <h3>Quick Actions</h3>
            
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="btn btn-info" onclick="printQR()">
                    <span>🖨️</span> Print QR
                </button>
                <button class="btn btn-primary" onclick="emailQR()">
                    <span>📧</span> Email
                </button>
                <button class="btn btn-warning" onclick="generateBulkQR()">
                    <span>📚</span> Bulk Generate
                </button>
            </div>
        </div>

        <!-- Recently Generated QR Keys -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0;">Recent QR Keys</h3>
                <button class="btn btn-info btn-sm" onclick="loadRecentKeys()">Refresh</button>
            </div>
            
            <div id="recentKeys" class="recent-keys">
                <div style="padding: 20px; text-align: center; color: #666;">
                    Loading recent keys...
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentQR = null;
        let currentKey = '';
        let currentOwner = '';
        
        // Show notification
        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.className = 'notification ' + type;
            notification.innerHTML = message;
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }
        
        // Convert SVG to PNG data URL
        function svgToPNG(svgElement) {
            return new Promise((resolve) => {
                const svgString = new XMLSerializer().serializeToString(svgElement);
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();
                
                img.onload = function() {
                    canvas.width = img.width;
                    canvas.height = img.height;
                    ctx.drawImage(img, 0, 0);
                    resolve(canvas.toDataURL('image/png'));
                };
                
                img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString);
            });
        }
        
        // Generate QR code
        function generateQR() {
            const key = document.getElementById('keyValue').value.trim();
            const owner = document.getElementById('ownerName').value.trim();
            
            if (!key) {
                showNotification('Please enter a key value', 'error');
                return;
            }
            
            currentKey = key;
            currentOwner = owner || 'Unknown';
            
            const qr = qrcode(0, 'M');
            qr.addData(key);
            qr.make();
            
            const qrContainer = document.getElementById('qrContainer');
            qrContainer.innerHTML = '<div class="qr-preview">' + qr.createSvgTag({cellSize: 8}) + '</div>' +
                '<p><strong>Key:</strong> ' + key + '<br><strong>Owner:</strong> ' + (owner || 'Unknown') + '</p>';
            
            document.getElementById('shareButtons').style.display = 'flex';
            currentQR = qr;
            
            showNotification('QR code generated', 'success');
        }
        
        // Save key to database
        function saveKey() {
            const key = document.getElementById('keyValue').value.trim();
            const owner = document.getElementById('ownerName').value.trim() || 'Unknown';
            const type = document.getElementById('keyType').value;
            
            if (!key) {
                showNotification('Please enter a key value', 'error');
                return;
            }
            
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
                if (data.status === 'success') {
                    showNotification('✅ Key saved to database', 'success');
                    loadRecentKeys();
                } else {
                    showNotification('❌ ' + data.message, 'error');
                }
            })
            .catch(error => showNotification('❌ Error: ' + error, 'error'));
        }
        
        // Generate random key
        function generateRandomKey() {
            const key = Math.floor(10000000 + Math.random() * 90000000).toString();
            document.getElementById('keyValue').value = key;
            showNotification('Random key generated: ' + key, 'success');
        }
        
        // Send to Telegram - используем прямой API бота
        async function shareTelegram() {
            if (!currentKey) {
                showNotification('Please generate a QR code first', 'error');
                return;
            }
            
            const svgElement = document.querySelector('#qrContainer svg');
            if (!svgElement) return;
            
            try {
                showNotification('Sending to Telegram...', 'info');
                
                // Получаем настройки бота из конфига
                const configResponse = await fetch('/cgi-bin/p/telegram_config.cgi');
                const config = await configResponse.json();
                
                if (!config.token || !config.chat_id) {
                    showNotification('Telegram bot not configured', 'error');
                    return;
                }
                
                // Get PNG data URL
                const pngDataUrl = await svgToPNG(svgElement);
                
                // Convert to blob
                const response = await fetch(pngDataUrl);
                const blob = await response.blob();
                
                // Create form data for Telegram Bot API
                const formData = new FormData();
                formData.append('chat_id', config.chat_id);
                formData.append('photo', blob, `qr_${currentKey}.png`);
                formData.append('caption', `🔑 QR Key: ${currentKey}\nOwner: ${currentOwner}`);
                
                // Send directly to Telegram Bot API
                const botResponse = await fetch(`https://api.telegram.org/bot${config.token}/sendPhoto`, {
                    method: 'POST',
                    body: formData
                });
                
                const result = await botResponse.json();
                
                if (result.ok) {
                    showNotification('✅ QR code sent to Telegram!', 'success');
                    document.getElementById('lastShare').innerHTML = new Date().toLocaleTimeString();
                } else {
                    showNotification('❌ Telegram error: ' + (result.description || 'Unknown'), 'error');
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('Failed to send to Telegram', 'error');
            }
        }
        
        // Share WeChat (copy to clipboard)
        function shareWeChat() {
            if (!currentKey) return;
            
            const text = `QR Key for door access: ${currentKey}\nOwner: ${currentOwner}`;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Copied to clipboard - paste in WeChat', 'success');
            }).catch(() => {
                showNotification('Failed to copy', 'error');
            });
            
            // Also download QR code
            const svgElement = document.querySelector('#qrContainer svg');
            if (svgElement) {
                svgToPNG(svgElement).then(pngDataUrl => {
                    const link = document.createElement('a');
                    link.href = pngDataUrl;
                    link.download = `qr_${currentKey}.png`;
                    link.click();
                });
            }
        }
        
        // Copy QR code
        function copyQRCode() {
            if (!currentQR) return;
            
            const svgElement = document.querySelector('#qrContainer svg');
            if (svgElement) {
                svgToPNG(svgElement).then(pngDataUrl => {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    const img = new Image();
                    img.onload = function() {
                        canvas.width = img.width;
                        canvas.height = img.height;
                        ctx.drawImage(img, 0, 0);
                        canvas.toBlob(blob => {
                            navigator.clipboard.write([
                                new ClipboardItem({
                                    'image/png': blob
                                })
                            ]).then(() => {
                                showNotification('QR code copied to clipboard', 'success');
                            }).catch(() => {
                                showNotification('Failed to copy', 'error');
                            });
                        });
                    };
                    img.src = pngDataUrl;
                });
            }
        }
        
        // Download QR code
        function downloadQR() {
            if (!currentQR) return;
            
            const svgElement = document.querySelector('#qrContainer svg');
            if (svgElement) {
                svgToPNG(svgElement).then(pngDataUrl => {
                    const link = document.createElement('a');
                    link.href = pngDataUrl;
                    link.download = `qr_${currentKey}.png`;
                    link.click();
                    showNotification('QR code downloaded', 'success');
                });
            }
        }
        
        function printQR() {
            if (!currentQR) return;
            window.print();
        }
        
        function emailQR() {
            if (!currentKey) return;
            const subject = 'QR Key for Door Access';
            const body = `QR Key: ${currentKey}\nOwner: ${currentOwner}\n\nYou can scan this QR code at the doorphone.`;
            window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        }
        
        function generateBulkQR() {
            showNotification('Bulk generation coming soon', 'info');
        }
        
        // Load recent keys
        function loadRecentKeys() {
            fetch('/cgi-bin/p/door_api.cgi?action=list_keys')
                .then(r => r.json())
                .then(data => {
                    const keys = data.keys || [];
                    const qrKeys = keys.filter(k => k.key.startsWith('QR_') || k.key.length > 8);
                    
                    let html = '';
                    if (qrKeys.length === 0) {
                        html = '<div style="padding: 20px; text-align: center; color: #666;">No QR keys found</div>';
                    } else {
                        qrKeys.slice(0, 10).forEach(key => {
                            html += '<div class="recent-key-item">' +
                                '<div><strong>' + key.key + '</strong><br><small>' + (key.owner || 'Unknown') + '</small></div>' +
                                '<div>' +
                                    '<button class="btn btn-info btn-sm" onclick="regenerateQR(\'' + key.key + '\', \'' + (key.owner || '') + '\')">🔄</button> ' +
                                    '<button class="btn btn-danger btn-sm" onclick="deleteKey(\'' + key.key + '\')">🗑️</button>' +
                                '</div>' +
                                '</div>';
                        });
                    }
                    
                    document.getElementById('recentKeys').innerHTML = html;
                    document.getElementById('qrKeysCount').innerHTML = qrKeys.length;
                })
                .catch(() => {
                    document.getElementById('recentKeys').innerHTML = '<div style="padding: 20px; text-align: center; color: #f44336;">Error loading keys</div>';
                });
        }
        
        function regenerateQR(key, owner) {
            document.getElementById('keyValue').value = key;
            document.getElementById('ownerName').value = owner;
            generateQR();
        }
        
        function deleteKey(key) {
            if (!confirm('Delete key ' + key + '?')) return;
            
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
                    showNotification('Key deleted', 'success');
                    loadRecentKeys();
                } else {
                    showNotification('Error: ' + data.message, 'error');
                }
            });
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadRecentKeys();
            document.getElementById('lastShare').innerHTML = '-';
            document.getElementById('telegramStatus').innerHTML = '✅';
        });
    </script>
</body>
</html>
EOFH
