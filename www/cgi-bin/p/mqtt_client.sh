#!/bin/sh
#===============================================================================
# OpenIPC Doorphone MQTT Client
#===============================================================================

MQTT_CONFIG="/etc/mqtt.conf"
MQTT_LOG="/var/log/mqtt.log"
MQTT_PID="/var/run/mqtt_client.pid"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$MQTT_LOG"
}

# Загрузка конфигурации
if [ -f "$MQTT_CONFIG" ]; then
    . "$MQTT_CONFIG"
else
    log "ERROR: MQTT configuration not found"
    exit 1
fi

if [ "$MQTT_ENABLED" != "true" ]; then
    log "MQTT client is disabled"
    exit 0
fi

log "Starting MQTT client for OpenIPC Doorphone"
log "Broker: $MQTT_HOST:$MQTT_PORT"
log "Client ID: $MQTT_CLIENT_ID"
log "Topic prefix: $MQTT_TOPIC_PREFIX"

# Отправка статуса онлайн
/usr/bin/mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
    ${MQTT_USER:+-u "$MQTT_USER"} ${MQTT_PASS:+-P "$MQTT_PASS"} \
    -i "$MQTT_CLIENT_ID" \
    -t "$MQTT_TOPIC_PREFIX/status" \
    -m "online" \
    -r

# Если включен Discovery, отправляем конфигурацию
if [ "$MQTT_DISCOVERY" = "true" ]; then
    # Здесь можно вызвать send_discovery из API
    log "Sending Home Assistant Discovery configuration"
fi

# Основной цикл обработки событий
# В реальном клиенте здесь должно быть подключение к FIFO или событиям от door_monitor

echo $$ > "$MQTT_PID"

# Функция отправки сообщения
publish() {
    topic="$1"
    message="$2"
    /usr/bin/mosquitto_pub -h "$MQTT_HOST" -p "$MQTT_PORT" \
        ${MQTT_USER:+-u "$MQTT_USER"} ${MQTT_PASS:+-P "$MQTT_PASS"} \
        -i "$MQTT_CLIENT_ID" \
        -t "$MQTT_TOPIC_PREFIX/$topic" \
        -m "$message"
    log "Published to $MQTT_TOPIC_PREFIX/$topic: $message"
}

# Обработка сигналов
trap "publish status 'offline'; log 'MQTT client stopped'; rm -f $MQTT_PID; exit 0" INT TERM

# Отправка статуса оффлайн при выходе
publish status "offline"

exit 0