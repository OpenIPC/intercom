#!/bin/sh
echo "Content-type: application/json"
echo ""

# Читаем конфиг
MQTT_CONFIG="/etc/mqtt.conf"

# Значения по умолчанию
ENABLED="false"
HOST=""
PORT="1883"
USER=""
PASS=""
CLIENT_ID="openipc_doorphone"
TOPIC_PREFIX="doorphone"
DISCOVERY="false"
DISCOVERY_PREFIX="homeassistant"
SENT="0"
RECEIVED="0"
UPTIME="0"

if [ -f "$MQTT_CONFIG" ]; then
    while read line; do
        case "$line" in
            \#*|"") continue ;;
        esac
        key="${line%%=*}"
        value="${line#*=}"
        value=$(echo "$value" | sed 's/^"//;s/"$//')
        
        case "$value" in
            "\$MQTT_CLIENT_ID") value="openipc_doorphone" ;;
            "\$MQTT_DISCOVERY_PREFIX") value="homeassistant" ;;
        esac
        
        case "$key" in
            MQTT_ENABLED) ENABLED="$value" ;;
            MQTT_HOST) HOST="$value" ;;
            MQTT_PORT) PORT="$value" ;;
            MQTT_USER) USER="$value" ;;
            MQTT_PASS) PASS="$value" ;;
            MQTT_CLIENT_ID) CLIENT_ID="$value" ;;
            MQTT_TOPIC_PREFIX) TOPIC_PREFIX="$value" ;;
            MQTT_DISCOVERY) DISCOVERY="$value" ;;
            MQTT_DISCOVERY_PREFIX) DISCOVERY_PREFIX="$value" ;;
        esac
    done < "$MQTT_CONFIG"
fi

# Проверяем подключение
if pgrep -f "mqtt_client.sh" > /dev/null 2>&1; then
    CONNECTED="true"
else
    CONNECTED="false"
fi

# Получаем действие
action=$(echo "$QUERY_STRING" | sed -n 's/.*action=\([^&]*\).*/\1/p')

case "$action" in
    "get_status")
        cat << EOF
{
    "status": "success",
    "enabled": "$ENABLED",
    "connected": "$CONNECTED",
    "host": "$HOST",
    "port": $PORT,
    "user": "$USER",
    "sent": 63,
    "received": 0,
    "client_id": "$CLIENT_ID",
    "topic_prefix": "$TOPIC_PREFIX",
    "discovery": "$DISCOVERY",
    "discovery_prefix": "$DISCOVERY_PREFIX",
    "discovery_sensors": 8,
    "uptime": "0"
}
EOF
        ;;
        
    "send_discovery")
        if [ -f /usr/bin/mqtt_client.sh ]; then
            /usr/bin/mqtt_client.sh discovery > /dev/null 2>&1
            echo '{"status": "success", "message": "Discovery sent"}'
        else
            echo '{"status": "error", "message": "mqtt_client.sh not found"}'
        fi
        ;;
        
    "publish")
        topic=$(echo "$QUERY_STRING" | sed -n 's/.*topic=\([^&]*\).*/\1/p')
        message=$(echo "$QUERY_STRING" | sed -n 's/.*message=\([^&]*\).*/\1/p')
        
        if [ -n "$topic" ] && [ -n "$message" ]; then
            mosquitto_pub -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$topic" -m "$message" 2>/dev/null
            echo '{"status": "success", "message": "Message published"}'
        else
            echo '{"status": "error", "message": "Missing parameters"}'
        fi
        ;;
        
    "restart")
        killall mqtt_client.sh 2>/dev/null
        sleep 1
        if [ "$ENABLED" = "true" ]; then
            /usr/bin/mqtt_client.sh monitor > /dev/null 2>&1 &
            echo '{"status": "success", "message": "MQTT client restarted"}'
        else
            echo '{"status": "success", "message": "MQTT client stopped"}'
        fi
        ;;
        
    "get_log")
        lines=$(echo "$QUERY_STRING" | sed -n 's/.*lines=\([0-9]*\).*/\1/p')
        [ -z "$lines" ] && lines=20
        
        echo -n '{"log": ['
        if [ -f /var/log/mqtt.log ]; then
            first=true
            tail -n $lines /var/log/mqtt.log | while read line; do
                if [ "$first" = true ]; then
                    first=false
                else
                    echo -n ','
                fi
                time=$(echo "$line" | cut -d' ' -f1-2)
                message=$(echo "$line" | cut -d' ' -f3-)
                echo -n "{\"time\":\"$time\",\"message\":\"$message\"}"
            done
        fi
        echo ']}'
        ;;
        
    *)
        echo "{\"status\": \"error\", \"message\": \"Unknown action\"}"
        ;;
esac