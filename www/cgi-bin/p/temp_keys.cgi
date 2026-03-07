#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

cat << 'EOFH'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Временные ключи</title>
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
        .form-row {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: flex-end;
        }
        .form-row .form-group {
            flex: 1;
            min-width: 200px;
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
        
        .keys-table {
            width: 100%;
            border-collapse: collapse;
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
        .badge-success {
            background: #4caf50;
            color: white;
        }
        .badge-warning {
            background: #ff9800;
            color: white;
        }
        .badge-danger {
            background: #f44336;
            color: white;
        }
        .badge-info {
            background: #17a2b8;
            color: white;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin: 5px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4caf50, #ff9800, #f44336);
            transition: width 0.3s;
            border-radius: 4px;
        }
        
        .time-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .time-text {
            min-width: 60px;
            font-size: 12px;
            color: #666;
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
        
        .quick-presets {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        .preset-btn {
            padding: 8px 16px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 13px;
        }
        .preset-btn:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }
        .preset-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
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
            .form-row {
                flex-direction: column;
            }
            .form-row .form-group {
                width: 100%;
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
                <a href="/cgi-bin/p/temp_keys.cgi" class="navbar-item active">
                    <span>⏱️</span> Временные
                </a>
                <a href="/cgi-bin/p/sounds.cgi" class="navbar-item">
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
        <h1 class="mb-4">⏱️ Временные ключи</h1>
        
        <!-- Статистика -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Всего временных</div>
                <div class="stat-value" id="totalTemp">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Активных</div>
                <div class="stat-value" style="color: #4caf50;" id="activeTemp">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Истекают сегодня</div>
                <div class="stat-value" style="color: #ff9800;" id="expiringToday">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Истекшие</div>
                <div class="stat-value" style="color: #f44336;" id="expiredTemp">0</div>
            </div>
        </div>
        
        <!-- Форма создания временного ключа -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">➕ Создать временный ключ</h3>
            
            <div class="form-row">
                <div class="form-group">
                    <label>🔑 Номер ключа</label>
                    <input type="text" id="keyValue" class="form-control" placeholder="Например: 12345678">
                </div>
                
                <div class="form-group">
                    <label>👤 Имя владельца</label>
                    <input type="text" id="ownerName" class="form-control" placeholder="Например: Гость">
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>⏱️ Срок действия</label>
                    <select id="expiryType" class="form-control">
                        <option value="hours">Часы</option>
                        <option value="days">Дни</option>
                        <option value="date">Конкретная дата</option>
                    </select>
                </div>
                
                <div class="form-group" id="hoursGroup">
                    <label>Количество часов</label>
                    <input type="number" id="hoursValue" class="form-control" value="24" min="1" max="720">
                </div>
                
                <div class="form-group" id="daysGroup" style="display: none;">
                    <label>Количество дней</label>
                    <input type="number" id="daysValue" class="form-control" value="7" min="1" max="365">
                </div>
                
                <div class="form-group" id="dateGroup" style="display: none;">
                    <label>Дата истечения</label>
                    <input type="datetime-local" id="dateValue" class="form-control">
                </div>
            </div>
            
            <div class="quick-presets">
                <span class="preset-btn" onclick="setPreset(1, 'hours')">1 час</span>
                <span class="preset-btn" onclick="setPreset(3, 'hours')">3 часа</span>
                <span class="preset-btn" onclick="setPreset(6, 'hours')">6 часов</span>
                <span class="preset-btn" onclick="setPreset(12, 'hours')">12 часов</span>
                <span class="preset-btn" onclick="setPreset(24, 'hours')">24 часа</span>
                <span class="preset-btn" onclick="setPreset(2, 'days')">2 дня</span>
                <span class="preset-btn" onclick="setPreset(7, 'days')">7 дней</span>
                <span class="preset-btn" onclick="setPreset(30, 'days')">30 дней</span>
            </div>
            
            <div style="margin-top: 20px;">
                <button class="btn btn-success" onclick="createTempKey()">
                    ✨ Создать временный ключ
                </button>
                <button class="btn btn-info" onclick="generateRandomKey()">
                    🎲 Сгенерировать ключ
                </button>
            </div>
            
            <div id="createProgress" style="display: none; margin-top: 15px;">
                <div class="progress-bar">
                    <div class="progress-fill" id="createProgressFill" style="width: 0%;"></div>
                </div>
            </div>
        </div>
        
        <!-- Поиск -->
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Поиск по ключу или владельцу...">
            <i>🔍</i>
        </div>
        
        <!-- Список временных ключей -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0;">📋 Список временных ключей</h3>
                <div>
                    <button class="btn btn-primary btn-sm" onclick="loadKeys()">
                        🔄 Обновить
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="showClearExpiredModal()">
                        🗑️ Удалить истекшие
                    </button>
                </div>
            </div>
            
            <div style="overflow-x: auto;">
                <table class="keys-table" id="keysTable">
                    <thead>
                        <tr>
                            <th>Ключ</th>
                            <th>Владелец</th>
                            <th>Создан</th>
                            <th>Истекает</th>
                            <th>Осталось</th>
                            <th>Статус</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody id="keysList">
                        <tr>
                            <td colspan="7" style="text-align: center; padding: 40px;">
                                <p style="color: #666;">Загрузка ключей...</p>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Информация о временных ключах -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">ℹ️ О временных ключах</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div>
                    <h4>⏱️ Как это работает</h4>
                    <ul style="color: #666; line-height: 1.6;">
                        <li>Временные ключи автоматически удаляются по истечении срока</li>
                        <li>Проверка выполняется каждый час через cron</li>
                        <li>Истекшие ключи помечаются красным и могут быть удалены</li>
                    </ul>
                </div>
                
                <div>
                    <h4>📊 Статусы ключей</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 10px;">
                            <span class="badge badge-success">Активный</span> - ключ действителен
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span class="badge badge-warning">Скоро истечет</span> - осталось менее 24 часов
                        </li>
                        <li style="margin-bottom: 10px;">
                            <span class="badge badge-danger">Истек</span> - срок действия прошел
                        </li>
                    </ul>
                </div>
                
                <div>
                    <h4>📝 Примеры использования</h4>
                    <ul style="color: #666; line-height: 1.6;">
                        <li>Гостевой доступ на несколько часов</li>
                        <li>Курьерская доставка на 1 день</li>
                        <li>Ремонтные работы на неделю</li>
                        <li>Арендаторам на месяц</li>
                    </ul>
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
        let allKeys = [];
        let filteredKeys = [];
        let deleteCallback = null;
        
        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            // Устанавливаем сегодняшнюю дату для поля выбора даты
            const now = new Date();
            now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
            document.getElementById('dateValue').value = now.toISOString().slice(0, 16);
            
            // Загружаем ключи
            loadKeys();
            
            // Поиск
            document.getElementById('searchInput').addEventListener('input', filterKeys);
            
            // Переключение типов срока действия
            document.getElementById('expiryType').addEventListener('change', toggleExpiryType);
            
            // Обновляем каждые 30 секунд
            setInterval(loadKeys, 30000);
        });
        
        // Переключение типов срока действия
        function toggleExpiryType() {
            const type = document.getElementById('expiryType').value;
            
            document.getElementById('hoursGroup').style.display = type === 'hours' ? 'block' : 'none';
            document.getElementById('daysGroup').style.display = type === 'days' ? 'block' : 'none';
            document.getElementById('dateGroup').style.display = type === 'date' ? 'block' : 'none';
        }
        
        // Установка предустановленного значения
        function setPreset(value, type) {
            document.getElementById('expiryType').value = type;
            toggleExpiryType();
            
            if (type === 'hours') {
                document.getElementById('hoursValue').value = value;
            } else if (type === 'days') {
                document.getElementById('daysValue').value = value;
            }
        }
        
        // Генерация случайного ключа
        function generateRandomKey() {
            const key = Math.floor(10000000 + Math.random() * 90000000).toString();
            document.getElementById('keyValue').value = key;
            showNotification('🎲 Сгенерирован ключ: ' + key, 'info');
        }
        
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
        
        // Загрузка ключей
        function loadKeys() {
            fetch('/cgi-bin/p/door_api.cgi?action=list_keys')
                .then(r => r.json())
                .then(data => {
                    allKeys = data.keys || [];
                    filterKeys();
                    updateStats();
                })
                .catch(error => {
                    console.error('Error loading keys:', error);
                    showNotification('❌ Ошибка загрузки ключей', 'error');
                });
        }
        
        // Фильтрация ключей
        function filterKeys() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const now = Math.floor(Date.now() / 1000);
            
            // Оставляем только временные ключи (с expiry)
            filteredKeys = allKeys.filter(key => key.expiry);
            
            // Применяем поиск
            if (searchTerm) {
                filteredKeys = filteredKeys.filter(key => 
                    key.key.toLowerCase().includes(searchTerm) ||
                    (key.owner || '').toLowerCase().includes(searchTerm)
                );
            }
            
            renderKeys();
        }
        
        // Обновление статистики
        function updateStats() {
            const now = Math.floor(Date.now() / 1000);
            const tomorrow = now + 86400;
            
            let total = 0;
            let active = 0;
            let expiringToday = 0;
            let expired = 0;
            
            allKeys.forEach(key => {
                if (key.expiry) {
                    total++;
                    const expiry = parseInt(key.expiry);
                    
                    if (expiry < now) {
                        expired++;
                    } else {
                        active++;
                        if (expiry < tomorrow) {
                            expiringToday++;
                        }
                    }
                }
            });
            
            document.getElementById('totalTemp').textContent = total;
            document.getElementById('activeTemp').textContent = active;
            document.getElementById('expiringToday').textContent = expiringToday;
            document.getElementById('expiredTemp').textContent = expired;
        }
        
        // Форматирование даты
        function formatDate(timestamp) {
            if (!timestamp) return '-';
            const date = new Date(parseInt(timestamp) * 1000);
            return date.toLocaleString('ru-RU', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        // Расчет оставшегося времени
        function getTimeLeft(expiry) {
            const now = Math.floor(Date.now() / 1000);
            const diff = parseInt(expiry) - now;
            
            if (diff <= 0) {
                return { text: 'Истек', percent: 100, class: 'badge-danger' };
            }
            
            const days = Math.floor(diff / 86400);
            const hours = Math.floor((diff % 86400) / 3600);
            const minutes = Math.floor((diff % 3600) / 60);
            
            let text = '';
            let percent = 0;
            let statusClass = 'badge-success';
            
            // Рассчитываем процент для шкалы (максимум 30 дней)
            const maxDays = 30;
            const maxSeconds = maxDays * 86400;
            percent = Math.min(100, Math.floor((maxSeconds - diff) / maxSeconds * 100));
            
            if (days > 0) {
                text = `${days} дн ${hours} ч`;
            } else if (hours > 0) {
                text = `${hours} ч ${minutes} мин`;
                if (hours < 24) statusClass = 'badge-warning';
            } else {
                text = `${minutes} мин`;
                statusClass = 'badge-warning';
            }
            
            return { text, percent, class: statusClass };
        }
        
        // Отображение ключей
        function renderKeys() {
            if (filteredKeys.length === 0) {
                document.getElementById('keysList').innerHTML = `
                    <tr>
                        <td colspan="7" style="text-align: center; padding: 40px; color: #666;">
                            🔍 Временные ключи не найдены
                        </td>
                    </tr>
                `;
                return;
            }
            
            // Сортируем по дате истечения (скоро истекающие сверху)
            filteredKeys.sort((a, b) => {
                const expiryA = parseInt(a.expiry) || 0;
                const expiryB = parseInt(b.expiry) || 0;
                return expiryA - expiryB;
            });
            
            let html = '';
            filteredKeys.forEach(key => {
                const timeLeft = getTimeLeft(key.expiry);
                const created = key.date ? new Date(key.date).toLocaleString('ru-RU') : '-';
                
                html += '<tr>' +
                    '<td><strong>' + key.key + '</strong></td>' +
                    '<td>' + (key.owner || 'Не указан') + '</td>' +
                    '<td>' + created + '</td>' +
                    '<td>' + formatDate(key.expiry) + '</td>' +
                    '<td>' +
                        '<div class="time-left">' +
                            '<span class="time-text">' + timeLeft.text + '</span>' +
                            '<div class="progress-bar" style="width: 60px;">' +
                                '<div class="progress-fill" style="width: ' + timeLeft.percent + '%;"></div>' +
                            '</div>' +
                        '</div>' +
                    '</td>' +
                    '<td><span class="badge ' + timeLeft.class + '">' + 
                        (timeLeft.class === 'badge-success' ? 'Активен' : 
                         timeLeft.class === 'badge-warning' ? 'Скоро истечет' : 'Истек') + 
                    '</span></td>' +
                    '<td>' +
                        '<button class="btn btn-danger btn-sm" onclick="deleteKey(\'' + key.key + '\')">🗑️</button>' +
                    '</td>' +
                    '</tr>';
            });
            
            document.getElementById('keysList').innerHTML = html;
        }
        
        // Создание временного ключа
        function createTempKey() {
            const key = document.getElementById('keyValue').value.trim();
            const owner = document.getElementById('ownerName').value.trim();
            const expiryType = document.getElementById('expiryType').value;
            
            if (!key || !owner) {
                showNotification('❌ Заполните все поля', 'error');
                return;
            }
            
            // Рассчитываем timestamp истечения
            let expiry = '';
            const now = Math.floor(Date.now() / 1000);
            
            if (expiryType === 'hours') {
                const hours = parseInt(document.getElementById('hoursValue').value);
                expiry = now + (hours * 3600);
            } else if (expiryType === 'days') {
                const days = parseInt(document.getElementById('daysValue').value);
                expiry = now + (days * 86400);
            } else {
                const dateStr = document.getElementById('dateValue').value;
                if (dateStr) {
                    expiry = Math.floor(new Date(dateStr).getTime() / 1000);
                }
            }
            
            if (!expiry) {
                showNotification('❌ Укажите срок действия', 'error');
                return;
            }
            
            // Показываем прогресс
            const progress = document.getElementById('createProgress');
            const progressFill = document.getElementById('createProgressFill');
            progress.style.display = 'block';
            progressFill.style.width = '50%';
            
            const body = `action=add_key&key=${encodeURIComponent(key)}&owner=${encodeURIComponent(owner)}&expiry=${expiry}`;
            
            fetch('/cgi-bin/p/door_api.cgi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: body
            })
            .then(r => r.json())
            .then(data => {
                progressFill.style.width = '100%';
                setTimeout(() => {
                    progress.style.display = 'none';
                    progressFill.style.width = '0%';
                }, 500);
                
                if (data.status === 'success') {
                    showNotification('✅ Временный ключ создан', 'success');
                    document.getElementById('keyValue').value = '';
                    document.getElementById('ownerName').value = '';
                    loadKeys();
                } else {
                    showNotification('❌ ' + data.message, 'error');
                }
            })
            .catch(error => {
                progress.style.display = 'none';
                showNotification('❌ Ошибка: ' + error, 'error');
            });
        }
        
        // Удаление ключа
        function deleteKey(key) {
            showModal(
                'Удаление ключа',
                `Вы уверены, что хотите удалить ключ ${key}?`,
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
                            showNotification('✅ Ключ удален', 'success');
                            loadKeys();
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
        
        // Очистка истекших ключей
        function showClearExpiredModal() {
            const now = Math.floor(Date.now() / 1000);
            const expiredCount = allKeys.filter(key => key.expiry && parseInt(key.expiry) < now).length;
            
            if (expiredCount === 0) {
                showNotification('ℹ️ Нет истекших ключей', 'info');
                return;
            }
            
            showModal(
                'Очистка истекших ключей',
                `Удалить ${expiredCount} истекших ключей?`,
                function() {
                    const now = Math.floor(Date.now() / 1000);
                    let deleted = 0;
                    
                    allKeys.forEach(key => {
                        if (key.expiry && parseInt(key.expiry) < now) {
                            fetch('/cgi-bin/p/door_api.cgi', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded'
                                },
                                body: 'action=remove_key&key=' + encodeURIComponent(key.key)
                            })
                            .then(r => r.json())
                            .then(data => {
                                if (data.status === 'success') {
                                    deleted++;
                                    if (deleted === expiredCount) {
                                        showNotification(`✅ Удалено ${deleted} истекших ключей`, 'success');
                                        loadKeys();
                                    }
                                }
                            })
                            .catch(error => {
                                console.error('Error deleting key:', error);
                            });
                        }
                    });
                }
            );
        }
    </script>
</body>
</html>
EOFH