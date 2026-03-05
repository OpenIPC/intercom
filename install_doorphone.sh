#!/bin/sh
#===============================================================================
# OpenIPC Doorphone Installer
#===============================================================================

echo "=========================================="
echo "OpenIPC Doorphone Installer v2.0"
echo "=========================================="
echo ""

# Проверка прав
if [ "$(id -u)" != "0" ]; then
    echo "ERROR: This script must be run as root"
    exit 1
fi

echo "Step 1: Detecting UART ports..."
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
    echo "ERROR: No UART ports found!"
    exit 1
fi

echo "Selected UART: $UART_SELECTED"
echo ""

echo "Step 2: Creating directories..."
mkdir -p /var/www/cgi-bin/p
mkdir -p /var/www/a
mkdir -p /usr/share/sounds/doorphone
mkdir -p /root/backups
mkdir -p /etc/baresip

echo "Step 3: Configuring UART..."
chmod 666 $UART_SELECTED
if ! grep -q "chmod 666 $UART_SELECTED" /etc/rc.local; then
    sed -i "/exit 0/i chmod 666 $UART_SELECTED" /etc/rc.local
fi

echo "Step 4: Downloading files..."
TEMP_DIR="/tmp/intercom_$$"
mkdir -p "$TEMP_DIR"

echo "  - Downloading from GitHub..."
wget -q -O "$TEMP_DIR/intercom.tar.gz" https://github.com/OpenIPC/intercom/archive/main.tar.gz

if [ $? -ne 0 ] || [ ! -s "$TEMP_DIR/intercom.tar.gz" ]; then
    echo "ERROR: Failed to download from GitHub"
    echo "Using minimal files instead..."
    
    # Создаем минимальный backup_manager.cgi
    cat > /var/www/cgi-bin/p/backup_manager.cgi << 'EOFC'
#!/bin/sh
echo "Content-type: text/html"
echo ""
echo "<html><body><h1>Installation incomplete</h1>"
echo "<p>Please download files manually from GitHub:</p>"
echo "<p>https://github.com/OpenIPC/intercom</p>"
echo "</body></html>"
EOFC
    chmod +x /var/www/cgi-bin/p/backup_manager.cgi
else
    echo "  - Extracting files..."
    tar -xzf "$TEMP_DIR/intercom.tar.gz" -C "$TEMP_DIR"
    
    if [ -d "$TEMP_DIR/intercom-main/cgi-bin" ]; then
        echo "  - Installing CGI scripts..."
        cp -r "$TEMP_DIR/intercom-main/cgi-bin/"* /var/www/cgi-bin/
        chmod +x /var/www/cgi-bin/p/*.cgi 2>/dev/null
        chmod +x /var/www/cgi-bin/backup.cgi 2>/dev/null
    fi
fi

echo "Step 5: Installing Bootstrap..."
wget -q -O /var/www/a/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
wget -q -O /var/www/a/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js

echo "Step 6: Creating door_monitor.sh..."
cat > /usr/bin/door_monitor.sh << 'EOF'
#!/bin/sh
# Door monitor script
UART_DEV="$UART_SELECTED"
KEYS_FILE="/etc/door_keys.conf"
LOG_FILE="/var/log/door_monitor.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

case "$1" in
    start)
        log "Door monitor starting on $UART_DEV"
        while true; do
            if [ -c "$UART_DEV" ]; then
                read line < "$UART_DEV" 2>/dev/null
                if [ -n "$line" ]; then
                    log "Received: $line"
                fi
            fi
            sleep 0.1
        done &
        echo $! > /var/run/door_monitor.pid
        ;;
    stop)
        kill $(cat /var/run/door_monitor.pid 2>/dev/null) 2>/dev/null
        rm -f /var/run/door_monitor.pid
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        ;;
esac
EOF
chmod +x /usr/bin/door_monitor.sh

echo "Step 7: Configuring autostart..."
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
    start-stop-daemon -K -p $PIDFILE
    rm -f $PIDFILE
    echo "OK"
}

case "$1" in
    start|stop) $1 ;;
    restart) stop; start ;;
    *) echo "Usage: $0 {start|stop|restart}"; exit 1 ;;
esac
exit 0
EOF
chmod +x /etc/init.d/S99door

echo "Step 8: Setting up backup server..."
if ! grep -q "httpd -p 8080" /etc/rc.local; then
    sed -i "/exit 0/i httpd -p 8080 -h /var/www \&" /etc/rc.local
fi

echo "Step 9: Creating keys database..."
touch /etc/door_keys.conf
chmod 666 /etc/door_keys.conf

echo "Step 10: Starting services..."
killall httpd 2>/dev/null
httpd -p 8080 -h /var/www &
/etc/init.d/S99door restart

echo "Step 11: Cleaning up..."
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""

# Получаем IP
IP=$(ip addr show | grep -o '192\.168\.[0-9]*\.[0-9]*' | head -1)
[ -z "$IP" ] && IP="192.168.1.4"

echo "📱 Main web interface: http://$IP"
echo "💾 Backup manager:     http://$IP:8080/cgi-bin/p/backup_manager.cgi"
echo "🔌 UART device:        $UART_SELECTED"
echo ""
echo "📝 Commands:"
echo "  View logs: tail -f /var/log/door_monitor.log"
echo "  Add key:   echo \"12345678|User|$(date +%Y-%m-%d)\" >> /etc/door_keys.conf"
echo ""
echo "=========================================="
