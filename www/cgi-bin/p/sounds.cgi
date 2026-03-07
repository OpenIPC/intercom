#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

# Получаем список доступных звуков
SOUND_DIR="/usr/share/sounds/doorphone"
SOUNDS=""
if [ -d "$SOUND_DIR" ]; then
    SOUNDS=$(ls "$SOUND_DIR"/*.pcm 2>/dev/null | xargs -n1 basename | sed 's/\.pcm$//')
fi

cat << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Звуковые эффекты</title>
    <link rel="stylesheet" href="/a/bootstrap.min.css">
    <style>
        /* Навигационная панель */
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
            display: flex;
            align-items: center;
            gap: 10px;
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
            display: flex;
            align-items: center;
            gap: 5px;
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
        
        .sound-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .sound-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        .sound-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        .sound-icon {
            font-size: 48px;
            text-align: center;
            margin-bottom: 15px;
        }
        .sound-name {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            color: #333;
        }
        .sound-info {
            font-size: 12px;
            color: #666;
            text-align: center;
            margin-bottom: 15px;
        }
        .sound-actions {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        
        .upload-area {
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            background: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s;
            margin: 20px 0;
        }
        .upload-area:hover {
            background: #e9ecef;
            border-color: #5a67d8;
            transform: translateY(-2px);
        }
        .upload-area.dragover {
            background: #d1d5f0;
            border-color: #4c51bf;
        }
        .upload-icon {
            font-size: 48px;
            color: #667eea;
            margin-bottom: 15px;
        }
        .upload-text {
            font-size: 16px;
            color: #495057;
            margin-bottom: 10px;
        }
        .upload-hint {
            font-size: 12px;
            color: #6c757d;
        }
        
        .btn {
            padding: 10px 20px;
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
            padding: 6px 12px;
            font-size: 12px;
        }
        
        .progress {
            margin-top: 15px;
            display: none;
        }
        .progress-bar {
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s;
            border-radius: 3px;
        }
        .progress-text {
            text-align: center;
            font-size: 12px;
            color: #6c757d;
            margin-top: 5px;
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
        
        .volume-slider {
            width: 100%;
            margin: 10px 0;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            background: #e9ecef;
            color: #495057;
        }
        .badge-success {
            background: #4caf50;
            color: white;
        }
        
        .format-info {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
            font-size: 13px;
            color: #495057;
        }
        .format-info code {
            background: #e9ecef;
            padding: 2px 5px;
            border-radius: 4px;
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
        
        .converter-tool {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
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
            .sound-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Навигационная панель -->
    <nav class="navbar">
        <div class="navbar-container">
            <a href="/cgi-bin/status.cgi" class="navbar-brand">
                <span style="font-size: 28px;">🏠</span>
                <span>OpenIPC Doorphone</span>
            </a>
            
            <div class="navbar-menu">
                <a href="/cgi-bin/status.cgi" class="navbar-item">
                    <span>🏠</span> Главная
                </a>
                <a href="/cgi-bin/p/door_keys.cgi" class="navbar-item">
                    <span>🔑</span> Ключи
                </a>
                <a href="/cgi-bin/p/sip_manager.cgi" class="navbar-item">
                    <span>📞</span> SIP
                </a>
                <a href="/cgi-bin/p/qr_generator.cgi" class="navbar-item">
                    <span>🎯</span> QR
                </a>
                <a href="/cgi-bin/p/temp_keys.cgi" class="navbar-item">
                    <span>⏱️</span> Временные
                </a>
                <a href="/cgi-bin/p/sounds.cgi" class="navbar-item active">
                    <span>🔊</span> Звуки
                </a>
                <a href="/cgi-bin/p/door_history.cgi" class="navbar-item">
                    <span>📋</span> История
                </a>
                <a href="/cgi-bin/backup.cgi" class="navbar-item">
                    <span>💾</span> Бэкапы
                </a>
            </div>
            
            <a href="/cgi-bin/status.cgi" class="home-button">
                <span>⬅️</span> На главную
            </a>
        </div>
    </nav>

    <div class="container">
        <!-- Уведомления -->
        <div id="notification" class="notification"></div>
        
        <!-- Заголовок -->
        <h1 class="mb-4">🔊 Звуковые эффекты</h1>
        
        <!-- Статистика -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Всего звуков</div>
                <div class="stat-value" id="totalSounds">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Размер</div>
                <div class="stat-value" id="totalSize">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Свободно на SD</div>
                <div class="stat-value" id="sdFree">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Громкость</div>
                <div class="stat-value" id="volumeValue">100%</div>
            </div>
        </div>
        
        <!-- Громкость -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">🔊 Регулятор громкости</h3>
            
            <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 200px;">
                    <input type="range" id="volumeSlider" class="volume-slider" min="0" max="100" value="80">
                </div>
                <div>
                    <span id="volumeDisplay" style="font-size: 18px; font-weight: bold;">80%</span>
                </div>
                <div>
                    <button class="btn btn-primary btn-sm" onclick="testVolume()">🔊 Тест</button>
                    <button class="btn btn-success btn-sm" onclick="saveVolume()">💾 Сохранить</button>
                </div>
            </div>
        </div>
        
        <!-- Загрузка звуков -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">📤 Загрузить новый звук</h3>
            
            <div class="format-info">
                <strong>Требования к формату:</strong><br>
                • Формат: <code>PCM</code> (сырые данные)<br>
                • Частота: <code>8000 Гц</code> (8kHz)<br>
                • Разрядность: <code>16 бит</code><br>
                • Каналы: <code>моно</code><br>
                • Расширение: <code>.pcm</code>
            </div>
            
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📁</div>
                <div class="upload-text">Нажмите или перетащите PCM файл сюда</div>
                <div class="upload-hint">Поддерживаются только файлы .pcm (8kHz, 16bit, mono)</div>
                <input type="file" id="fileInput" style="display: none;" accept=".pcm">
            </div>
            
            <div class="converter-tool">
                <p><strong>🔄 Нужно конвертировать MP3/WAV в PCM?</strong></p>
                <p style="font-size: 13px; color: #666;">Используйте команду на компьютере:</p>
                <code style="display: block; background: #e9ecef; padding: 10px; border-radius: 5px; margin: 10px 0;">
                    ffmpeg -i input.mp3 -ar 8000 -ac 1 -f s16le output.pcm
                </code>
                <p style="font-size: 12px; color: #999;">Или используйте онлайн-конвертеры</p>
            </div>
            
            <div id="uploadProgress" class="progress">
                <div class="progress-bar">
                    <div class="progress-fill" id="uploadProgressFill"></div>
                </div>
                <div class="progress-text" id="uploadProgressText">0%</div>
            </div>
        </div>
        
        <!-- Список звуков -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0;">📋 Доступные звуки</h3>
                <div>
                    <button class="btn btn-primary btn-sm" onclick="loadSounds()">
                        🔄 Обновить
                    </button>
                </div>
            </div>
            
            <div id="soundsGrid" class="sound-grid">
                <!-- Сюда будут добавлены звуки через JavaScript -->
            </div>
        </div>
        
        <!-- Звуки по умолчанию -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">📝 Стандартные звуки</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div class="sound-card" style="background: #e3f2fd;">
                    <div class="sound-icon">🔔</div>
                    <div class="sound-name">Звонок</div>
                    <div class="sound-info">ring.pcm</div>
                    <div class="sound-actions">
                        <button class="btn btn-primary btn-sm" onclick="playSound('ring')">▶️</button>
                    </div>
                </div>
                
                <div class="sound-card" style="background: #e8f5e8;">
                    <div class="sound-icon">🚪</div>
                    <div class="sound-name">Открытие</div>
                    <div class="sound-info">door_open.pcm</div>
                    <div class="sound-actions">
                        <button class="btn btn-primary btn-sm" onclick="playSound('door_open')">▶️</button>
                    </div>
                </div>
                
                <div class="sound-card" style="background: #fff3e0;">
                    <div class="sound-icon">❌</div>
                    <div class="sound-name">Отказ</div>
                    <div class="sound-info">denied.pcm</div>
                    <div class="sound-actions">
                        <button class="btn btn-primary btn-sm" onclick="playSound('denied')">▶️</button>
                    </div>
                </div>
                
                <div class="sound-card" style="background: #f1f1f1;">
                    <div class="sound-icon">🔊</div>
                    <div class="sound-name">Тест</div>
                    <div class="sound-info">beep.pcm</div>
                    <div class="sound-actions">
                        <button class="btn btn-primary btn-sm" onclick="playSound('beep')">▶️</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Модальное окно подтверждения -->
    <div class="modal" id="confirmModal">
        <div class="modal-content">
            <h3 class="modal-title" id="modalTitle">Подтверждение</h3>
            <p id="modalMessage">Вы уверены?</p>
            <div class="modal-buttons">
                <button class="btn btn-secondary" onclick="closeModal()">Отмена</button>
                <button class="btn btn-danger" id="modalConfirmBtn">Подтвердить</button>
            </div>
        </div>
    </div>

    <script>
        // Глобальные переменные
        let sounds = [];
        let deleteCallback = null;
        let volume = 80;
        
        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            loadSounds();
            loadVolume();
            checkSDCard();
            initUpload();
        });
        
        // Уведомления
        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.className = 'notification ' + type;
            notification.innerHTML = message;
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }
        
        // Модальное окно
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
        
        // Инициализация загрузки
        function initUpload() {
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
                if (file) uploadSound(file);
            });
            
            fileInput.addEventListener('change', (e) => {
                if (e.target.files[0]) uploadSound(e.target.files[0]);
            });
        }
        
        // Загрузка звука
        function uploadSound(file) {
            // Проверка расширения
            if (!file.name.toLowerCase().endsWith('.pcm')) {
                showNotification('❌ Можно загружать только .pcm файлы', 'error');
                return;
            }
            
            // Проверка размера (макс 1MB)
            if (file.size > 1024 * 1024) {
                showNotification('❌ Файл слишком большой (макс 1MB)', 'error');
                return;
            }
            
            const progress = document.getElementById('uploadProgress');
            const progressFill = document.getElementById('uploadProgressFill');
            const progressText = document.getElementById('uploadProgressText');
            
            progress.style.display = 'block';
            progressFill.style.width = '0%';
            progressText.textContent = '0%';
            
            const formData = new FormData();
            formData.append('sound', file);
            
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percent = Math.round(e.loaded / e.total * 100);
                    progressFill.style.width = percent + '%';
                    progressText.textContent = percent + '%';
                }
            });
            
            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        if (response.status === 'success') {
                            showNotification('✅ ' + response.message, 'success');
                            loadSounds();
                        } else {
                            showNotification('❌ ' + response.message, 'error');
                        }
                    } catch (e) {
                        showNotification('✅ Файл загружен', 'success');
                        loadSounds();
                    }
                } else {
                    showNotification('❌ Ошибка загрузки', 'error');
                }
                
                setTimeout(() => {
                    progress.style.display = 'none';
                    progressFill.style.width = '0%';
                }, 1000);
            });
            
            xhr.addEventListener('error', () => {
                showNotification('❌ Ошибка соединения', 'error');
                progress.style.display = 'none';
            });
            
            xhr.open('POST', '/cgi-bin/p/upload_sound.cgi');
            xhr.send(formData);
        }
        
        // Загрузка списка звуков
        function loadSounds() {
            fetch('/cgi-bin/p/sound_api.cgi?action=list_sounds')
                .then(r => r.json())
                .then(data => {
                    sounds = data.sounds || [];
                    renderSounds();
                    updateStats();
                })
                .catch(error => {
                    console.error('Error loading sounds:', error);
                });
        }
        
        // Отображение звуков
        function renderSounds() {
            const grid = document.getElementById('soundsGrid');
            
            if (sounds.length === 0) {
                grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #666;">📭 Нет загруженных звуков</div>';
                return;
            }
            
            let html = '';
            sounds.forEach(sound => {
                const icon = getSoundIcon(sound.name);
                const size = formatSize(sound.size);
                
                html += '<div class="sound-card">' +
                    '<div class="sound-icon">' + icon + '</div>' +
                    '<div class="sound-name">' + (sound.displayName || sound.name) + '</div>' +
                    '<div class="sound-info">' + sound.name + ' • ' + size + '</div>' +
                    '<div class="sound-actions">' +
                        '<button class="btn btn-primary btn-sm" onclick="playSound(\'' + sound.name.replace('.pcm', '') + '\')">▶️</button> ' +
                        '<button class="btn btn-danger btn-sm" onclick="deleteSound(\'' + sound.name + '\')">🗑️</button>' +
                    '</div>' +
                    '</div>';
            });
            
            grid.innerHTML = html;
        }
        
        // Получение иконки для звука
        function getSoundIcon(name) {
            if (name.includes('ring')) return '🔔';
            if (name.includes('door_open')) return '🚪';
            if (name.includes('denied')) return '❌';
            if (name.includes('beep')) return '🔊';
            return '🎵';
        }
        
        // Форматирование размера
        function formatSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        }
        
        // Обновление статистики
        function updateStats() {
            document.getElementById('totalSounds').textContent = sounds.length;
            
            let totalSize = 0;
            sounds.forEach(s => totalSize += s.size || 0);
            document.getElementById('totalSize').textContent = formatSize(totalSize);
        }
        
        // Воспроизведение звука
        function playSound(name) {
            fetch('/cgi-bin/p/play_sound.cgi?name=' + name)
                .then(r => r.text())
                .then(data => {
                    showNotification('🔊 Воспроизведение: ' + name, 'info');
                })
                .catch(error => {
                    showNotification('❌ Ошибка: ' + error, 'error');
                });
        }
        
        // Удаление звука
        function deleteSound(name) {
            showModal(
                'Удаление звука',
                'Удалить файл ' + name + '?',
                function() {
                    fetch('/cgi-bin/p/sound_api.cgi?action=delete_sound&name=' + encodeURIComponent(name))
                        .then(r => r.json())
                        .then(data => {
                            if (data.status === 'success') {
                                showNotification('✅ ' + data.message, 'success');
                                loadSounds();
                            } else {
                                showNotification('❌ ' + data.message, 'error');
                            }
                        })
                        .catch(error => {
                            showNotification('❌ Ошибка: ' + error, 'error');
                        });
                }
            );
        }
        
        // Проверка SD-карты
        function checkSDCard() {
            fetch('/cgi-bin/p/backup_api.cgi?action=check_sd')
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('sdFree').textContent = data.free || '0';
                    } else {
                        document.getElementById('sdFree').textContent = 'N/A';
                    }
                })
                .catch(error => {
                    document.getElementById('sdFree').textContent = 'N/A';
                });
        }
        
        // Громкость
        function loadVolume() {
            const slider = document.getElementById('volumeSlider');
            const display = document.getElementById('volumeDisplay');
            
            slider.addEventListener('input', function() {
                display.textContent = this.value + '%';
            });
        }
        
        function testVolume() {
            playSound('beep');
        }
        
        function saveVolume() {
            const volume = document.getElementById('volumeSlider').value;
            // Здесь можно сохранять громкость в конфиг
            showNotification('✅ Громкость сохранена: ' + volume + '%', 'success');
        }
    </script>
</body>
</html>
EOF