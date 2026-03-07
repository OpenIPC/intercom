#!/bin/sh
echo "Content-type: application/json; charset=utf-8"
echo ""

#===============================================================================
# OpenIPC Doorphone API
#===============================================================================

# Функции для работы с URL и JSON
urldecode() {
    echo -e "$(echo "$1" | sed 's/+/ /g;s/%/\\x/g')"
}

json_escape() {
    echo "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

# Функция логирования
log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> /var/log/door_monitor.log
}

# Функция для получения размера файла
get_file_size() {
    if [ -f "$1" ]; then
        stat -c%s "$1" 2>/dev/null || stat -f%z "$1" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Функция для форматирования размера
format_size() {
    size=$1
    if [ $size -lt 1024 ]; then
        echo "${size}B"
    elif [ $size -lt 1048576 ]; then
        echo "$((size / 1024))KB"
    else
        echo "$((size / 1048576))MB"
    fi
}

# Получаем действие из QUERY_STRING
action=$(echo "$QUERY_STRING" | sed -n 's/.*action=\([^&]*\).*/\1/p')

# Если это POST запрос, читаем данные
if [ "$REQUEST_METHOD" = "POST" ]; then
    read POST_STRING
    key=$(echo "$POST_STRING" | sed -n 's/.*key=\([^&]*\).*/\1/p')
    owner=$(echo "$POST_STRING" | sed -n 's/.*owner=\([^&]*\).*/\1/p')
    expiry=$(echo "$POST_STRING" | sed -n 's/.*expiry=\([^&]*\).*/\1/p')
    
    if [ -n "$key" ]; then
        key=$(urldecode "$key")
    fi
    if [ -n "$owner" ]; then
        owner=$(urldecode "$owner")
    fi
fi

case "$action" in
    #===========================================================================
    # Управление ключами
    #===========================================================================
    "list_keys")
        echo -n '{"keys": ['
        if [ -f /etc/door_keys.conf ]; then
            first=true
            cat /etc/door_keys.conf | while IFS='|' read k o d e; do
                if [ -n "$k" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    k=$(json_escape "$k")
                    o=$(json_escape "$o")
                    d=$(json_escape "$d")
                    e=$(json_escape "$e")
                    echo -n "{\"key\":\"$k\",\"owner\":\"$o\",\"date\":\"$d\",\"expiry\":\"$e\"}"
                fi
            done
        fi
        echo ']}'
        ;;
        
    "add_key")
        if [ -n "$key" ]; then
            if [ -z "$owner" ]; then
                owner="Unknown"
            fi
            
            # Проверяем, существует ли уже такой ключ
            if grep -q "^$key|" /etc/door_keys.conf 2>/dev/null; then
                echo '{"status": "error", "message": "Ключ уже существует"}'
            else
                # Формируем строку ключа
                if [ -n "$expiry" ]; then
                    # Временный ключ с датой истечения
                    echo "$key|$owner|$(date '+%Y-%m-%d')|$expiry" >> /etc/door_keys.conf
                    log_event "TEMP_KEY_ADDED - Временный ключ $key для $owner добавлен, истекает: $(date -d @$expiry '+%Y-%m-%d %H:%M:%S')"
                    echo '{"status": "success", "message": "Временный ключ добавлен"}'
                else
                    # Постоянный ключ
                    echo "$key|$owner|$(date '+%Y-%m-%d')" >> /etc/door_keys.conf
                    log_event "KEY_ADDED - Ключ $key для $owner добавлен"
                    echo '{"status": "success", "message": "Ключ добавлен"}'
                fi
            fi
        else
            echo '{"status": "error", "message": "Не указан ключ"}'
        fi
        ;;
        
    "remove_key")
        if [ -n "$key" ] && [ -f /etc/door_keys.conf ]; then
            # Проверяем, существует ли ключ
            if grep -q "^$key|" /etc/door_keys.conf 2>/dev/null; then
                # Получаем информацию о ключе для лога
                key_info=$(grep "^$key|" /etc/door_keys.conf | head -1)
                owner=$(echo "$key_info" | cut -d'|' -f2)
                
                # Удаляем ключ
                grep -v "^$key|" /etc/door_keys.conf > /tmp/keys.tmp
                mv /tmp/keys.tmp /etc/door_keys.conf
                log_event "KEY_REMOVED - Ключ $key ($owner) удален"
                echo '{"status": "success", "message": "Ключ удален"}'
            else
                echo '{"status": "error", "message": "Ключ не найден"}'
            fi
        else
            echo '{"status": "error", "message": "Не указан ключ"}'
        fi
        ;;
        
    "get_temp_keys")
        echo -n '{"keys": ['
        if [ -f /etc/door_keys.conf ]; then
            first=true
            current_time=$(date +%s)
            cat /etc/door_keys.conf | while IFS='|' read k o d e; do
                # Проверяем, есть ли expiry (4-е поле) и оно числовое
                if [ -n "$e" ] && [ "$e" -eq "$e" ] 2>/dev/null; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    k=$(json_escape "$k")
                    o=$(json_escape "$o")
                    d=$(json_escape "$d")
                    e=$(json_escape "$e")
                    
                    # Определяем статус
                    status="active"
                    if [ "$e" -lt "$current_time" ]; then
                        status="expired"
                    fi
                    
                    echo -n "{\"key\":\"$k\",\"owner\":\"$o\",\"date\":\"$d\",\"expiry\":$e,\"status\":\"$status\"}"
                fi
            done
        fi
        echo ']}'
        ;;
        
    "clean_temp_keys")
        if [ ! -f /etc/door_keys.conf ]; then
            echo '{"status": "error", "message": "Файл ключей не найден"}'
            exit 0
        fi
        
        current_time=$(date +%s)
        TEMP_FILE="/tmp/keys_clean.tmp"
        REMOVED=0
        KEPT=0
        
        while IFS='|' read k o d e; do
            if [ -n "$e" ] && [ "$e" -eq "$e" ] 2>/dev/null; then
                # Это временный ключ
                if [ "$e" -lt "$current_time" ]; then
                    # Истек - пропускаем (не сохраняем)
                    REMOVED=$((REMOVED + 1))
                    log_event "TEMP_KEY_EXPIRED - Автоматически удален истекший ключ $k ($o)"
                else
                    # Еще действует - сохраняем
                    echo "$k|$o|$d|$e" >> "$TEMP_FILE"
                    KEPT=$((KEPT + 1))
                fi
            else
                # Постоянный ключ - сохраняем
                echo "$k|$o|$d|$e" >> "$TEMP_FILE"
                KEPT=$((KEPT + 1))
            fi
        done < /etc/door_keys.conf
        
        mv "$TEMP_FILE" /etc/door_keys.conf
        chmod 666 /etc/door_keys.conf
        
        echo "{\"status\": \"success\", \"message\": \"Очистка завершена\", \"removed\": $REMOVED, \"kept\": $KEPT}"
        ;;
        
    "get_stats")
        total_keys=0
        perm_keys=0
        temp_keys=0
        expired_temp=0
        current_time=$(date +%s)
        
        if [ -f /etc/door_keys.conf ]; then
            while IFS='|' read k o d e; do
                if [ -n "$k" ]; then
                    total_keys=$((total_keys + 1))
                    if [ -n "$e" ] && [ "$e" -eq "$e" ] 2>/dev/null; then
                        temp_keys=$((temp_keys + 1))
                        if [ "$e" -lt "$current_time" ]; then
                            expired_temp=$((expired_temp + 1))
                        fi
                    else
                        perm_keys=$((perm_keys + 1))
                    fi
                fi
            done < /etc/door_keys.conf
        fi
        
        echo "{\"status\": \"success\", \"total\": $total_keys, \"permanent\": $perm_keys, \"temporary\": $temp_keys, \"expired\": $expired_temp}"
        ;;
        
    #===========================================================================
    # Управление дверью и ESP
    #===========================================================================
    "get_status")
        esp_status="disconnected"
        if [ -c /dev/ttyS0 ] || [ -c /dev/ttyAMA0 ]; then
            if pgrep -f "door_monitor" > /dev/null; then
                esp_status="connected"
            else
                esp_status="detected"
            fi
        fi
        
        keys_count=$(cat /etc/door_keys.conf 2>/dev/null | wc -l)
        temp_keys=$(grep -c "|.*|.*|[0-9]" /etc/door_keys.conf 2>/dev/null || echo "0")
        
        echo "{\"esp\": \"$esp_status\", \"keys\": $keys_count, \"temp_keys\": $temp_keys}"
        ;;
        
    "open_door")
        if [ -c /dev/ttyS0 ]; then
            echo "OPEN" > /dev/ttyS0 2>/dev/null
            log_event "MANUAL_OPEN - Дверь открыта вручную (ttyS0)"
            echo '{"status": "success", "message": "Дверь открыта"}'
        elif [ -c /dev/ttyAMA0 ]; then
            echo "OPEN" > /dev/ttyAMA0 2>/dev/null
            log_event "MANUAL_OPEN - Дверь открыта вручную (ttyAMA0)"
            echo '{"status": "success", "message": "Дверь открыта"}'
        else
            echo '{"status": "error", "message": "ESP не подключен"}'
        fi
        ;;
        
    "control_door")
        cmd=$(echo "$QUERY_STRING" | sed -n 's/.*cmd=\([^&]*\).*/\1/p')
        
        if [ "$cmd" = "open" ]; then
            if [ -c /dev/ttyS0 ]; then
                echo "OPEN" > /dev/ttyS0 2>/dev/null
                log_event "DOOR_OPEN - Дверь открыта через веб-интерфейс"
                echo '{"status": "success", "message": "Дверь открыта"}'
            elif [ -c /dev/ttyAMA0 ]; then
                echo "OPEN" > /dev/ttyAMA0 2>/dev/null
                log_event "DOOR_OPEN - Дверь открыта через веб-интерфейс"
                echo '{"status": "success", "message": "Дверь открыта"}'
            else
                echo '{"status": "error", "message": "ESP не подключен"}'
            fi
        elif [ "$cmd" = "close" ]; then
            if [ -c /dev/ttyS0 ]; then
                echo "CLOSE" > /dev/ttyS0 2>/dev/null
                log_event "DOOR_CLOSE - Дверь закрыта через веб-интерфейс"
                echo '{"status": "success", "message": "Дверь закрыта"}'
            elif [ -c /dev/ttyAMA0 ]; then
                echo "CLOSE" > /dev/ttyAMA0 2>/dev/null
                log_event "DOOR_CLOSE - Дверь закрыта через веб-интерфейс"
                echo '{"status": "success", "message": "Дверь закрыта"}'
            else
                echo '{"status": "error", "message": "ESP не подключен"}'
            fi
        else
            echo '{"status": "error", "message": "Неизвестная команда"}'
        fi
        ;;
        
    "get_door_status")
        door_status="unknown"
        relay_status="unknown"
        last_change=""
        
        if [ -c /dev/ttyS0 ] || [ -c /dev/ttyAMA0 ]; then
            if pgrep -f "door_monitor" > /dev/null; then
                if [ -f /var/log/door_monitor.log ]; then
                    last_door_event=$(grep "DOOR:" /var/log/door_monitor.log | tail -1)
                    if echo "$last_door_event" | grep -q "OPEN"; then
                        door_status="open"
                    elif echo "$last_door_event" | grep -q "CLOSED"; then
                        door_status="closed"
                    fi
                    last_change=$(echo "$last_door_event" | cut -d' ' -f1-2)
                fi
            fi
        fi
        
        esp_status="disconnected"
        if [ -c /dev/ttyS0 ] || [ -c /dev/ttyAMA0 ]; then
            if pgrep -f "door_monitor" > /dev/null; then
                esp_status="connected"
            else
                esp_status="detected"
            fi
        fi
        
        echo "{\"status\":\"success\",\"door\":\"$door_status\",\"relay\":\"$relay_status\",\"esp\":\"$esp_status\",\"last_change\":\"$last_change\"}"
        ;;
        
    "get_door_history")
        lines=$(echo "$QUERY_STRING" | sed -n 's/.*lines=\([0-9]*\).*/\1/p')
        [ -z "$lines" ] && lines=10
        
        echo -n '{"events": ['
        if [ -f /var/log/door_monitor.log ]; then
            first=true
            grep -E "DOOR:|OPEN|CLOSED" /var/log/door_monitor.log | tail -n $lines | while read line; do
                if [ -n "$line" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    time=$(echo "$line" | cut -d' ' -f1-2)
                    action=$(echo "$line" | grep -oE "DOOR: OPEN|DOOR: CLOSED|OPEN|CLOSED" | head -1)
                    result="success"
                    if echo "$line" | grep -q "DENIED"; then
                        result="denied"
                    fi
                    time=$(json_escape "$time")
                    action=$(json_escape "$action")
                    echo -n "{\"time\":\"$time\",\"action\":\"$action\",\"result\":\"$result\"}"
                fi
            done
        fi
        echo ']}'
        ;;
        
    "get_door_stats")
        today=$(date '+%Y-%m-%d')
        open_today=0
        
        if [ -f /var/log/door_monitor.log ]; then
            open_today=$(grep "$today" /var/log/door_monitor.log | grep -c "OPEN")
        fi
        
        echo "{\"status\":\"success\",\"open_today\":$open_today}"
        ;;
        
    #===========================================================================
    # История и логи
    #===========================================================================
    "get_history")
        lines=$(echo "$QUERY_STRING" | sed -n 's/.*lines=\([0-9]*\).*/\1/p')
        [ -z "$lines" ] && lines=100
        
        echo -n '{"events": ['
        if [ -f /var/log/door_monitor.log ]; then
            first=true
            tail -n $lines /var/log/door_monitor.log | while read line; do
                if [ -n "$line" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    line=$(json_escape "$line")
                    echo -n "{\"msg\":\"$line\"}"
                fi
            done
        fi
        echo ']}'
        ;;
        
    "clear_history")
        LOG_FILE="/var/log/door_monitor.log"
        BACKUP_FILE="/var/log/door_monitor.log.bak"
        
        if [ -f "$LOG_FILE" ]; then
            cp "$LOG_FILE" "$BACKUP_FILE" 2>/dev/null
            > "$LOG_FILE"
            log_event "HISTORY_CLEARED - История очищена (резервная копия: door_monitor.log.bak)"
            echo '{"status": "success", "message": "История очищена"}'
        else
            echo '{"status": "error", "message": "Файл лога не найден"}'
        fi
        ;;
        
    "log_info")
        LOG_FILE="/var/log/door_monitor.log"
        if [ -f "$LOG_FILE" ]; then
            SIZE=$(get_file_size "$LOG_FILE")
            SIZE_HUMAN=$(format_size $SIZE)
            LINES=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
            FIRST_LINE=$(head -1 "$LOG_FILE" 2>/dev/null | cut -c1-100)
            LAST_MODIFIED=$(date -r "$LOG_FILE" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "unknown")
            
            FIRST_LINE=$(json_escape "$FIRST_LINE")
            
            echo "{\"status\": \"success\", \"size_bytes\": $SIZE, \"size\": \"$SIZE_HUMAN\", \"lines\": $LINES, \"first\": \"$FIRST_LINE\", \"modified\": \"$LAST_MODIFIED\"}"
        else
            echo '{"status": "error", "message": "Файл лога не найден"}'
        fi
        ;;
        
    #===========================================================================
    # SIP интеграция
    #===========================================================================
    "make_call")
        number=$(echo "$QUERY_STRING" | sed -n 's/.*number=\([^&]*\).*/\1/p')
        
        if [ -n "$number" ]; then
            number=$(urldecode "$number")
            echo "/dial $number" | nc 127.0.0.1 3000 2>/dev/null
            log_event "CALL_MADE - Вызов на номер $number"
            echo '{"status": "success", "message": "Звонок инициирован"}'
        else
            echo '{"status": "error", "message": "Не указан номер"}'
        fi
        ;;
        
    "get_call_history")
        CALL_LOG="/mnt/mmcblk0p1/call_history/calls.log"
        lines=$(echo "$QUERY_STRING" | sed -n 's/.*lines=\([0-9]*\).*/\1/p')
        [ -z "$lines" ] && lines=20
        
        echo -n '{"calls": ['
        
        if [ -f "$CALL_LOG" ]; then
            first=true
            tail -n $lines "$CALL_LOG" 2>/dev/null | while IFS='|' read datetime direction number status duration; do
                if [ -n "$datetime" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    
                    datetime=$(json_escape "$datetime")
                    number=$(json_escape "$number")
                    
                    echo -n "{\"time\":\"$datetime\",\"direction\":\"$direction\",\"number\":\"$number\",\"status\":\"$status\",\"duration\":\"$duration\"}"
                fi
            done
        fi
        
        echo ']}'
        ;;
        
    #===========================================================================
    # Неизвестное действие
    #===========================================================================
    *)
        echo '{"status": "error", "message": "Неизвестное действие"}'
        ;;
esac