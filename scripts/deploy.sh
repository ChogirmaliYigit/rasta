#!/bin/bash
set -euo pipefail

# =============================================
# Rasta B2B Marketplace - Deploy Script
# =============================================

APP_DIR="/opt/rasta"
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    echo "Usage: $0 {deploy|setup-ssl|migrate|rollback|status|logs|restart}"
    echo ""
    echo "Commands:"
    echo "  deploy     - Pull latest code, build and deploy all services"
    echo "  setup-ssl  - Obtain SSL certificates with Let's Encrypt"
    echo "  migrate    - Run Alembic database migrations"
    echo "  rollback   - Rollback to previous deployment"
    echo "  status     - Show status of all services"
    echo "  logs       - Show logs of all services"
    echo "  restart    - Restart all services"
    exit 1
}

check_env() {
    if [ ! -f "$APP_DIR/$ENV_FILE" ]; then
        log_error ".env.production not found! Copy and configure it first:"
        log_error "  cp .env.production.example .env.production"
        exit 1
    fi
    source "$APP_DIR/$ENV_FILE"
    
    # Docker Compose o'zgaruvchilarni topishi uchun .env.production ni .env ga nusxalaymiz
    cp -f "$APP_DIR/$ENV_FILE" "$APP_DIR/.env"
}

deploy() {
    cd "$APP_DIR"
    check_env

    log_info "Saving current commit for potential rollback..."
    PREVIOUS_COMMIT=$(git rev-parse HEAD)
    echo "$PREVIOUS_COMMIT" > .last_deploy_commit

    log_info "Pulling latest code..."
    git pull origin main

    log_info "Building Docker images..."
    docker compose -f "$COMPOSE_FILE" build --no-cache

    log_info "Starting services..."
    docker compose -f "$COMPOSE_FILE" up -d

    log_info "Waiting for services to start..."
    sleep 15

    log_info "Running database migrations..."
    docker compose -f "$COMPOSE_FILE" exec -T backend alembic upgrade head || {
        log_error "Migration failed!"
        rollback
        exit 1
    }

    # Health check
    log_info "Running health checks..."
    sleep 5
    RETRIES=5
    for i in $(seq 1 $RETRIES); do
        if docker compose -f "$COMPOSE_FILE" exec -T backend curl -sf http://localhost:8000/health > /dev/null 2>&1; then
            log_info "✅ Backend is healthy!"
            break
        fi
        if [ "$i" -eq "$RETRIES" ]; then
            log_error "Health check failed after $RETRIES attempts!"
            log_warn "Check logs with: $0 logs"
            exit 1
        fi
        log_warn "Health check attempt $i/$RETRIES failed, retrying in 5s..."
        sleep 5
    done

    # Check web dashboard
    if docker compose -f "$COMPOSE_FILE" ps web-dashboard | grep -q "running"; then
        log_info "✅ Web dashboard is running!"
    else
        log_warn "⚠️  Web dashboard might not be running. Check logs."
    fi

    log_info "✅ Deployment completed successfully!"
    log_info "Current commit: $(git rev-parse --short HEAD)"
}

setup_ssl() {
    cd "$APP_DIR"
    check_env

    log_info "Setting up SSL certificates for ${DOMAIN_NAME}..."

    # Create required directories
    mkdir -p certbot/conf certbot/www

    # Start nginx first (for ACME challenge)
    docker compose -f "$COMPOSE_FILE" up -d nginx

    sleep 5

    # Get certificate
    docker compose -f "$COMPOSE_FILE" run --rm certbot certonly \
        --webroot -w /var/www/certbot \
        --email "${SSL_EMAIL}" \
        -d "${DOMAIN_NAME}" \
        --agree-tos \
        --no-eff-email \
        --force-renewal

    # Restart nginx to load new certs
    docker compose -f "$COMPOSE_FILE" restart nginx

    log_info "✅ SSL certificates obtained successfully!"

    # Setup auto-renewal cron
    CRON_CMD="0 12 * * * cd $APP_DIR && docker compose -f $COMPOSE_FILE run --rm certbot renew && docker compose -f $COMPOSE_FILE restart nginx"
    (crontab -l 2>/dev/null | grep -v "certbot renew"; echo "$CRON_CMD") | crontab -
    log_info "Auto-renewal cron job added (daily at 12:00)"
}

migrate() {
    cd "$APP_DIR"
    log_info "Running database migrations..."
    docker compose -f "$COMPOSE_FILE" exec -T backend alembic upgrade head
    log_info "✅ Migrations completed!"
}

rollback() {
    cd "$APP_DIR"

    if [ ! -f .last_deploy_commit ]; then
        log_error "No previous deployment found for rollback!"
        exit 1
    fi

    PREVIOUS_COMMIT=$(cat .last_deploy_commit)
    log_warn "Rolling back to commit: $PREVIOUS_COMMIT"

    git checkout "$PREVIOUS_COMMIT"

    docker compose -f "$COMPOSE_FILE" build
    docker compose -f "$COMPOSE_FILE" up -d

    sleep 10

    log_info "Running migrations for rolled-back version..."
    docker compose -f "$COMPOSE_FILE" exec -T backend alembic upgrade head || true

    log_info "✅ Rollback completed to $PREVIOUS_COMMIT"
}

status() {
    cd "$APP_DIR"
    log_info "Service status:"
    docker compose -f "$COMPOSE_FILE" ps
    echo ""
    log_info "Resource usage:"
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
}

show_logs() {
    cd "$APP_DIR"
    docker compose -f "$COMPOSE_FILE" logs -f --tail=100
}

restart() {
    cd "$APP_DIR"
    log_info "Restarting all services..."
    docker compose -f "$COMPOSE_FILE" restart
    log_info "✅ All services restarted!"
}

# Main
case "${1:-}" in
    deploy)    deploy ;;
    setup-ssl) setup_ssl ;;
    migrate)   migrate ;;
    rollback)  rollback ;;
    status)    status ;;
    logs)      show_logs ;;
    restart)   restart ;;
    *)         usage ;;
esac
