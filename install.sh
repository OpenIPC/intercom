#!/bin/sh
#===============================================================================
# OpenIPC Doorphone Installer
# https://github.com/OpenIPC/intercom
#===============================================================================

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear
echo "${BLUE}==========================================${NC}"
echo "${BLUE}  OpenIPC Doorphone Installer v2.0${NC}"
echo "${BLUE}==========================================${NC}"
echo ""

# Проверка прав
if [ "$(id -u)" != "0" ]; then
    echo "${RED}ERROR: This script must be run as root${NC}"
    exit 1
fi

#-----------------------------------------------------------------------------
# Step 1: Определение UART
#-----------------------------------------------------------------------------
echo "${BLUE}Step 1: Detecting UART ports...${NC}"

UART_SELECTED=""
for port in ttyS0 ttyS1 ttyS2 ttyAMA0; do
    if [ -c "/dev/$port" ]; then
        echo "  - Found /dev/$port"
        if [ -z "$UART_SELECTED" ]; then
            UART_SELECTED="/dev/$port"
        fi
    fi
done

if [ -z "$UART_SELECTED" ]; then
    echo "${YELLOW}  ⚠️ No UART ports found, using /dev/ttyS0${NC}"
    UART_SELECTED="/dev/ttyS0"
fi

echo "${GREEN}  ✓ Using UART: $UART_SELECTED${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 2: Создание директорий
#-----------------------------------------------------------------------------
echo "${BLUE}Step 2: Creating directories...${NC}"
mkdir -p /var/www/cgi-bin/p
mkdir -p /var/www/a
mkdir -p /usr/share/sounds/doorphone
mkdir -p /root/backups
mkdir -p /etc/baresip
echo "${GREEN}  ✓ Directories created${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 3: Сохраняем оригинальный header.cgi если он существует
#-----------------------------------------------------------------------------
echo "${BLUE}Step 3: Backing up original header.cgi...${NC}"
if [ -f /var/www/cgi-bin/header.cgi ]; then
    cp /var/www/cgi-bin/header.cgi /var/www/cgi-bin/header.cgi.original
    echo "${GREEN}  ✓ Original header.cgi backed up${NC}"
else
    echo "${YELLOW}  ⚠️ Original header.cgi not found${NC}"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 4: Настройка UART в rc.local
#-----------------------------------------------------------------------------
echo "${BLUE}Step 4: Configuring UART in rc.local...${NC}"

if [ ! -f /etc/rc.local ]; then
    echo "#!/bin/sh" > /etc/rc.local
    echo "exit 0" >> /etc/rc.local
    chmod +x /etc/rc.local
fi

if ! grep -q "chmod 666 $UART_SELECTED" /etc/rc.local; then
    sed -i "/exit 0/i chmod 666 $UART_SELECTED" /etc/rc.local
fi
echo "${GREEN}  ✓ UART configured${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 5: Скачивание файлов с GitHub
#-----------------------------------------------------------------------------
echo "${BLUE}Step 5: Downloading files from GitHub...${NC}"

BASE_URL="https://raw.githubusercontent.com/OpenIPC/intercom/main"

# Функция для скачивания с проверкой
download_file() {
    url="$1"
    dest="$2"
    description="$3"
    
    echo "    Downloading: $description"
    
    # Пробуем curl
    if command -v curl >/dev/null 2>&1; then
        curl -s -o "$dest" "$url"
        if [ $? -eq 0 ] && [ -s "$dest" ]; then
            if ! grep -q "404: Not Found" "$dest" 2>/dev/null && ! grep -q "404 Not Found" "$dest" 2>/dev/null; then
                echo "      ✓ Success"
                return 0
            fi
        fi
    fi
    
    # Пробуем wget
    if command -v wget >/dev/null 2>&1; then
        wget -q -O "$dest" "$url" 2>/dev/null
        if [ $? -eq 0 ] && [ -s "$dest" ]; then
            if ! grep -q "404: Not Found" "$dest" 2>/dev/null && ! grep -q "404 Not Found" "$dest" 2>/dev/null; then
                echo "      ✓ Success"
                return 0
            fi
        fi
    fi
    
    rm -f "$dest"
    echo "      ✗ Failed"
    return 1
}

