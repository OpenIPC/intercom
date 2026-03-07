#!/bin/sh
#===============================================================================
# OpenIPC Doorphone Installer v4.0
# https://github.com/OpenIPC/intercom
#===============================================================================
# SAFE INSTALLATION MODE:
# 1. Все файлы сначала скачиваются в /tmp/intercom_new/
# 2. Проверяется, что все необходимые файлы скачались
# 3. Только после успешной проверки происходит замена
# 4. В случае ошибки - камера остаётся работоспособной
#===============================================================================

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear
echo "${BLUE}==========================================${NC}"
echo "${BLUE}  OpenIPC Doorphone Installer v4.0${NC}"
echo "${BLUE}  SAFE INSTALLATION MODE${NC}"
echo "${BLUE}==========================================${NC}"
echo ""

# Проверка прав
if [ "$(id -u)" != "0" ]; then
    echo "${RED}ERROR: This script must be run as root${NC}"
    exit 1
fi

#-----------------------------------------------------------------------------
# Функция для скачивания
#-----------------------------------------------------------------------------
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

# Базовый URL с фиксированным хешем коммита
BASE_URL="https://raw.githubusercontent.com/OpenIPC/intercom/50bf937"

#-----------------------------------------------------------------------------
# Step 1: ОСТАНОВКА СЕРВИСОВ
#-----------------------------------------------------------------------------
echo "${BLUE}Step 1: Stopping services...${NC}"

# Останавливаем наши сервисы
killall door_monitor.sh 2>/dev/null
killall mqtt_client.sh 2>/dev/null
killall baresip 2>/dev/null
killall httpd 2>/dev/null

# Удаляем старые PID файлы
rm -f /var/run/door_monitor.pid 2>/dev/null

echo "${GREEN}  ✓ Services stopped${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 2: Определение UART
#-----------------------------------------------------------------------------
echo "${BLUE}Step 2: Detecting UART ports...${NC}"

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
# Step 3: СОЗДАНИЕ ВРЕМЕННОЙ ДИРЕКТОРИИ
#-----------------------------------------------------------------------------
echo "${BLUE}Step 3: Creating temporary directory...${NC}"

TEMP_DIR="/tmp/intercom_install_$$"
mkdir -p "$TEMP_DIR"
mkdir -p "$TEMP_DIR/www/cgi-bin/p"
mkdir -p "$TEMP_DIR/usr/bin"
mkdir -p "$TEMP_DIR/etc"
mkdir -p "$TEMP_DIR/etc/baresip"
mkdir -p "$TEMP_DIR/etc/webui"
mkdir -p "$TEMP_DIR/usr/share/sounds/doorphone"

echo "${GREEN}  ✓ Temporary directory created: $TEMP_DIR${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 4: СКАЧИВАНИЕ ВСЕХ ФАЙЛОВ ВО ВРЕМЕННУЮ ДИРЕКТОРИЮ
#-----------------------------------------------------------------------------
echo "${BLUE}Step 4: Downloading files to temporary directory...${NC}"

TOTAL=0
SUCCESS=0
FAILED=""

# Список всех файлов для скачивания
FILES="
www/cgi-bin/header.cgi
www/cgi-bin/backup.cgi
www/cgi-bin/p/door_keys.cgi
www/cgi-bin/p/sip_manager.cgi
www/cgi-bin/p/qr_generator.cgi
www/cgi-bin/p/temp_keys.cgi
www/cgi-bin/p/sounds.cgi
www/cgi-bin/p/door_history.cgi
www/cgi-bin/p/mqtt.cgi
www/cgi-bin/p/mqtt_status.cgi
www/cgi-bin/p/mqtt_api.cgi
www/cgi-bin/p/backup_manager.cgi
www/cgi-bin/p/backup_api.cgi
www/cgi-bin/p/door_api.cgi
www/cgi-bin/p/sip_api.cgi
www/cgi-bin/p/sip_save.cgi
www/cgi-bin/p/play_sound.cgi
www/cgi-bin/p/upload_final.cgi
www/cgi-bin/p/common.cgi
usr/bin/door_monitor.sh
usr/bin/mqtt_client.sh
usr/bin/check_temp_keys.sh
etc/door_keys.conf
etc/mqtt.conf
etc/doorphone_sounds.conf
etc/baresip/accounts
etc/baresip/call_number
sounds/ring.pcm
sounds/door_open.pcm
sounds/door_close.pcm
sounds/denied.pcm
sounds/beep.pcm
sounds/success.pcm
sounds/error.pcm
"

