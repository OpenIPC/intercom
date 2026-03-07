#!/bin/sh
# DTMF handler for OpenIPC Doorphone

# Получаем параметры
digit=$(echo "$QUERY_STRING" | sed -n 's/.*digit=\([^&]*\).*/\1/p')
sequence=$(echo "$QUERY_STRING" | sed -n 's/.*sequence=\([^&]*\).*/\1/p')

# Функция логирования
log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - DTMF - $1" >> /var/log/sip_monitor.log
}

if [ -n "$digit" ]; then
    # Отправляем одиночный DTMF
    echo "/dtmf $digit" | nc 127.0.0.1 3000 2>/dev/null
    log_event "DTMF sent: $digit"
    echo "Content-type: text/plain"
    echo ""
    echo "DTMF $digit sent"
    
elif [ -n "$sequence" ]; then
    # Отправляем последовательность DTMF
    # Декодируем URL
    sequence=$(echo -e "$(echo "$sequence" | sed 's/+/ /g;s/%/\\x/g')")
    
    # Отправляем каждый символ с небольшой задержкой
    length=${#sequence}
    i=0
    while [ $i -lt $length ]; do
        char=$(echo "$sequence" | cut -c $((i+1)))
        echo "/dtmf $char" | nc 127.0.0.1 3000 2>/dev/null
        log_event "DTMF sent: $char"
        sleep 0.2
        i=$((i + 1))
    done
    
    echo "Content-type: text/plain"
    echo ""
    echo "DTMF sequence sent: $sequence"
    
else
    echo "Content-type: text/plain"
    echo ""
    echo "Usage: dtmf_9.sh?digit=X or dtmf_9.sh?sequence=123"
fi