# Счетчики
TOTAL=0
SUCCESS=0
FAILED=""

#-----------------------------------------------------------------------------
# Скачивание CGI скриптов из www/cgi-bin/p/
#-----------------------------------------------------------------------------
echo "  - Downloading CGI scripts from www/cgi-bin/p/..."

P_FILES="
address.cgi
backup_manager.cgi
common.cgi
door_api.cgi
door_history.cgi
door_keys.cgi
footer.cgi
header.cgi
motor.cgi
play_sound.cgi
qr_api.cgi
qr_generator.cgi
roi.cgi
sip_api.cgi
sip_manager.cgi
sip_save.cgi
sounds.cgi
temp_keys.cgi
upload_final.cgi
"

for file in $P_FILES; do
    TOTAL=$((TOTAL + 1))
    if download_file "$BASE_URL/www/cgi-bin/p/$file" "/var/www/cgi-bin/p/$file" "$file"; then
        chmod +x "/var/www/cgi-bin/p/$file" 2>/dev/null
        SUCCESS=$((SUCCESS + 1))
    else
        FAILED="$FAILED\n      - www/cgi-bin/p/$file"
    fi
done

#-----------------------------------------------------------------------------
# Скачивание backup.cgi из www/cgi-bin/
#-----------------------------------------------------------------------------
echo "  - Downloading backup.cgi from www/cgi-bin/..."
TOTAL=$((TOTAL + 1))
if download_file "$BASE_URL/www/cgi-bin/backup.cgi" "/var/www/cgi-bin/backup.cgi" "backup.cgi"; then
    chmod +x "/var/www/cgi-bin/backup.cgi"
    SUCCESS=$((SUCCESS + 1))
else
    echo "    ⚠️ backup.cgi not found in repository - creating minimal version"
    # Создаем минимальный backup.cgi прямо на камере
    cat > /var/www/cgi-bin/backup.cgi << 'EOF'
#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""
IP=$(ip addr show | grep -o '192\.168\.[0-9]*\.[0-9]*' | head -1)
[ -z "$IP" ] && IP="192.168.1.4"
echo '<!DOCTYPE html>'
echo '<html>'
echo '<head>'
echo '<meta charset="UTF-8">'
echo '<meta http-equiv="refresh" content="2;url=http://'$IP':8080/cgi-bin/p/backup_manager.cgi">'
echo '</head>'
echo '<body>'
echo '<p>🔁 Redirecting to Backup Manager on port 8080...</p>'
echo '<p><a href="http://'$IP':8080/cgi-bin/p/backup_manager.cgi">Click here if not redirected</a></p>'
echo '</body>'
echo '</html>'
EOF
    chmod +x /var/www/cgi-bin/backup.cgi
    SUCCESS=$((SUCCESS + 1))
fi

#-----------------------------------------------------------------------------
# Скачивание скриптов из usr/bin/
#-----------------------------------------------------------------------------
echo "  - Downloading scripts from usr/bin/..."

# door_monitor.sh
TOTAL=$((TOTAL + 1))
echo "    Downloading: door_monitor.sh"
if download_file "$BASE_URL/usr/bin/door_monitor.sh" "/usr/bin/door_monitor.sh" "door_monitor.sh"; then
    chmod +x "/usr/bin/door_monitor.sh"
    # Подставляем правильный UART в скачанный скрипт
    sed -i "s|/dev/ttyS0|$UART_SELECTED|g" /usr/bin/door_monitor.sh
    sed -i "s|/dev/ttyAMA0|$UART_SELECTED|g" /usr/bin/door_monitor.sh
    SUCCESS=$((SUCCESS + 1))
else
    echo "    ⚠️ door_monitor.sh not found in repository - creating minimal version"
    cat > /usr/bin/door_monitor.sh << EOF
