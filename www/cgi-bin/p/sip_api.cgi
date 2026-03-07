#!/bin/sh
echo "Content-type: application/json"
echo ""

# Функция для декодирования URL
urldecode() {
    echo -e "$(echo "$1" | sed 's/+/ /g;s/%/\\x/g')"
}

# Функция логирования
log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - SIP - $1" >> /var/log/sip_monitor.log
}

# Функция для записи звонка
record_call() {
    direction="$1"
    number="$2"
    status="$3"
    duration="$4"
    
    RECORD_DIR="/mnt/mmcblk0p1/call_history"
    mkdir -p "$RECORD_DIR"
    
    DATE=$(date '+%Y-%m-%d %H:%M:%S')
    echo "$DATE|$direction|$number|$status|$duration" >> "$RECORD_DIR/calls.log"
}

# Получаем действие
action=$(echo "$QUERY_STRING" | sed -n 's/.*action=\([^&]*\).*/\1/p')

case "$action" in
    "get_sip_status")
        if pgrep -f "baresip" > /dev/null; then
            echo '{"status": "running"}'
        else
            echo '{"status": "stopped"}'
        fi
        ;;
        
    "save_sip_get")
        user=$(echo "$QUERY_STRING" | sed -n 's/.*user=\([^&]*\).*/\1/p')
        server=$(echo "$QUERY_STRING" | sed -n 's/.*server=\([^&]*\).*/\1/p')
        pass=$(echo "$QUERY_STRING" | sed -n 's/.*pass=\([^&]*\).*/\1/p')
        transport=$(echo "$QUERY_STRING" | sed -n 's/.*transport=\([^&]*\).*/\1/p')
        auto=$(echo "$QUERY_STRING" | sed -n 's/.*auto=\([^&]*\).*/\1/p')
        
        if [ -n "$user" ] && [ -n "$server" ] && [ -n "$pass" ]; then
            # Декодируем параметры
            user=$(urldecode "$user")
            server=$(urldecode "$server")
            pass=$(urldecode "$pass")
            [ -z "$transport" ] && transport="udp"
            
            # Формируем аккаунт
            if [ "$auto" = "true" ]; then
                ACCOUNT="<sip:$user@$server;transport=$transport>;auth_pass=$pass;answermode=auto;regint=60"
            else
                ACCOUNT="<sip:$user@$server;transport=$transport>;auth_pass=$pass;regint=60"
            fi
            
            # Сохраняем аккаунт
            mkdir -p /etc/baresip
            echo "# SIP account configured via web interface" > /etc/baresip/accounts
            echo "$ACCOUNT" >> /etc/baresip/accounts
            
            # Перезапускаем baresip
            killall baresip 2>/dev/null
            sleep 1
            if [ -f /usr/bin/baresip ]; then
                /usr/bin/baresip -f /etc/baresip -d > /dev/null 2>&1 &
            fi
            
            log_event "SIP account saved: $user@$server"
            echo '{"status": "success", "message": "SIP настройки сохранены"}'
        else
            echo '{"status": "error", "message": "Не все поля заполнены"}'
        fi
        ;;
        
    "save_call_number")
        number=$(echo "$QUERY_STRING" | sed -n 's/.*number=\([^&]*\).*/\1/p')
        if [ -n "$number" ]; then
            number=$(urldecode "$number")
            echo "$number" > /etc/baresip/call_number
            log_event "Call number saved: $number"
            echo "{\"status\": \"success\", \"message\": \"Номер сохранен\"}"
        else
            echo "{\"status\": \"error\", \"message\": \"Нет номера\"}"
        fi
        ;;
        
    "restart_sip")
        killall baresip 2>/dev/null
        sleep 1
        if [ -f /usr/bin/baresip ]; then
            /usr/bin/baresip -f /etc/baresip -d > /dev/null 2>&1 &
        fi
        log_event "SIP restarted"
        echo '{"status": "success", "message": "SIP перезапущен"}'
        ;;
        
    "get_call_history")
        lines=$(echo "$QUERY_STRING" | sed -n 's/.*lines=\([0-9]*\).*/\1/p')
        [ -z "$lines" ] && lines=20
        
        HISTORY_FILE="/mnt/mmcblk0p1/call_history/calls.log"
        
        echo -n '{"calls": ['
        
        if [ -f "$HISTORY_FILE" ]; then
            first=true
            tail -n $lines "$HISTORY_FILE" | while IFS='|' read datetime direction number status duration; do
                if [ -n "$datetime" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    
                    # Экранируем JSON
                    datetime=$(echo "$datetime" | sed 's/\\/\\\\/g; s/"/\\"/g')
                    number=$(echo "$number" | sed 's/\\/\\\\/g; s/"/\\"/g')
                    
                    echo -n "{\"time\":\"$datetime\",\"direction\":\"$direction\",\"number\":\"$number\",\"status\":\"$status\",\"duration\":\"$duration\"}"
                fi
            done
        fi
        
        echo ']}'
        ;;
        
    "list_recordings")
        RECORD_DIR="/mnt/mmcblk0p1/recordings"
        
        echo -n '{"recordings": ['
        
        if [ -d "$RECORD_DIR" ]; then
            first=true
            ls -t "$RECORD_DIR"/*.wav 2>/dev/null | while read file; do
                if [ -f "$file" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    
                    filename=$(basename "$file")
                    filesize=$(du -h "$file" | cut -f1)
                    filedate=$(date -r "$file" '+%Y-%m-%d %H:%M:%S')
                    
                    echo -n "{\"name\":\"$filename\",\"size\":\"$filesize\",\"date\":\"$filedate\"}"
                fi
            done
        fi
        
        echo ']}'
        ;;
        
    "clear_recordings")
        RECORD_DIR="/mnt/mmcblk0p1/recordings"
        
        if [ -d "$RECORD_DIR" ]; then
            rm -f "$RECORD_DIR"/*.wav
            log_event "All recordings cleared"
            echo '{"status": "success", "message": "Все записи удалены"}'
        else
            echo '{"status": "error", "message": "Директория записей не найдена"}'
        fi
        ;;
        
    "enable_recording")
        enabled=$(echo "$QUERY_STRING" | sed -n 's/.*enabled=\([^&]*\).*/\1/p')
        
        CONFIG_FILE="/etc/baresip/config"
        
        if [ "$enabled" = "true" ]; then
            # Включаем запись
            if ! grep -q "^module[[:space:]]*record" "$CONFIG_FILE" 2>/dev/null; then
                echo "module record.so" >> "$CONFIG_FILE"
            fi
            log_event "Call recording enabled"
            echo '{"status": "success", "message": "Запись звонков включена"}'
        else
            # Отключаем запись
            if [ -f "$CONFIG_FILE" ]; then
                sed -i '/^module[[:space:]]*record/d' "$CONFIG_FILE"
            fi
            log_event "Call recording disabled"
            echo '{"status": "success", "message": "Запись звонков отключена"}'
        fi
        ;;
        
    "send_dtmf")
        digit=$(echo "$QUERY_STRING" | sed -n 's/.*digit=\([^&]*\).*/\1/p')
        
        if [ -n "$digit" ]; then
            digit=$(urldecode "$digit")
            # Отправляем DTMF через baresip
            echo "/dtmf $digit" | nc 127.0.0.1 3000 2>/dev/null
            log_event "DTMF sent: $digit"
            echo '{"status": "success", "message": "DTMF отправлен"}'
        else
            echo '{"status": "error", "message": "Не указан DTMF сигнал"}'
        fi
        ;;
        
    "make_call")
        number=$(echo "$QUERY_STRING" | sed -n 's/.*number=\([^&]*\).*/\1/p')
        
        if [ -n "$number" ]; then
            number=$(urldecode "$number")
            echo "/dial $number" | nc 127.0.0.1 3000 2>/dev/null
            log_event "Call initiated to $number"
            
            # Записываем в историю
            record_call "outgoing" "$number" "initiated" ""
            
            echo '{"status": "success", "message": "Звонок инициирован"}'
        else
            echo '{"status": "error", "message": "Не указан номер"}'
        fi
        ;;
        
    "hangup")
        echo "/hangup" | nc 127.0.0.1 3000 2>/dev/null
        log_event "Call terminated"
        echo '{"status": "success", "message": "Звонок завершен"}'
        ;;
        
    *)
        echo "{\"status\": \"error\", \"message\": \"Неизвестное действие: $action\"}"
        ;;
esac