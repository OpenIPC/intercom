#!/bin/sh
# Backup API for OpenIPC Doorphone
# Supports: internal storage, SD card, USB drives
# Components: CGI, SIP, Keys, MQTT, Scripts, Init, Majestic, UART, Telegram

#===============================================================================
# Helper Functions
#===============================================================================

# Function to decode URL parameters
urldecode() {
    echo -e "$(echo "$1" | sed 's/+/ /g;s/%/\\x/g')"
}

# Logging function
log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - BACKUP - $1" >> /var/log/door_monitor.log
}

# Function to mount a device
mount_device() {
    device=$1
    mount_point="/mnt/$(basename $device)"
    
    if mount | grep -q "$mount_point"; then
        echo "$mount_point"
        return 0
    fi
    
    mkdir -p "$mount_point"
    
    if blkid "$device" | grep -q "vfat"; then
        mount -t vfat "$device" "$mount_point" 2>/dev/null
    elif blkid "$device" | grep -q "ext[234]"; then
        mount -t ext4 "$device" "$mount_point" 2>/dev/null
    else
        mount "$device" "$mount_point" 2>/dev/null
    fi
    
    if [ $? -eq 0 ]; then
        echo "$mount_point"
        return 0
    else
        echo ""
        return 1
    fi
}

# Function to format file size
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

#===============================================================================
# Main Request Handling
#===============================================================================

# Get action from query string
action=$(echo "$QUERY_STRING" | sed -n 's/.*action=\([^&]*\).*/\1/p')

# Handle download action - must be first because it returns file, not JSON
if [ "$action" = "download_backup" ]; then
    storage=$(echo "$QUERY_STRING" | sed -n 's/.*storage=\([^&]*\).*/\1/p')
    storage=$(urldecode "$storage")
    file=$(echo "$QUERY_STRING" | sed -n 's/.*file=\([^&]*\).*/\1/p')
    
    if [ -z "$storage" ] || [ -z "$file" ]; then
        echo "Status: 400 Bad Request"
        echo "Content-type: text/plain"
        echo ""
        echo "Missing parameters"
        exit 1
    fi
    
    if [ "$storage" = "internal" ]; then
        BACKUP_DIR="/root/backups"
    else
        mount_point="/mnt/$(basename $storage)"
        BACKUP_DIR="${mount_point}/backups"
    fi
    
    BACKUP_FILE="${BACKUP_DIR}/${file}"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo "Status: 404 Not Found"
        echo "Content-type: text/plain"
        echo ""
        echo "Backup file not found"
        exit 1
    fi
    
    echo "Content-type: application/octet-stream"
    echo "Content-Disposition: attachment; filename=\"$file\""
    echo "Content-Transfer-Encoding: binary"
    echo "Cache-Control: no-cache"
    echo "Pragma: no-cache"
    echo "Content-length: $(stat -c%s "$BACKUP_FILE" 2>/dev/null || stat -f%z "$BACKUP_FILE" 2>/dev/null)"
    echo ""
    cat "$BACKUP_FILE"
    exit 0
fi

# For all other actions, return JSON
echo "Content-type: application/json"
echo ""