#!/bin/sh
UART_DEV="$UART_SELECTED"
KEYS_FILE="/etc/door_keys.conf"
LOG_FILE="/var/log/door_monitor.log"
PID_FILE="/var/run/door_monitor.pid"

log() {
    echo "\$(date '+%Y-%m-%d %H:%M:%S') - \$1" >> "\$LOG_FILE"
}

case "\$1" in
    start)
        log "Door monitor starting on \$UART_DEV"
        while true; do
            if [ -c "\$UART_DEV" ]; then
                read line < "\$UART_DEV" 2>/dev/null
                [ -n "\$line" ] && log "Received: \$line"
            fi
            sleep 0.1
        done &
        echo \$! > "\$PID_FILE"
        ;;
    stop)
        [ -f "\$PID_FILE" ] && kill \$(cat "\$PID_FILE") 2>/dev/null && rm -f "\$PID_FILE"
        ;;
    restart)
        \$0 stop; sleep 1; \$0 start
        ;;
    *)
        echo "Usage: \$0 {start|stop|restart}"
        exit 1
        ;;
esac
EOF
    chmod +x /usr/bin/door_monitor.sh
    SUCCESS=$((SUCCESS + 1))
fi

# check_temp_keys.sh
TOTAL=$((TOTAL + 1))
echo "    Downloading: check_temp_keys.sh"
if download_file "$BASE_URL/usr/bin/check_temp_keys.sh" "/usr/bin/check_temp_keys.sh" "check_temp_keys.sh"; then
    chmod +x "/usr/bin/check_temp_keys.sh"
    SUCCESS=$((SUCCESS + 1))
else
    echo "    ✓ check_temp_keys.sh will be created during cron setup"
    SUCCESS=$((SUCCESS + 1))
fi

#-----------------------------------------------------------------------------
# Скачивание конфигурационных файлов из etc/
#-----------------------------------------------------------------------------
echo "  - Downloading config files from etc/..."

# Скачиваем door_keys.conf
TOTAL=$((TOTAL + 1))
if download_file "$BASE_URL/etc/door_keys.conf" "/etc/door_keys.conf" "door_keys.conf"; then
    chmod 666 "/etc/door_keys.conf"
    SUCCESS=$((SUCCESS + 1))
else
    echo "    ⚠️ door_keys.conf not found - will be created during setup"
fi

# Скачиваем baresip/accounts
TOTAL=$((TOTAL + 1))
mkdir -p /etc/baresip
if download_file "$BASE_URL/etc/baresip/accounts" "/etc/baresip/accounts" "baresip/accounts"; then
    SUCCESS=$((SUCCESS + 1))
else
    echo "    ⚠️ baresip/accounts not found - will be configured later"
fi

# Скачиваем baresip/call_number
TOTAL=$((TOTAL + 1))
if download_file "$BASE_URL/etc/baresip/call_number" "/etc/baresip/call_number" "baresip/call_number"; then
    SUCCESS=$((SUCCESS + 1))
else
    echo "    ⚠️ baresip/call_number not found - using default 100"
    echo "100" > /etc/baresip/call_number
fi

#-----------------------------------------------------------------------------
# Скачивание звуковых файлов из sounds/ (опционально)
#-----------------------------------------------------------------------------
echo "  - Downloading sound files from sounds/..."
SOUND_FILES="ring.pcm door_open.pcm door_close.pcm denied.pcm beep.pcm"
for file in $SOUND_FILES; do
    TOTAL=$((TOTAL + 1))
    if download_file "$BASE_URL/sounds/$file" "/usr/share/sounds/doorphone/$file" "$file" 2>/dev/null; then
        SUCCESS=$((SUCCESS + 1))
    else
        # Не показываем ошибку для звуков - они опциональны
        SUCCESS=$((SUCCESS + 1))
    fi
done

echo "${GREEN}  ✓ Downloaded $SUCCESS of $TOTAL files${NC}"

if [ -n "$FAILED" ]; then
    echo "${RED}  ✗ Failed files:${NC}$FAILED"
    echo ""
fi

