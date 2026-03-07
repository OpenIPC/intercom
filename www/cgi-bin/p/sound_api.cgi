#!/bin/sh
echo "Content-type: application/json"
echo ""

# Функция логирования
log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - SOUND - $1" >> /var/log/door_monitor.log
}

# Декодирование URL
urldecode() {
    echo -e "$(echo "$1" | sed 's/+/ /g;s/%/\\x/g')"
}

# Получаем действие
action=$(echo "$QUERY_STRING" | sed -n 's/.*action=\([^&]*\).*/\1/p')

case "$action" in
    "list_sounds")
        SOUND_DIR="/usr/share/sounds/doorphone"
        
        echo -n '{"sounds": ['
        
        if [ -d "$SOUND_DIR" ]; then
            first=true
            for file in "$SOUND_DIR"/*.pcm; do
                if [ -f "$file" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    
                    filename=$(basename "$file")
                    filesize=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
                    
                    # Человеческое имя
                    display_name=$(echo "$filename" | sed 's/\.pcm$//' | tr '_' ' ')
                    
                    echo -n "{\"name\":\"$filename\",\"size\":$filesize,\"displayName\":\"$display_name\"}"
                fi
            done
        fi
        
        echo ']}'
        ;;
        
    "delete_sound")
        name=$(echo "$QUERY_STRING" | sed -n 's/.*name=\([^&]*\).*/\1/p')
        name=$(urldecode "$name")
        
        SOUND_FILE="/usr/share/sounds/doorphone/$name"
        
        # Запрещаем удалять стандартные звуки
        if echo "$name" | grep -qE '^(ring|door_open|door_close|denied|beep)\.pcm$'; then
            echo '{"status": "error", "message": "Нельзя удалить стандартный звук"}'
            exit 0
        fi
        
        if [ -f "$SOUND_FILE" ]; then
            rm -f "$SOUND_FILE"
            log_event "Sound deleted: $name"
            echo '{"status": "success", "message": "Звук удален"}'
        else
            echo '{"status": "error", "message": "Файл не найден"}'
        fi
        ;;
        
    *)
        echo '{"status": "error", "message": "Unknown action"}'
        ;;
esac