case "$action" in
    #===========================================================================
    # Storage Scanning
    #===========================================================================
    "scan_storage")
        devices=""
        first=true
        
        # Internal storage
        ROOT_FREE=$(df -h / | tail -1 | awk '{print $4}')
        ROOT_TOTAL=$(df -h / | tail -1 | awk '{print $2}')
        devices="${devices}{\"path\":\"internal\",\"name\":\"Internal Storage\",\"mount\":\"/root/backups\",\"free\":\"${ROOT_FREE}\",\"total\":\"${ROOT_TOTAL}\",\"icon\":\"📁\",\"available\":true}"
        first=false
        
        # SD Card
        if [ -e /dev/mmcblk0p1 ]; then
            if blkid /dev/mmcblk0p1 >/dev/null 2>&1; then
                LABEL=$(blkid /dev/mmcblk0p1 | sed -n 's/.*LABEL="\([^"]*\)".*/\1/p')
                NAME="SD Card${LABEL:+ ($LABEL)}"
                mount_point=$(mount_device "/dev/mmcblk0p1")
                if [ -n "$mount_point" ]; then
                    FREE=$(df -h "$mount_point" | tail -1 | awk '{print $4}')
                    TOTAL=$(df -h "$mount_point" | tail -1 | awk '{print $2}')
                    devices="${devices},{\"path\":\"/dev/mmcblk0p1\",\"name\":\"${NAME}\",\"mount\":\"$mount_point\",\"free\":\"${FREE}\",\"total\":\"${TOTAL}\",\"icon\":\"💾\",\"available\":true}"
                else
                    devices="${devices},{\"path\":\"/dev/mmcblk0p1\",\"name\":\"SD Card\",\"mount\":\"\",\"free\":\"0\",\"total\":\"0\",\"icon\":\"💾\",\"available\":false,\"error\":\"Mount failed\"}"
                fi
            else
                devices="${devices},{\"path\":\"/dev/mmcblk0p1\",\"name\":\"SD Card\",\"mount\":\"\",\"free\":\"0\",\"total\":\"0\",\"icon\":\"💾\",\"available\":false,\"error\":\"No filesystem\"}"
            fi
        else
            devices="${devices},{\"path\":\"sdcard\",\"name\":\"SD Card\",\"mount\":\"\",\"free\":\"0\",\"total\":\"0\",\"icon\":\"💾\",\"available\":false,\"error\":\"Not detected\"}"
        fi
        
        # USB devices
        usb_found=false
        for usb in /dev/sd*[0-9]; do
            if [ -e "$usb" ] && [ -b "$usb" ]; then
                if blkid "$usb" >/dev/null 2>&1; then
                    LABEL=$(blkid "$usb" | sed -n 's/.*LABEL="\([^"]*\)".*/\1/p')
                    NAME="USB Flash${LABEL:+ ($LABEL)}"
                    mount_point=$(mount_device "$usb")
                    if [ -n "$mount_point" ]; then
                        FREE=$(df -h "$mount_point" | tail -1 | awk '{print $4}')
                        TOTAL=$(df -h "$mount_point" | tail -1 | awk '{print $2}')
                        devices="${devices},{\"path\":\"$usb\",\"name\":\"${NAME}\",\"mount\":\"$mount_point\",\"free\":\"${FREE}\",\"total\":\"${TOTAL}\",\"icon\":\"💿\",\"available\":true}"
                        usb_found=true
                    fi
                fi
            fi
        done
        
        if [ "$usb_found" = false ]; then
            devices="${devices},{\"path\":\"usb\",\"name\":\"USB Flash Drive\",\"mount\":\"\",\"free\":\"0\",\"total\":\"0\",\"icon\":\"💿\",\"available\":false,\"error\":\"Not detected\"}"
        fi
        
        echo "{\"status\":\"success\",\"devices\":[$devices]}"
        ;;
        
    #===========================================================================
    # SD Card Check
    #===========================================================================
    "check_sd")
        SD_DEV="/dev/mmcblk0p1"
        SD_MOUNT="/mnt/mmcblk0p1"
        
        if [ ! -e "$SD_DEV" ]; then
            echo '{"status": "error", "message": "SD card not found"}'
            exit 0
        fi
        
        # Try to mount if not mounted
        if ! mount | grep -q "$SD_MOUNT"; then
            mkdir -p "$SD_MOUNT"
            mount "$SD_DEV" "$SD_MOUNT" 2>/dev/null
            if [ $? -ne 0 ]; then
                echo '{"status": "error", "message": "SD card mount failed"}'
                exit 0
            fi
        fi
        
        # Get space info
        FREE_SPACE=$(df -h "$SD_MOUNT" | tail -1 | awk '{print $4}')
        TOTAL_SPACE=$(df -h "$SD_MOUNT" | tail -1 | awk '{print $2}')
        USED_SPACE=$(df -h "$SD_MOUNT" | tail -1 | awk '{print $3}')
        USED_PERCENT=$(df -h "$SD_MOUNT" | tail -1 | awk '{print $5}' | sed 's/%//')
        
        echo "{\"status\": \"success\", \"message\": \"SD card ready\", \"free\": \"${FREE_SPACE}\", \"total\": \"${TOTAL_SPACE}\", \"used\": \"${USED_SPACE}\", \"used_percent\": ${USED_PERCENT}}"
        ;;
        
    #===========================================================================
    # Create Backup
    #===========================================================================
    "create_backup")
        storage=$(echo "$QUERY_STRING" | sed -n 's/.*storage=\([^&]*\).*/\1/p')
        storage=$(urldecode "$storage")
        components=$(echo "$QUERY_STRING" | sed -n 's/.*components=\([^&]*\).*/\1/p')
        
        if [ -z "$storage" ]; then
            echo '{"status": "error", "message": "No storage selected"}'
            exit 1
        fi
        
        # Setup backup directory
        if [ "$storage" = "internal" ]; then
            BACKUP_DIR="/root/backups"
            mkdir -p "${BACKUP_DIR}"
        else
            if [ ! -e "$storage" ]; then
                echo "{\"status\": \"error\", \"message\": \"Device $storage not found\"}"
                exit 1
            fi
            mount_point=$(mount_device "$storage")
            if [ -z "$mount_point" ]; then
                echo "{\"status\": \"error\", \"message\": \"Failed to mount $storage\"}"
                exit 1
            fi
            BACKUP_DIR="${mount_point}/backups"
            mkdir -p "${BACKUP_DIR}"
        fi
        
        # Check free space (need at least 1MB)
        df_cmd=$(df -k "$(dirname ${BACKUP_DIR})" | tail -1)
        FREE_SPACE=$(echo "$df_cmd" | awk '{print $4}')
        if [ "$FREE_SPACE" -lt 1024 ]; then
            echo '{"status": "error", "message": "Insufficient free space"}'
            exit 1
        fi
        
        DATE=$(date '+%Y%m%d_%H%M%S')
        BACKUP_NAME="doorphone_backup_${DATE}"
        TEMP_DIR="/tmp/${BACKUP_NAME}"
        
        mkdir -p "${TEMP_DIR}"
        
        # Create directory structure
        mkdir -p "${TEMP_DIR}/www/cgi-bin/p"
        mkdir -p "${TEMP_DIR}/etc/baresip"
        mkdir -p "${TEMP_DIR}/usr/bin"
        mkdir -p "${TEMP_DIR}/etc/init.d"
        mkdir -p "${TEMP_DIR}/etc"
        mkdir -p "${TEMP_DIR}/etc/webui"
        
        log_event "Creating backup: $BACKUP_NAME with components: $components"
        
        # Copy selected components
        if echo "$components" | grep -q "cgi"; then
            cp -r /var/www/cgi-bin/p/*.cgi "${TEMP_DIR}/www/cgi-bin/p/" 2>/dev/null
            log_event "  - CGI scripts backed up"
        fi
        
        if echo "$components" | grep -q "baresip"; then
            [ -f /etc/baresip/accounts ] && cp /etc/baresip/accounts "${TEMP_DIR}/etc/baresip/" 2>/dev/null
            [ -f /etc/baresip/call_number ] && cp /etc/baresip/call_number "${TEMP_DIR}/etc/baresip/" 2>/dev/null
            [ -f /etc/baresip/config ] && cp /etc/baresip/config "${TEMP_DIR}/etc/baresip/" 2>/dev/null
            log_event "  - SIP configs backed up"
        fi
        
        if echo "$components" | grep -q "keys"; then
            [ -f /etc/door_keys.conf ] && cp /etc/door_keys.conf "${TEMP_DIR}/" 2>/dev/null
            log_event "  - Key database backed up"
        fi
        
        if echo "$components" | grep -q "mqtt"; then
            [ -f /etc/mqtt.conf ] && cp /etc/mqtt.conf "${TEMP_DIR}/etc/" 2>/dev/null
            log_event "  - MQTT config backed up"
        fi
        
        if echo "$components" | grep -q "telegram"; then
            [ -f /etc/webui/telegram.conf ] && cp /etc/webui/telegram.conf "${TEMP_DIR}/etc/webui/" 2>/dev/null
            log_event "  - Telegram config backed up"
        fi
        
        if echo "$components" | grep -q "scripts"; then
            [ -f /usr/bin/door_monitor.sh ] && cp /usr/bin/door_monitor.sh "${TEMP_DIR}/usr/bin/" 2>/dev/null
            [ -f /usr/bin/mqtt_client.sh ] && cp /usr/bin/mqtt_client.sh "${TEMP_DIR}/usr/bin/" 2>/dev/null
            [ -f /usr/bin/check_temp_keys.sh ] && cp /usr/bin/check_temp_keys.sh "${TEMP_DIR}/usr/bin/" 2>/dev/null
            [ -f /usr/bin/start_baresip.sh ] && cp /usr/bin/start_baresip.sh "${TEMP_DIR}/usr/bin/" 2>/dev/null
            log_event "  - System scripts backed up"
        fi
        
        if echo "$components" | grep -q "init"; then
            [ -f /etc/init.d/S99door ] && cp /etc/init.d/S99door "${TEMP_DIR}/etc/init.d/" 2>/dev/null
            log_event "  - Init scripts backed up"
        fi
        
        if echo "$components" | grep -q "majestic"; then
            [ -f /etc/majestic.yaml ] && cp /etc/majestic.yaml "${TEMP_DIR}/etc/" 2>/dev/null
            log_event "  - Majestic config backed up"
        fi
        
        if echo "$components" | grep -q "uart"; then
            [ -f /etc/rc.local ] && cp /etc/rc.local "${TEMP_DIR}/etc/" 2>/dev/null
            stty -F /dev/ttyS0 -a 2>/dev/null > "${TEMP_DIR}/uart_settings.txt"
            stty -F /dev/ttyAMA0 -a 2>/dev/null >> "${TEMP_DIR}/uart_settings.txt"
            log_event "  - UART settings backed up"
        fi
        
        # Create backup info file
        {
            echo "Backup created: $(date)"
            echo "Camera: $(hostname)"
            echo "IP: $(ip addr show | grep -o '192\.168\.[0-9]*\.[0-9]*' | head -1)"
            echo "Storage: $storage"
            echo "Components: $components"
            echo "MQTT enabled: $(grep MQTT_ENABLED /etc/mqtt.conf 2>/dev/null || echo 'unknown')"
            echo "Telegram enabled: $(grep telegram_enabled /etc/webui/telegram.conf 2>/dev/null || echo 'unknown')"
        } > "${TEMP_DIR}/backup_info.txt"
        
        # Create archive
        cd /tmp
        tar -cf "${BACKUP_DIR}/${BACKUP_NAME}.tar" "${BACKUP_NAME}/" 2>/tmp/tar_error
        TAR_RESULT=$?
        
        if [ $TAR_RESULT -ne 0 ] || [ ! -f "${BACKUP_DIR}/${BACKUP_NAME}.tar" ]; then
            ERROR_MSG=$(cat /tmp/tar_error 2>/dev/null)
            echo "{\"status\": \"error\", \"message\": \"Archive creation failed: $ERROR_MSG\"}"
            rm -rf "${TEMP_DIR}"
            exit 1
        fi
        
        # Compress if gzip available
        if command -v gzip >/dev/null 2>&1; then
            gzip -f "${BACKUP_DIR}/${BACKUP_NAME}.tar"
            BACKUP_FILE="${BACKUP_NAME}.tar.gz"
        else
            BACKUP_FILE="${BACKUP_NAME}.tar"
        fi
        
        # Cleanup temp directory
        rm -rf "${TEMP_DIR}"
        
        # Keep only last 10 backups
        cd "${BACKUP_DIR}"
        ls -t doorphone_backup_* 2>/dev/null | tail -n +11 | xargs -r rm
        
        if [ -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
            SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
            COUNT=$(ls -1 ${BACKUP_DIR}/doorphone_backup_* ${BACKUP_DIR}/uploaded_backup_* 2>/dev/null | wc -l)
            
            log_event "Backup created: ${BACKUP_FILE} (${SIZE}) on ${storage}"
            
            echo "{\"status\": \"success\", \"message\": \"Backup created\", \"file\": \"${BACKUP_FILE}\", \"size\": \"${SIZE}\", \"total\": ${COUNT}}"
        else
            echo "{\"status\": \"error\", \"message\": \"Failed to create archive\"}"
        fi
        ;;
        
    #===========================================================================
    # List Backups
    #===========================================================================
    "list_backups")
        storage=$(echo "$QUERY_STRING" | sed -n 's/.*storage=\([^&]*\).*/\1/p')
        storage=$(urldecode "$storage")
        
        if [ -z "$storage" ]; then
            echo '{"status": "error", "message": "No storage specified"}'
            exit 1
        fi
        
        if [ "$storage" = "internal" ]; then
            BACKUP_DIR="/root/backups"
        else
            mount_point="/mnt/$(basename $storage)"
            BACKUP_DIR="${mount_point}/backups"
        fi
        
        mkdir -p "${BACKUP_DIR}" 2>/dev/null
        
        echo -n '{"status": "success", "backups": ['
        first=true
        cd "${BACKUP_DIR}" 2>/dev/null
        if [ $? -eq 0 ]; then
            ls -t *.tar *.tar.gz 2>/dev/null | while read file; do
                if [ -n "$file" ] && [ -f "$file" ]; then
                    if [ "$first" = true ]; then
                        first=false
                    else
                        echo -n ','
                    fi
                    size=$(du -h "$file" 2>/dev/null | cut -f1)
                    [ -z "$size" ] && size="0B"
                    
                    if echo "$file" | grep -q "doorphone_backup_"; then
                        date=$(echo "$file" | sed 's/doorphone_backup_\(.*\)\.tar.*/\1/')
                    elif echo "$file" | grep -q "uploaded_backup_"; then
                        date=$(echo "$file" | sed 's/uploaded_backup_\(.*\)\.tar.*/\1/')
                    else
                        date=$(date -r "$file" '+%Y%m%d_%H%M%S' 2>/dev/null || echo "unknown")
                    fi
                    
                    echo -n "{\"file\":\"$file\",\"size\":\"$size\",\"date\":\"$date\"}"
                fi
            done
        fi
        echo ']}'
        ;;
        
    #===========================================================================
    # Upload Backup
    #===========================================================================
    "upload_backup")
        if [ "$REQUEST_METHOD" != "POST" ]; then
            echo '{"status": "error", "message": "Method not allowed"}'
            exit 1
        fi
        
        storage=$(echo "$QUERY_STRING" | sed -n 's/.*storage=\([^&]*\).*/\1/p')
        storage=$(urldecode "$storage")
        
        if [ -z "$storage" ]; then
            echo '{"status": "error", "message": "No storage specified"}'
            exit 1
        fi
        
        if [ "$storage" = "internal" ]; then
            BACKUP_DIR="/root/backups"
        else
            mount_point="/mnt/$(basename $storage)"
            BACKUP_DIR="${mount_point}/backups"
        fi
        
        mkdir -p "${BACKUP_DIR}"
        
        DATE=$(date '+%Y%m%d_%H%M%S')
        TEMP_FILE="/tmp/upload_$$.tmp"
        SAVED_FILE="${BACKUP_DIR}/uploaded_backup_${DATE}.tar"
        
        # Read POST data
        cat > "$TEMP_FILE"
        BYTES=$(stat -c%s "$TEMP_FILE" 2>/dev/null)
        
        if [ "$BYTES" -eq 0 ]; then
            echo '{"status": "error", "message": "Empty file"}'
            rm -f "$TEMP_FILE"
            exit 1
        fi
        
        mv "$TEMP_FILE" "$SAVED_FILE"
        SIZE=$(du -h "$SAVED_FILE" | cut -f1)
        log_event "Backup uploaded: $(basename $SAVED_FILE) (${SIZE}) on ${storage}"
        echo "{\"status\": \"success\", \"message\": \"File uploaded\", \"file\": \"$(basename $SAVED_FILE)\", \"size\": \"${SIZE}\"}"
        ;;
        
    #===========================================================================
    # Restore Backup
    #===========================================================================
    "restore_backup")
        storage=$(echo "$QUERY_STRING" | sed -n 's/.*storage=\([^&]*\).*/\1/p')
        storage=$(urldecode "$storage")
        file=$(echo "$QUERY_STRING" | sed -n 's/.*file=\([^&]*\).*/\1/p')
        
        if [ -z "$storage" ] || [ -z "$file" ]; then
            echo '{"status": "error", "message": "Missing parameters"}'
            exit 1
        fi
        
        if [ "$storage" = "internal" ]; then
            BACKUP_DIR="/root/backups"
        else
            mount_point="/mnt/$(basename $storage)"
            BACKUP_DIR="${mount_point}/backups"
        fi
        
        if [ ! -f "${BACKUP_DIR}/${file}" ]; then
            echo '{"status": "error", "message": "Backup file not found"}'
            exit 1
        fi
        
        TEMP_DIR="/tmp/restore_$$"
        mkdir -p "${TEMP_DIR}"
        
        log_event "Restoring backup: $file from $storage"
        
        # Extract archive
        case "$file" in
            *.tar.gz)
                tar -xzf "${BACKUP_DIR}/${file}" -C "${TEMP_DIR}" 2>/tmp/untar_error
                ;;
            *.tar)
                tar -xf "${BACKUP_DIR}/${file}" -C "${TEMP_DIR}" 2>/tmp/untar_error
                ;;
            *)
                echo '{"status": "error", "message": "Unsupported archive format"}'
                rm -rf "${TEMP_DIR}"
                exit 1
                ;;
        esac
        
        if [ $? -ne 0 ]; then
            ERROR_MSG=$(cat /tmp/untar_error 2>/dev/null)
            echo "{\"status\": \"error\", \"message\": \"Extraction error: $ERROR_MSG\"}"
            rm -rf "${TEMP_DIR}"
            exit 1
        fi
        
        # Find extracted directory
        EXTRACTED_DIR=$(find "${TEMP_DIR}" -type d | grep -v "^${TEMP_DIR}$" | head -1)
        
        if [ -z "$EXTRACTED_DIR" ]; then
            EXTRACTED_DIR="$TEMP_DIR"
        fi
        
        cd "$EXTRACTED_DIR"
        
        # Restore files with logging
        if [ -d "www/cgi-bin/p" ]; then
            cp -rf www/cgi-bin/p/*.cgi /var/www/cgi-bin/p/ 2>/dev/null
            chmod +x /var/www/cgi-bin/p/*.cgi 2>/dev/null
            log_event "  - Restored CGI scripts"
        fi
        
        if [ -d "etc/baresip" ]; then
            cp -rf etc/baresip/* /etc/baresip/ 2>/dev/null
            log_event "  - Restored SIP configs"
        fi
        
        if [ -f "door_keys.conf" ]; then
            cp -f door_keys.conf /etc/door_keys.conf
            chmod 666 /etc/door_keys.conf
            log_event "  - Restored key database"
        fi
        
        if [ -f "etc/mqtt.conf" ]; then
            cp -f etc/mqtt.conf /etc/mqtt.conf
            chmod 644 /etc/mqtt.conf
            log_event "  - Restored MQTT config"
        fi
        
        if [ -f "etc/webui/telegram.conf" ]; then
            cp -f etc/webui/telegram.conf /etc/webui/telegram.conf
            chmod 644 /etc/webui/telegram.conf
            log_event "  - Restored Telegram config"
        fi
        
        if [ -d "usr/bin" ]; then
            cp -rf usr/bin/* /usr/bin/ 2>/dev/null
            chmod +x /usr/bin/*.sh 2>/dev/null
            chmod +x /usr/bin/mqtt_client.sh 2>/dev/null
            log_event "  - Restored system scripts"
        fi
        
        if [ -d "etc/init.d" ]; then
            cp -rf etc/init.d/* /etc/init.d/ 2>/dev/null
            chmod +x /etc/init.d/S99door 2>/dev/null
            log_event "  - Restored init scripts"
        fi
        
        if [ -f "etc/majestic.yaml" ]; then
            cp -f etc/majestic.yaml /etc/majestic.yaml 2>/dev/null
            log_event "  - Restored majestic config"
        fi
        
        if [ -f "etc/rc.local" ]; then
            cp -f etc/rc.local /etc/rc.local 2>/dev/null
            chmod +x /etc/rc.local
            log_event "  - Restored rc.local"
        fi
        
        # Cleanup
        rm -rf "${TEMP_DIR}"
        
        log_event "Restore completed: ${file}"
        echo '{"status": "success", "message": "Backup restored. Reboot recommended."}'
        ;;
        
    #===========================================================================
    # Delete Backup
    #===========================================================================
    "delete_backup")
        storage=$(echo "$QUERY_STRING" | sed -n 's/.*storage=\([^&]*\).*/\1/p')
        storage=$(urldecode "$storage")
        file=$(echo "$QUERY_STRING" | sed -n 's/.*file=\([^&]*\).*/\1/p')
        
        if [ -z "$storage" ] || [ -z "$file" ]; then
            echo '{"status": "error", "message": "Missing parameters"}'
            exit 1
        fi
        
        if [ "$storage" = "internal" ]; then
            BACKUP_DIR="/root/backups"
        else
            mount_point="/mnt/$(basename $storage)"
            BACKUP_DIR="${mount_point}/backups"
        fi
        
        if [ -f "${BACKUP_DIR}/${file}" ]; then
            rm -f "${BACKUP_DIR}/${file}"
            log_event "Deleted backup: ${file} from ${storage}"
            echo '{"status": "success", "message": "Backup deleted"}'
        else
            echo '{"status": "error", "message": "File not found"}'
        fi
        ;;
        
    #===========================================================================
    # Unknown Action
    #===========================================================================
    *)
        echo '{"status": "error", "message": "Unknown action"}'
        ;;
esac