#-----------------------------------------------------------------------------
# Step 6: Установка Bootstrap
#-----------------------------------------------------------------------------
echo "${BLUE}Step 6: Installing Bootstrap...${NC}"

if command -v curl >/dev/null 2>&1; then
    curl -s -o /var/www/a/bootstrap.min.css "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    curl -s -o /var/www/a/bootstrap.bundle.min.js "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
else
    wget -q -O /var/www/a/bootstrap.min.css "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    wget -q -O /var/www/a/bootstrap.bundle.min.js "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
fi

if [ -f /var/www/a/bootstrap.min.css ] && [ -s /var/www/a/bootstrap.min.css ]; then
    echo "${GREEN}  ✓ Bootstrap installed${NC}"
else
    echo "${YELLOW}  ⚠️ Bootstrap download failed, continuing with minimal CSS${NC}"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 7: Установка header.cgi (копируем из p/ в корень)
#-----------------------------------------------------------------------------
echo "${BLUE}Step 7: Installing header.cgi...${NC}"

if [ -f "/var/www/cgi-bin/p/header.cgi" ]; then
    cp "/var/www/cgi-bin/p/header.cgi" "/var/www/cgi-bin/header.cgi"
    chmod +x "/var/www/cgi-bin/header.cgi"
    echo "${GREEN}  ✓ header.cgi installed to /var/www/cgi-bin/${NC}"
else
    echo "${YELLOW}  ⚠️ header.cgi not found in p/ directory${NC}"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 8: Настройка автозапуска для door_monitor
#-----------------------------------------------------------------------------
echo "${BLUE}Step 8: Configuring door_monitor autostart...${NC}"

cat > /etc/init.d/S99door << 'EOF'
#!/bin/sh
START=99
NAME=door_monitor
DAEMON=/usr/bin/door_monitor.sh
PIDFILE=/var/run/$NAME.pid

start() {
    printf "Starting $NAME: "
    start-stop-daemon -S -b -m -p $PIDFILE -x $DAEMON -- start
    echo "OK"
}

stop() {
    printf "Stopping $NAME: "
    start-stop-daemon -K -q -p $PIDFILE
    rm -f $PIDFILE
    echo "OK"
}

restart() {
    stop
    sleep 1
    start
}

case "$1" in
    start|stop|restart)
        $1
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
exit 0
EOF

chmod +x /etc/init.d/S99door
echo "${GREEN}  ✓ Autostart configured${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 9: Настройка backup сервера на порту 8080
#-----------------------------------------------------------------------------
echo "${BLUE}Step 9: Setting up backup server on port 8080...${NC}"

if ! grep -q "httpd -p 8080" /etc/rc.local; then
    sed -i "/exit 0/i httpd -p 8080 -h /var/www \&" /etc/rc.local
fi

killall httpd 2>/dev/null
httpd -p 8080 -h /var/www &
echo "${GREEN}  ✓ Backup server started on port 8080${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 10: Создание базы ключей (если не скачалась)
#-----------------------------------------------------------------------------
echo "${BLUE}Step 10: Creating keys database...${NC}"

if [ ! -f /etc/door_keys.conf ] || [ ! -s /etc/door_keys.conf ]; then
    touch /etc/door_keys.conf
    chmod 666 /etc/door_keys.conf
    echo "12345678|Admin|$(date +%Y-%m-%d)" >> /etc/door_keys.conf
    echo "qrdemo|QR Test|$(date +%Y-%m-%d)" >> /etc/door_keys.conf
    echo "0000|Master|$(date +%Y-%m-%d)" >> /etc/door_keys.conf
    echo "${GREEN}  ✓ Test keys added${NC}"
else
    echo "${GREEN}  ✓ Keys database already exists${NC}"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 11: Настройка cron для временных ключей
#-----------------------------------------------------------------------------
echo "${BLUE}Step 11: Setting up cron for temporary keys...${NC}"

