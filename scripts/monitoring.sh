#!/bin/bash

# Configuration
TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
COMPOSE_FILE="/opt/rasta/docker-compose.prod.yml"
THRESHOLD_DISK=90

send_notification() {
    local message="$1"
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ "$TELEGRAM_BOT_TOKEN" != "YOUR_BOT_TOKEN" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d chat_id="${TELEGRAM_CHAT_ID}" \
            -d text="${message}" > /dev/null
    fi
    echo "$message"
}

# 1. Check Container Status
cd /opt/rasta
DOWN_CONTAINERS=$(docker compose -f $COMPOSE_FILE ps --format "{{.Name}} {{.State}}" | grep -v "running" | wc -l)
if [ "$DOWN_CONTAINERS" -gt 0 ]; then
    send_notification "🚨 Rasta Alert: Some containers are down!"
fi

# 2. Check Backend Health
if ! curl -s -f http://localhost:8003/health > /dev/null; then
    send_notification "🚨 Rasta Alert: Backend health check failed!"
fi

# 3. Check Disk Usage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt "$THRESHOLD_DISK" ]; then
    send_notification "🚨 Rasta Alert: Disk usage is above ${THRESHOLD_DISK}% (Current: ${DISK_USAGE}%)"
fi

echo "Monitoring check completed."
