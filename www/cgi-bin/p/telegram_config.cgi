#!/bin/sh
echo "Content-type: application/json"
echo ""

# Читаем конфиг Telegram
CONFIG_FILE="/etc/webui/telegram.conf"
TOKEN=""
CHAT_ID=""

if [ -f "$CONFIG_FILE" ]; then
    while read line; do
        case "$line" in
            telegram_token=*) TOKEN=$(echo "$line" | cut -d'"' -f2) ;;
            telegram_channel=*) CHAT_ID=$(echo "$line" | cut -d'"' -f2) ;;
        esac
    done < "$CONFIG_FILE"
fi

echo "{\"token\":\"$TOKEN\",\"chat_id\":\"$CHAT_ID\"}"