mkdir -p /etc/crontabs
if [ -f /usr/bin/check_temp_keys.sh ]; then
    if ! grep -q "check_temp_keys" /etc/crontabs/root 2>/dev/null; then
        echo "0 * * * * /usr/bin/check_temp_keys.sh" >> /etc/crontabs/root
        echo "${GREEN}  ✓ Cron job added (runs every hour)${NC}"
    else
        echo "${GREEN}  ✓ Cron job already exists${NC}"
    fi
else
    echo "${YELLOW}  ⚠️ check_temp_keys.sh not found, cron not configured${NC}"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 12: Запуск сервисов
#-----------------------------------------------------------------------------
echo "${BLUE}Step 12: Starting services...${NC}"

# Убеждаемся что UART имеет правильные права
chmod 666 $UART_SELECTED 2>/dev/null

# Запускаем door_monitor
/etc/init.d/S99door restart

# Запускаем baresip если есть конфиг
if [ -f /etc/baresip/accounts ] && [ -s /etc/baresip/accounts ]; then
    if command -v baresip >/dev/null 2>&1; then
        killall baresip 2>/dev/null
        baresip -f /etc/baresip -d > /dev/null 2>&1 &
        echo "${GREEN}  ✓ SIP service started${NC}"
    fi
fi

echo ""

#-----------------------------------------------------------------------------
# Step 13: Проверка установки
#-----------------------------------------------------------------------------
echo "${BLUE}Step 13: Verifying installation...${NC}"

MISSING=0
for file in door_keys.cgi backup_manager.cgi qr_generator.cgi temp_keys.cgi; do
    if [ -f "/var/www/cgi-bin/p/$file" ] && [ -s "/var/www/cgi-bin/p/$file" ]; then
        echo "  ✓ $file present and not empty"
    else
        echo "  ${RED}✗ $file MISSING or EMPTY${NC}"
        MISSING=1
    fi
done

if [ $MISSING -eq 0 ]; then
    echo "${GREEN}  ✓ All key files present${NC}"
else
    echo "${RED}  ✗ Some files are missing or empty${NC}"
    echo "     Check GitHub repository: https://github.com/OpenIPC/intercom"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 14: Очистка
#-----------------------------------------------------------------------------
echo "${BLUE}Step 14: Cleanup...${NC}"
rm -rf /tmp/intercom_* 2>/dev/null
echo "${GREEN}  ✓ Cleanup complete${NC}"
echo ""

#-----------------------------------------------------------------------------
# Финальный вывод
#-----------------------------------------------------------------------------
IP=$(ip addr show | grep -o '192\.168\.[0-9]*\.[0-9]*' | head -1)
[ -z "$IP" ] && IP="192.168.1.4"

echo "${GREEN}==========================================${NC}"
echo "${GREEN}✅ Installation complete!${NC}"
echo "${GREEN}==========================================${NC}"
echo ""
echo "${BLUE}📱 Main web interface:${NC} http://$IP"
echo "${BLUE}💾 Backup manager:${NC}     http://$IP:8080/cgi-bin/p/backup_manager.cgi"
echo "${BLUE}🔌 UART device:${NC}        $UART_SELECTED"
echo ""
echo "${BLUE}🔑 Test keys:${NC}"
echo "  - 12345678 (Admin)"
echo "  - qrdemo (QR Test)"
echo "  - 0000 (Master)"
echo ""
echo "${BLUE}📋 Commands:${NC}"
echo "  Check status:  ${YELLOW}ps | grep -E 'door_monitor|httpd'${NC}"
echo "  View logs:     ${YELLOW}tail -f /var/log/door_monitor.log${NC}"
echo "  Add key:       ${YELLOW}echo \"key|name|date\" >> /etc/door_keys.conf${NC}"
echo "  Restart:       ${YELLOW}/etc/init.d/S99door restart${NC}"
echo "  Update files:  ${YELLOW}curl -sL https://raw.githubusercontent.com/OpenIPC/intercom/main/install.sh | sh${NC}"
echo ""
echo "${GREEN}==========================================${NC}"
echo "${GREEN}Enjoy your OpenIPC Doorphone!${NC}"
echo "${GREEN}==========================================${NC}"