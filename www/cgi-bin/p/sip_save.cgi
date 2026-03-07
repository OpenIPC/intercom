#!/bin/sh
echo "Content-type: text/html; charset=utf-8"
echo ""

# Получаем параметры из QUERY_STRING
USER=$(echo "$QUERY_STRING" | sed -n 's/.*user=\([^&]*\).*/\1/p')
SERVER=$(echo "$QUERY_STRING" | sed -n 's/.*server=\([^&]*\).*/\1/p')
PASS=$(echo "$QUERY_STRING" | sed -n 's/.*pass=\([^&]*\).*/\1/p')
TRANSPORT=$(echo "$QUERY_STRING" | sed -n 's/.*transport=\([^&]*\).*/\1/p')
AUTO=$(echo "$QUERY_STRING" | sed -n 's/.*auto=\([^&]*\).*/\1/p')

# Декодируем URL
urldecode() {
    echo -e "$(echo "$1" | sed 's/+/ /g;s/%/\\x/g')"
}

USER=$(urldecode "$USER")
SERVER=$(urldecode "$SERVER")
PASS=$(urldecode "$PASS")
[ -z "$TRANSPORT" ] && TRANSPORT="udp"

# HTML страница с результатом
echo "<!DOCTYPE html>"
echo "<html>"
echo "<head>"
echo "    <meta charset='UTF-8'>"
echo "    <title>SIP - Сохранение</title>"
echo "    <style>"
echo "        body { font-family: Arial; margin: 20px; background: #f5f5f5; }"
echo "        .container { max-width: 600px; margin: 0 auto; }"
echo "        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }"
echo "        .btn { padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }"
echo "        .success { color: green; }"
echo "        .error { color: red; }"
echo "    </style>"
echo "</head>"
echo "<body>"
echo "    <div class='container'>"
echo "        <h1>📞 SIP - Результат</h1>"
echo "        <div class='card'>"

if [ -n "$USER" ] && [ -n "$SERVER" ] && [ -n "$PASS" ]; then
    # Формируем аккаунт
    if [ "$AUTO" = "true" ]; then
        ACCOUNT="<sip:$USER@$SERVER;transport=$TRANSPORT>;auth_pass=$PASS;answermode=auto;regint=60"
    else
        ACCOUNT="<sip:$USER@$SERVER;transport=$TRANSPORT>;auth_pass=$PASS;regint=60"
    fi
    
    # Сохраняем
    mkdir -p /etc/baresip
    {
        echo "# SIP account for doorphone"
        echo "$ACCOUNT"
    } > /etc/baresip/accounts
    
    # Перезапускаем SIP
    killall baresip 2>/dev/null
    sleep 1
    baresip -f /etc/baresip -d > /dev/null 2>&1 &
    
    echo "            <h2 class='success'>✅ Аккаунт успешно сохранен!</h2>"
    echo "            <pre style='background:#f0f0f0; padding:10px;'>$ACCOUNT</pre>"
else
    echo "            <h2 class='error'>❌ Ошибка: Не все параметры переданы</h2>"
    echo "            <p>USER: $USER</p>"
    echo "            <p>SERVER: $SERVER</p>"
    echo "            <p>PASS: ${#PASS} символов</p>"
fi

echo "            <p><a href='/cgi-bin/p/sip_manager.cgi' class='btn'>Вернуться к SIP Manager</a></p>"
echo "        </div>"
echo "    </div>"
echo "</body>"
echo "</html>"
