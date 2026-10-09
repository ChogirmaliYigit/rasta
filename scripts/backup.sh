#!/bin/bash
set -e

BACKUP_DIR="/opt/backups/rasta"
mkdir -p $BACKUP_DIR

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql.gz"
COMPOSE_FILE="/opt/rasta/docker-compose.prod.yml"

echo "Starting database backup: ${BACKUP_FILE}"

# Dump database directly from container and compress
docker compose -f $COMPOSE_FILE exec -T db pg_dump -U rasta_db_user rasta_db | gzip > $BACKUP_FILE

echo "Backup created successfully!"

# Cleanup old backups (keep last 7 days)
echo "Cleaning up backups older than 7 days..."
find $BACKUP_DIR -type f -name "db_backup_*.sql.gz" -mtime +7 -exec rm {} \;

# Optional: Upload to S3 or remote storage here
# aws s3 cp $BACKUP_FILE s3://my-backup-bucket/rasta/

echo "Backup process finished."