for file in $FILES; do
    TOTAL=$((TOTAL + 1))
    dest="$TEMP_DIR/$file"
    mkdir -p "$(dirname "$dest")"
    
    if download_file "$BASE_URL/$file" "$dest" "$file"; then
        SUCCESS=$((SUCCESS + 1))
    else
        FAILED="$FAILED\n      - $file"
    fi
done

echo "${GREEN}  ✓ Downloaded $SUCCESS of $TOTAL files${NC}"
[ -n "$FAILED" ] && echo "${RED}  ✗ Failed files:$FAILED${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 5: ПРОВЕРКА КРИТИЧЕСКИХ ФАЙЛОВ
#-----------------------------------------------------------------------------
echo "${BLUE}Step 5: Checking critical files...${NC}"

CRITICAL_FILES="
www/cgi-bin/header.cgi
www/cgi-bin/p/door_keys.cgi
usr/bin/door_monitor.sh
etc/door_keys.conf
"

MISSING_CRITICAL=0
for file in $CRITICAL_FILES; do
    if [ ! -f "$TEMP_DIR/$file" ]; then
        echo "${RED}  ✗ CRITICAL FILE MISSING: $file${NC}"
        MISSING_CRITICAL=1
    else
        echo "  ✓ $file present"
    fi
done

if [ $MISSING_CRITICAL -eq 1 ]; then
    echo "${RED}❌ Critical files missing! Aborting installation.${NC}"
    echo "${YELLOW}   Camera remains unchanged.${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
fi
echo ""

#-----------------------------------------------------------------------------
# Step 6: БЭКАП ТЕКУЩИХ ФАЙЛОВ (на всякий случай)
#-----------------------------------------------------------------------------
echo "${BLUE}Step 6: Backing up current files...${NC}"

BACKUP_DIR="/root/intercom_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Копируем текущие файлы в бэкап
[ -d /var/www/cgi-bin/p ] && cp -r /var/www/cgi-bin/p "$BACKUP_DIR/" 2>/dev/null
[ -f /var/www/cgi-bin/header.cgi ] && cp /var/www/cgi-bin/header.cgi "$BACKUP_DIR/" 2>/dev/null
[ -f /var/www/cgi-bin/backup.cgi ] && cp /var/www/cgi-bin/backup.cgi "$BACKUP_DIR/" 2>/dev/null
[ -d /usr/bin/door_monitor.sh ] && cp /usr/bin/door_monitor.sh "$BACKUP_DIR/" 2>/dev/null
[ -f /usr/bin/mqtt_client.sh ] && cp /usr/bin/mqtt_client.sh "$BACKUP_DIR/" 2>/dev/null
[ -f /usr/bin/check_temp_keys.sh ] && cp /usr/bin/check_temp_keys.sh "$BACKUP_DIR/" 2>/dev/null
[ -f /etc/door_keys.conf ] && cp /etc/door_keys.conf "$BACKUP_DIR/" 2>/dev/null
[ -f /etc/mqtt.conf ] && cp /etc/mqtt.conf "$BACKUP_DIR/" 2>/dev/null
[ -f /etc/doorphone_sounds.conf ] && cp /etc/doorphone_sounds.conf "$BACKUP_DIR/" 2>/dev/null
[ -d /etc/baresip ] && cp -r /etc/baresip "$BACKUP_DIR/" 2>/dev/null
[ -f /etc/webui/telegram.conf ] && cp /etc/webui/telegram.conf "$BACKUP_DIR/" 2>/dev/null

echo "${GREEN}  ✓ Backup saved to: $BACKUP_DIR${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 7: УСТАНОВКА НОВЫХ ФАЙЛОВ
#-----------------------------------------------------------------------------
echo "${BLUE}Step 7: Installing new files...${NC}"

