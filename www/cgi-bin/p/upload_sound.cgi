#!/bin/sh
echo "Content-type: application/json"
echo ""

# Функция логирования
log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - UPLOAD - $1" >> /var/log/door_monitor.log
}

# Проверяем метод
if [ "$REQUEST_METHOD" != "POST" ]; then
    echo '{"status": "error", "message": "Method not allowed"}'
    exit 1
fi

# Директория для звуков
SOUND_DIR="/usr/share/sounds/doorphone"
mkdir -p "$SOUND_DIR"

# Сохраняем POST данные во временный файл
TEMP_FILE="/tmp/upload_sound_$$.tmp"
cat > "$TEMP_FILE"
BYTES=$(stat -c%s "$TEMP_FILE" 2>/dev/null)

if [ "$BYTES" -eq 0 ]; then
    echo '{"status": "error", "message": "Empty file"}'
    rm -f "$TEMP_FILE"
    exit 1
fi

# Проверяем размер (макс 1MB)
if [ "$BYTES" -gt 1048576 ]; then
    echo '{"status": "error", "message": "File too large (max 1MB)"}'
    rm -f "$TEMP_FILE"
    exit 1
fi

# Пытаемся извлечь имя файла из multipart
BOUNDARY=$(head -1 "$TEMP_FILE" | tr -d '\r\n')
FILENAME=""

if [ -n "$BOUNDARY" ] && [ ${#BOUNDARY} -gt 10 ]; then
    # Ищем имя файла
    FILENAME=$(grep -a "filename=" "$TEMP_FILE" | head -1 | sed -n 's/.*filename="\([^"]*\)".*/\1/p')
    
    if [ -n "$FILENAME" ]; then
        # Извлекаем содержимое файла
        awk -v boundary="$BOUNDARY" '
            BEGIN { in_file = 0; }
            $0 ~ boundary { 
                if (in_file) exit;
                in_file = 1; 
                next;
            }
            in_file && /Content-Disposition:.*name="sound"/ { 
                while (getline && $0 !~ /^[[:space:]]*$/) {}
                while (getline && $0 !~ boundary) {
                    print;
                }
                exit;
            }
        ' "$TEMP_FILE" > "$SOUND_DIR/$FILENAME"
    fi
fi

# Если не удалось извлечь, сохраняем с временным именем
if [ ! -f "$SOUND_DIR/$FILENAME" ] || [ ! -s "$SOUND_DIR/$FILENAME" ]; then
    DATE=$(date '+%Y%m%d_%H%M%S')
    FILENAME="uploaded_${DATE}.pcm"
    mv "$TEMP_FILE" "$SOUND_DIR/$FILENAME"
else
    rm -f "$TEMP_FILE"
fi

if [ -f "$SOUND_DIR/$FILENAME" ]; then
    SIZE=$(du -h "$SOUND_DIR/$FILENAME" | cut -f1)
    log_event "Sound uploaded: $FILENAME ($SIZE)"
    echo "{\"status\": \"success\", \"message\": \"Файл загружен\", \"file\": \"$FILENAME\", \"size\": \"$SIZE\"}"
else
    echo '{"status": "error", "message": "Failed to save file"}'
fi
