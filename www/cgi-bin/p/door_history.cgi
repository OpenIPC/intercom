#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

cat << 'EOFH'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>История событий</title>
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
        .container { max-width: 1400px; margin: 0 auto; padding: 0 20px; }
        
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
        
        .filters {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        .filter-group {
            flex: 1;
            min-width: 200px;
        }
        .filter-group label {
            display: block;
            margin-bottom: 5px;
            color: #495057;
            font-size: 13px;
            font-weight: 500;
        }
        .filter-control {
            width: 100%;
            padding: 8px 12px;
            border: 2px solid #e9ecef;
            border-radius: 6px;
            font-size: 14px;
            transition: all 0.3s;
        }
        .filter-control:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
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
        
        .history-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        .history-table th {
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #495057;
            border-bottom: 2px solid #dee2e6;
            white-space: nowrap;
        }
        .history-table td {
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
            vertical-align: middle;
        }
        .history-table tr:hover {
            background: #f8f9fa;
            cursor: pointer;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
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
        .badge-secondary {
            background: #6c757d;
            color: white;
        }
        
        .event-icon {
            font-size: 18px;
            margin-right: 8px;
        }
        
        .key-highlight {
            background: #fff3cd;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
        }
        
        .pagination {
            display: flex;
            gap: 5px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .page-btn {
            padding: 6px 12px;
            border: 1px solid #dee2e6;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
            min-width: 35px;
        }
        .page-btn:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }
        .page-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        .page-btn.disabled {
            opacity: 0.5;
            cursor: not-allowed;
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
        
        .date-range {
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }
        .date-input {
            flex: 1;
            min-width: 150px;
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
        
        .export-menu {
            position: relative;
            display: inline-block;
        }
        .export-dropdown {
            display: none;
            position: absolute;
            right: 0;
            background: white;
            min-width: 160px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            border-radius: 8px;
            z-index: 1;
            margin-top: 5px;
        }
        .export-dropdown a {
            color: #333;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            transition: all 0.3s;
        }
        .export-dropdown a:hover {
            background: #f8f9fa;
        }
        .export-menu:hover .export-dropdown {
            display: block;
        }
        
        .timeline-view {
            display: none;
            margin-top: 20px;
        }
        .timeline-item {
            display: flex;
            gap: 20px;
            padding: 15px;
            border-left: 3px solid #667eea;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 0 8px 8px 0;
        }
        .timeline-time {
            min-width: 150px;
            font-weight: 500;
            color: #495057;
        }
        .timeline-content {
            flex: 1;
        }
        
        .chart-container {
            height: 300px;
            margin: 20px 0;
            display: none;
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
            .filters {
                flex-direction: column;
            }
            .filter-group {
                width: 100%;
            }
            .history-table {
                font-size: 12px;
            }
            .history-table td, .history-table th {
                padding: 8px 4px;
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
                <a href="/cgi-bin/p/sounds.cgi" class="navbar-item">
                    <span>🔊</span> Звуки
                </a>
                <a href="/cgi-bin/p/door_history.cgi" class="navbar-item active">
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
        <h1 class="mb-4">📋 История событий</h1>
        
        <!-- Статистика -->
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Всего событий</div>
                <div class="stat-value" id="totalEvents">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Открытий двери</div>
                <div class="stat-value" style="color: #4caf50;" id="openEvents">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Ключей (успешно)</div>
                <div class="stat-value" style="color: #4caf50;" id="keySuccess">0</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Отказов</div>
                <div class="stat-value" style="color: #f44336;" id="keyDenied">0</div>
            </div>
        </div>
        
        <!-- Фильтры -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">🔍 Фильтры</h3>
            
            <div class="filters">
                <div class="filter-group">
                    <label>📅 Период</label>
                    <div class="date-range">
                        <input type="date" id="dateFrom" class="filter-control date-input">
                        <span>—</span>
                        <input type="date" id="dateTo" class="filter-control date-input">
                    </div>
                </div>
                
                <div class="filter-group">
                    <label>🔑 Тип события</label>
                    <select id="eventType" class="filter-control">
                        <option value="all">Все события</option>
                        <option value="open">Открытие двери</option>
                        <option value="key_allowed">Ключ принят</option>
                        <option value="key_denied">Ключ отклонен</option>
                        <option value="call">Звонок</option>
                        <option value="button">Кнопка</option>
                        <option value="esp">ESP статус</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label>👤 Владелец/Ключ</label>
                    <input type="text" id="searchKey" class="filter-control" placeholder="Поиск по ключу или владельцу...">
                </div>
                
                <div class="filter-group" style="min-width: auto;">
                    <label>&nbsp;</label>
                    <button class="btn btn-primary" onclick="applyFilters()" style="width: 100%;">
                        🔍 Применить
                    </button>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; flex-wrap: wrap; justify-content: space-between; align-items: center;">
                <div style="display: flex; gap: 10px;">
                    <button class="btn btn-info btn-sm" onclick="refreshHistory()">
                        🔄 Обновить
                    </button>
                    <button class="btn btn-warning btn-sm" onclick="clearFilters()">
                        🗑️ Сбросить фильтры
                    </button>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <div class="export-menu">
                        <button class="btn btn-success btn-sm">
                            📥 Экспорт ▼
                        </button>
                        <div class="export-dropdown">
                            <a href="#" onclick="exportCSV()">📊 Экспорт в CSV</a>
                            <a href="#" onclick="exportJSON()">📋 Экспорт в JSON</a>
                            <a href="#" onclick="exportTXT()">📝 Экспорт в TXT</a>
                        </div>
                    </div>
                    
                    <button class="btn btn-danger btn-sm" onclick="clearHistory()">
                        🗑️ Очистить историю
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Вид отображения -->
        <div style="display: flex; gap: 10px; margin-bottom: 15px;">
            <button class="btn btn-sm btn-info" onclick="showTableView()" id="viewTableBtn">📋 Таблица</button>
            <button class="btn btn-sm btn-secondary" onclick="showTimelineView()" id="viewTimelineBtn">📅 Хронология</button>
            <button class="btn btn-sm btn-secondary" onclick="showChartView()" id="viewChartBtn">📊 График</button>
        </div>
        
        <!-- Таблица событий -->
        <div class="card" id="tableView">
            <div style="overflow-x: auto;">
                <table class="history-table" id="historyTable">
                    <thead>
                        <tr>
                            <th>Время</th>
                            <th>Тип</th>
                            <th>Событие</th>
                            <th>Ключ</th>
                            <th>Владелец</th>
                            <th>Результат</th>
                            <th>Детали</th>
                        </tr>
                    </thead>
                    <tbody id="historyList">
                        <tr>
                            <td colspan="7" style="text-align: center; padding: 40px;">
                                <p style="color: #666;">Загрузка истории...</p>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Пагинация -->
            <div class="pagination" id="pagination"></div>
            <div style="text-align: center; margin-top: 10px; color: #6c757d; font-size: 12px;">
                <span id="showingInfo">Показано 0 из 0 событий</span>
            </div>
        </div>
        
        <!-- Хронология -->
        <div class="card" id="timelineView" style="display: none;">
            <div id="timelineList"></div>
        </div>
        
        <!-- График -->
        <div class="card" id="chartView" style="display: none;">
            <div class="chart-container" id="chartContainer">
                <canvas id="activityChart"></canvas>
            </div>
            <div style="text-align: center; padding: 20px;">
                <p style="color: #666;">График активности по часам</p>
            </div>
        </div>
        
        <!-- Информация о базе данных -->
        <div class="card">
            <h3 style="margin-top: 0; margin-bottom: 20px;">ℹ️ Информация</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div>
                    <p><strong>📁 Файл лога:</strong> <code>/var/log/door_monitor.log</code></p>
                    <p><strong>📊 Размер лога:</strong> <span id="logSize">-</span></p>
                    <p><strong>📅 Первая запись:</strong> <span id="firstEntry">-</span></p>
                </div>
                <div>
                    <p><strong>🔄 Автообновление:</strong> каждые 30 секунд</p>
                    <p><strong>📝 Формат:</strong> Время - Тип - Детали</p>
                    <p><strong>🎯 Всего типов:</strong> 8 видов событий</p>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Глобальные переменные
        let allEvents = [];
        let filteredEvents = [];
        let currentPage = 1;
        let eventsPerPage = 50;
        let chart = null;
        
        // Инициализация
        document.addEventListener('DOMContentLoaded', function() {
            loadHistory();
            setDateRange();
            
            // Обновляем каждые 30 секунд
            setInterval(loadHistory, 30000);
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
        
        // Установка диапазона дат по умолчанию (последние 7 дней)
        function setDateRange() {
            const today = new Date();
            const weekAgo = new Date();
            weekAgo.setDate(weekAgo.getDate() - 7);
            
            document.getElementById('dateTo').value = today.toISOString().split('T')[0];
            document.getElementById('dateFrom').value = weekAgo.toISOString().split('T')[0];
        }
        
        // Загрузка истории
        function loadHistory() {
            fetch('/cgi-bin/p/door_api.cgi?action=get_history&lines=1000')
                .then(r => r.json())
                .then(data => {
                    allEvents = data.events || [];
                    applyFilters();
                    updateStats();
                    getLogInfo();
                })
                .catch(error => {
                    console.error('Error loading history:', error);
                    showNotification('❌ Ошибка загрузки истории', 'error');
                });
        }
        
        // Применение фильтров
        function applyFilters() {
            const dateFrom = document.getElementById('dateFrom').value;
            const dateTo = document.getElementById('dateTo').value;
            const eventType = document.getElementById('eventType').value;
            const searchKey = document.getElementById('searchKey').value.toLowerCase();
            
            filteredEvents = allEvents.filter(event => {
                const msg = event.msg || '';
                const parts = msg.split(' - ');
                
                if (parts.length < 3) return false;
                
                const timeStr = parts[0] + ' ' + parts[1];
                const eventDate = new Date(timeStr);
                
                // Фильтр по дате
                if (dateFrom && eventDate < new Date(dateFrom)) return false;
                if (dateTo) {
                    const endDate = new Date(dateTo);
                    endDate.setHours(23, 59, 59);
                    if (eventDate > endDate) return false;
                }
                
                // Фильтр по типу события
                if (eventType !== 'all') {
                    const eventText = parts[2] || '';
                    if (eventType === 'open' && !eventText.includes('OPEN')) return false;
                    if (eventType === 'key_allowed' && !eventText.includes('ALLOWED')) return false;
                    if (eventType === 'key_denied' && !eventText.includes('DENIED')) return false;
                    if (eventType === 'call' && !eventText.includes('CALL')) return false;
                    if (eventType === 'button' && !eventText.includes('BUTTON')) return false;
                    if (eventType === 'esp' && !eventText.includes('ESP')) return false;
                }
                
                // Поиск по ключу или владельцу
                if (searchKey && !msg.toLowerCase().includes(searchKey)) return false;
                
                return true;
            });
            
            // Сортируем по убыванию времени
            filteredEvents.sort((a, b) => {
                const timeA = new Date(a.msg.split(' - ')[0] + ' ' + a.msg.split(' - ')[1]);
                const timeB = new Date(b.msg.split(' - ')[0] + ' ' + b.msg.split(' - ')[1]);
                return timeB - timeA;
            });
            
            currentPage = 1;
            renderTable();
            renderTimeline();
            renderChart();
            updatePagination();
        }
        
        // Сброс фильтров
        function clearFilters() {
            document.getElementById('eventType').value = 'all';
            document.getElementById('searchKey').value = '';
            setDateRange();
            applyFilters();
        }
        
        // Обновление статистики
        function updateStats() {
            let total = allEvents.length;
            let open = 0;
            let keySuccess = 0;
            let keyDenied = 0;
            
            allEvents.forEach(event => {
                const msg = event.msg || '';
                if (msg.includes('OPEN') && !msg.includes('KEY_')) open++;
                if (msg.includes('ALLOWED')) keySuccess++;
                if (msg.includes('DENIED')) keyDenied++;
            });
            
            document.getElementById('totalEvents').textContent = total;
            document.getElementById('openEvents').textContent = open;
            document.getElementById('keySuccess').textContent = keySuccess;
            document.getElementById('keyDenied').textContent = keyDenied;
        }
        
        // Отображение таблицы
        function renderTable() {
            const tbody = document.getElementById('historyList');
            
            if (filteredEvents.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 40px;">📭 Нет событий</td></tr>';
                document.getElementById('showingInfo').textContent = 'Показано 0 из 0 событий';
                return;
            }
            
            const start = (currentPage - 1) * eventsPerPage;
            const end = Math.min(start + eventsPerPage, filteredEvents.length);
            const pageEvents = filteredEvents.slice(start, end);
            
            let html = '';
            pageEvents.forEach(event => {
                const msg = event.msg || '';
                const parts = msg.split(' - ');
                
                if (parts.length >= 3) {
                    const time = parts[0] + ' ' + parts[1];
                    const eventText = parts[2];
                    
                    let type = 'unknown';
                    let icon = '📝';
                    let badge = 'badge-secondary';
                    let result = '-';
                    let key = '-';
                    let owner = '-';
                    let details = '';
                    
                    if (eventText.includes('OPEN') && !eventText.includes('KEY_')) {
                        type = 'open';
                        icon = '🚪';
                        badge = 'badge-success';
                        result = 'Открыто';
                        details = 'Дверь открыта';
                    } else if (eventText.includes('KEY_ADDED')) {
                        type = 'key_add';
                        icon = '➕';
                        badge = 'badge-info';
                        result = 'Добавлен';
                        key = eventText.split(' ')[2] || '-';
                    } else if (eventText.includes('KEY_REMOVED')) {
                        type = 'key_remove';
                        icon = '🗑️';
                        badge = 'badge-warning';
                        result = 'Удален';
                        key = eventText.split(' ')[2] || '-';
                    } else if (eventText.includes('ALLOWED')) {
                        type = 'key_allowed';
                        icon = '✅';
                        badge = 'badge-success';
                        result = 'Разрешен';
                        key = eventText.split(' ')[1] || '-';
                        const match = msg.match(/for (.*?)$/);
                        owner = match ? match[1] : '-';
                    } else if (eventText.includes('DENIED')) {
                        type = 'key_denied';
                        icon = '❌';
                        badge = 'badge-danger';
                        result = 'Запрещен';
                        key = eventText.split(' ')[1] || '-';
                    } else if (eventText.includes('CALL')) {
                        type = 'call';
                        icon = '📞';
                        badge = 'badge-info';
                        result = 'Звонок';
                        const match = eventText.match(/calling (.*)$/);
                        details = match ? match[1] : '-';
                    } else if (eventText.includes('BUTTON')) {
                        type = 'button';
                        icon = '🔘';
                        badge = 'badge-info';
                        result = 'Кнопка';
                        const match = eventText.match(/BUTTON:(.*)$/);
                        details = match ? match[1] : '-';
                    } else if (eventText.includes('ESP')) {
                        type = 'esp';
                        icon = '🤖';
                        badge = 'badge-info';
                        result = 'ESP';
                        details = eventText;
                    }
                    
                    html += '<tr onclick="showEventDetails(\'' + event.msg.replace(/'/g, "\\'") + '\')">' +
                        '<td>' + time + '</td>' +
                        '<td><span class="event-icon">' + icon + '</span> ' + type + '</td>' +
                        '<td>' + eventText + '</td>' +
                        '<td><span class="key-highlight">' + key + '</span></td>' +
                        '<td>' + owner + '</td>' +
                        '<td><span class="badge ' + badge + '">' + result + '</span></td>' +
                        '<td>' + details + '</td>' +
                        '</tr>';
                }
            });
            
            tbody.innerHTML = html;
            document.getElementById('showingInfo').textContent = 
                `Показано ${start + 1}-${end} из ${filteredEvents.length} событий`;
        }
        
        // Обновление пагинации
        function updatePagination() {
            const totalPages = Math.ceil(filteredEvents.length / eventsPerPage);
            const pagination = document.getElementById('pagination');
            
            if (totalPages <= 1) {
                pagination.innerHTML = '';
                return;
            }
            
            let html = '';
            
            // Кнопка "Назад"
            html += '<button class="page-btn" onclick="changePage(' + (currentPage - 1) + ')" ' +
                    (currentPage === 1 ? 'disabled' : '') + '>←</button>';
            
            // Номера страниц
            for (let i = 1; i <= totalPages; i++) {
                if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
                    html += '<button class="page-btn ' + (i === currentPage ? 'active' : '') + '" ' +
                            'onclick="changePage(' + i + ')">' + i + '</button>';
                } else if (i === currentPage - 3 || i === currentPage + 3) {
                    html += '<span class="page-btn disabled">...</span>';
                }
            }
            
            // Кнопка "Вперед"
            html += '<button class="page-btn" onclick="changePage(' + (currentPage + 1) + ')" ' +
                    (currentPage === totalPages ? 'disabled' : '') + '>→</button>';
            
            pagination.innerHTML = html;
        }
        
        // Смена страницы
        function changePage(page) {
            const totalPages = Math.ceil(filteredEvents.length / eventsPerPage);
            if (page < 1 || page > totalPages) return;
            
            currentPage = page;
            renderTable();
            updatePagination();
            
            // Прокрутка к началу таблицы
            document.getElementById('tableView').scrollIntoView({ behavior: 'smooth' });
        }
        
        // Отображение хронологии
        function renderTimeline() {
            const timeline = document.getElementById('timelineList');
            
            if (filteredEvents.length === 0) {
                timeline.innerHTML = '<div style="text-align: center; padding: 40px;">📭 Нет событий</div>';
                return;
            }
            
            let html = '';
            const events = filteredEvents.slice(0, 100); // Показываем последние 100
            
            events.forEach(event => {
                const msg = event.msg || '';
                const parts = msg.split(' - ');
                
                if (parts.length >= 3) {
                    const time = parts[0] + ' ' + parts[1];
                    const eventText = parts[2];
                    
                    let icon = '📝';
                    if (eventText.includes('OPEN')) icon = '🚪';
                    else if (eventText.includes('ALLOWED')) icon = '✅';
                    else if (eventText.includes('DENIED')) icon = '❌';
                    else if (eventText.includes('CALL')) icon = '📞';
                    else if (eventText.includes('BUTTON')) icon = '🔘';
                    else if (eventText.includes('ESP')) icon = '🤖';
                    
                    html += '<div class="timeline-item">' +
                        '<div class="timeline-time">' + time + '</div>' +
                        '<div class="timeline-content">' +
                        '<span style="font-size: 20px; margin-right: 10px;">' + icon + '</span>' +
                        '<span>' + eventText + '</span>' +
                        '</div>' +
                        '</div>';
                }
            });
            
            timeline.innerHTML = html;
        }
        
        // Отображение графика
        function renderChart() {
            const ctx = document.getElementById('activityChart');
            if (!ctx) return;
            
            // Подсчет событий по часам
            const hours = {};
            for (let i = 0; i < 24; i++) hours[i] = 0;
            
            filteredEvents.forEach(event => {
                const msg = event.msg || '';
                const parts = msg.split(' - ');
                if (parts.length >= 3) {
                    const timeStr = parts[1];
                    const hour = parseInt(timeStr.split(':')[0]);
                    if (!isNaN(hour)) hours[hour]++;
                }
            });
            
            if (chart) chart.destroy();
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({length: 24}, (_, i) => i + ':00'),
                    datasets: [{
                        label: 'Количество событий',
                        data: Object.values(hours),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102,126,234,0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0,0,0,0.05)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
        
        // Переключение видов
        function showTableView() {
            document.getElementById('tableView').style.display = 'block';
            document.getElementById('timelineView').style.display = 'none';
            document.getElementById('chartView').style.display = 'none';
            
            document.getElementById('viewTableBtn').className = 'btn btn-sm btn-info';
            document.getElementById('viewTimelineBtn').className = 'btn btn-sm btn-secondary';
            document.getElementById('viewChartBtn').className = 'btn btn-sm btn-secondary';
        }
        
        function showTimelineView() {
            document.getElementById('tableView').style.display = 'none';
            document.getElementById('timelineView').style.display = 'block';
            document.getElementById('chartView').style.display = 'none';
            
            document.getElementById('viewTableBtn').className = 'btn btn-sm btn-secondary';
            document.getElementById('viewTimelineBtn').className = 'btn btn-sm btn-info';
            document.getElementById('viewChartBtn').className = 'btn btn-sm btn-secondary';
            
            renderTimeline();
        }
        
        function showChartView() {
            document.getElementById('tableView').style.display = 'none';
            document.getElementById('timelineView').style.display = 'none';
            document.getElementById('chartView').style.display = 'block';
            
            document.getElementById('viewTableBtn').className = 'btn btn-sm btn-secondary';
            document.getElementById('viewTimelineBtn').className = 'btn btn-sm btn-secondary';
            document.getElementById('viewChartBtn').className = 'btn btn-sm btn-info';
            
            renderChart();
        }
        
        // Обновление истории
        function refreshHistory() {
            loadHistory();
            showNotification('🔄 История обновлена', 'success');
        }
        
        // Очистка истории
        function clearHistory() {
            if (!confirm('🗑️ Очистить всю историю событий?')) return;
            
            fetch('/cgi-bin/p/door_api.cgi?action=clear_history', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        showNotification('✅ История очищена', 'success');
                        loadHistory();
                    } else {
                        showNotification('❌ ' + data.message, 'error');
                    }
                })
                .catch(error => {
                    showNotification('❌ Ошибка: ' + error, 'error');
                });
        }
        
        // Экспорт в CSV
        function exportCSV() {
            let csv = 'Время,Тип,Событие,Ключ,Владелец,Результат,Детали\n';
            
            filteredEvents.forEach(event => {
                const msg = event.msg || '';
                const parts = msg.split(' - ');
                
                if (parts.length >= 3) {
                    const time = parts[0] + ' ' + parts[1];
                    const eventText = parts[2].replace(/,/g, ';');
                    csv += `"${time}",,,,,"${eventText}",\n`;
                }
            });
            
            const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'door_history_' + new Date().toISOString().slice(0,10) + '.csv';
            link.click();
            
            showNotification('📥 Экспорт завершен', 'success');
        }
        
        // Экспорт в JSON
        function exportJSON() {
            const data = JSON.stringify(filteredEvents, null, 2);
            const blob = new Blob([data], { type: 'application/json' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'door_history_' + new Date().toISOString().slice(0,10) + '.json';
            link.click();
            
            showNotification('📥 Экспорт завершен', 'success');
        }
        
        // Экспорт в TXT
        function exportTXT() {
            let text = '';
            filteredEvents.forEach(event => {
                text += event.msg + '\n';
            });
            
            const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'door_history_' + new Date().toISOString().slice(0,10) + '.txt';
            link.click();
            
            showNotification('📥 Экспорт завершен', 'success');
        }
        
        // Информация о логе
        function getLogInfo() {
            fetch('/cgi-bin/p/door_api.cgi?action=log_info')
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('logSize').textContent = data.size || '-';
                        document.getElementById('firstEntry').textContent = data.first || '-';
                    }
                })
                .catch(error => {
                    console.error('Error getting log info:', error);
                });
        }
        
        // Детали события
        function showEventDetails(msg) {
            showNotification(msg, 'info');
        }
    </script>
</body>
</html>
EOFH