# Копируем все файлы из временной директории в целевые
cp -rf "$TEMP_DIR/www/cgi-bin/header.cgi" /var/www/cgi-bin/ 2>/dev/null
cp -rf "$TEMP_DIR/www/cgi-bin/backup.cgi" /var/www/cgi-bin/ 2>/dev/null
cp -rf "$TEMP_DIR/www/cgi-bin/p"/* /var/www/cgi-bin/p/ 2>/dev/null
cp -rf "$TEMP_DIR/usr/bin"/* /usr/bin/ 2>/dev/null
cp -rf "$TEMP_DIR/etc/door_keys.conf" /etc/ 2>/dev/null
cp -rf "$TEMP_DIR/etc/mqtt.conf" /etc/ 2>/dev/null
cp -rf "$TEMP_DIR/etc/doorphone_sounds.conf" /etc/ 2>/dev/null
cp -rf "$TEMP_DIR/etc/baresip"/* /etc/baresip/ 2>/dev/null
cp -rf "$TEMP_DIR/usr/share/sounds/doorphone"/* /usr/share/sounds/doorphone/ 2>/dev/null

# Устанавливаем права
chmod +x /var/www/cgi-bin/*.cgi 2>/dev/null
chmod +x /var/www/cgi-bin/p/*.cgi 2>/dev/null
chmod +x /usr/bin/door_monitor.sh 2>/dev/null
chmod +x /usr/bin/mqtt_client.sh 2>/dev/null
chmod +x /usr/bin/check_temp_keys.sh 2>/dev/null
chmod 666 /etc/door_keys.conf 2>/dev/null
chmod 644 /etc/mqtt.conf 2>/dev/null
chmod 644 /etc/doorphone_sounds.conf 2>/dev/null

# Подставляем правильный UART в скрипты
sed -i "s|/dev/ttyS0|$UART_SELECTED|g" /usr/bin/door_monitor.sh 2>/dev/null
sed -i "s|/dev/ttyAMA0|$UART_SELECTED|g" /usr/bin/door_monitor.sh 2>/dev/null
sed -i "s|/dev/ttyS0|$UART_SELECTED|g" /usr/bin/mqtt_client.sh 2>/dev/null
sed -i "s|/dev/ttyAMA0|$UART_SELECTED|g" /usr/bin/mqtt_client.sh 2>/dev/null

echo "${GREEN}  ✓ Files installed${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 8: ОЧИСТКА ВРЕМЕННОЙ ДИРЕКТОРИИ
#-----------------------------------------------------------------------------
echo "${BLUE}Step 8: Cleaning up...${NC}"
rm -rf "$TEMP_DIR"
echo "${GREEN}  ✓ Temporary directory removed${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 9: НАСТРОЙКА UART В rc.local
#-----------------------------------------------------------------------------
echo "${BLUE}Step 9: Configuring UART in rc.local...${NC}"

if [ ! -f /etc/rc.local ]; then
    echo "#!/bin/sh" > /etc/rc.local
    echo "exit 0" >> /etc/rc.local
    chmod +x /etc/rc.local
fi

# Удаляем старые настройки
sed -i '/stty -F/d' /etc/rc.local
sed -i '/mqtt_client.sh/d' /etc/rc.local
sed -i '/httpd -p 8080/d' /etc/rc.local

# Добавляем новые настройки
sed -i "/exit 0/i stty -F $UART_SELECTED 115200 cs8 -cstopb -parenb raw" /etc/rc.local
sed -i "/exit 0/i # Start MQTT client\nif [ -f /etc/mqtt.conf ]; then\n    . /etc/mqtt.conf\n    if [ \"\$MQTT_ENABLED\" = \"true\" ]; then\n        /usr/bin/mqtt_client.sh monitor > /dev/null 2>&1 &\n    fi\nfi" /etc/rc.local
sed -i "/exit 0/i httpd -p 8080 -h /var/www \&" /etc/rc.local

chmod +x /etc/rc.local
echo "${GREEN}  ✓ UART and services configured${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 10: НАСТРОЙКА АВТОЗАПУСКА
#-----------------------------------------------------------------------------
echo "${BLUE}Step 10: Configuring autostart...${NC}"

cat > /etc/init.d/S99door << 'EOF'
#!/bin/sh
START=99
NAME=door_monitor
DAEMON=/usr/bin/door_monitor.sh
PIDFILE=/var/run/$NAME.pid

start() {
    printf "Starting $NAME: "
    start-stop-daemon -S -b -m -p $PIDFILE -x $DAEMON
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
    start|stop|restart) $1 ;;
    *) echo "Usage: $0 {start|stop|restart}"; exit 1 ;;
esac
exit 0
EOF

chmod +x /etc/init.d/S99door
echo "${GREEN}  ✓ Autostart configured${NC}"
echo ""

#-----------------------------------------------------------------------------
# Step 11: НАСТРОЙКА CRON
#-----------------------------------------------------------------------------
echo "${BLUE}Step 11: Setting up cron for temporary keys...${NC}"

mkdir -p /etc/crontabs
sed -i '/check_temp_keys/d' /etc/crontabs/root 2>/dev/null

if [ -f /usr/bin/check_temp_keys.sh ]; then
    echo "0 * * * * /usr/bin/check_temp_keys.sh" >> /etc/crontabs/root
    echo "${GREEN}  ✓ Cron job added${NC}"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 12: УСТАНОВКА BOOTSTRAP
#-----------------------------------------------------------------------------
echo "${BLUE}Step 12: Installing Bootstrap...${NC}"

rm -f /var/www/a/bootstrap.min.css 2>/dev/null
rm -f /var/www/a/bootstrap.bundle.min.js 2>/dev/null

if command -v curl >/dev/null 2>&1; then
    curl -s -o /var/www/a/bootstrap.min.css "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    curl -s -o /var/www/a/bootstrap.bundle.min.js "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
else
    wget -q -O /var/www/a/bootstrap.min.css "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    wget -q -O /var/www/a/bootstrap.bundle.min.js "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
fi

if [ -f /var/www/a/bootstrap.min.css ] && [ -s /var/www/a/bootstrap.min.css ]; then
    echo "${GREEN}  ✓ Bootstrap installed${NC}"
fi
echo ""

#-----------------------------------------------------------------------------
# Step 13: ЗАПУСК СЕРВИСОВ
#-----------------------------------------------------------------------------
echo "${BLUE}Step 13: Starting services...${NC}"

chmod 666 $UART_SELECTED 2>/dev/null
/etc/init.d/S99door restart

if [ -f /etc/baresip/accounts ] && [ -s /etc/baresip/accounts ]; then
    if command -v baresip >/dev/null 2>&1; then
        killall baresip 2>/dev/null
        baresip -f /etc/baresip -d > /dev/null 2>&1 &
        echo "${GREEN}  ✓ SIP service started${NC}"
    fi
fi

if [ -f /etc/mqtt.conf ]; then
    . /etc/mqtt.conf
    if [ "$MQTT_ENABLED" = "true" ]; then
        /usr/bin/mqtt_client.sh monitor > /dev/null 2>&1 &
        echo "${GREEN}  ✓ MQTT client started${NC}"
    fi
fi

# Запускаем backup сервер
killall httpd 2>/dev/null
httpd -p 8080 -h /var/www &
echo "${GREEN}  ✓ Backup server started on port 8080${NC}"
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
echo "${BLUE}📁 Backup of old files:${NC} $BACKUP_DIR"
echo ""
echo "${BLUE}🔑 Test keys:${NC}"
echo "  - 12345678 (Admin)"
echo "  - qrdemo (QR Test)"
echo "  - 0000 (Master)"
echo ""
echo "${BLUE}📋 Commands:${NC}"
echo "  Check status:  ${YELLOW}ps | grep -E 'door_monitor|mqtt|httpd'${NC}"
echo "  View logs:     ${YELLOW}tail -f /var/log/door_monitor.log${NC}"
echo "                 ${YELLOW}tail -f /var/log/mqtt.log${NC}"
echo "  Add key:       ${YELLOW}echo \"key|name|date\" >> /etc/door_keys.conf${NC}"
echo "  Restart:       ${YELLOW}/etc/init.d/S99door restart${NC}"
echo "  Restore backup:${YELLOW} cp -r $BACKUP_DIR/* /${NC}"
echo ""
echo "${GREEN}==========================================${NC}"
echo "${GREEN}Enjoy your OpenIPC Doorphone!${NC}"
echo "${GREEN}==========================================${NC}"
