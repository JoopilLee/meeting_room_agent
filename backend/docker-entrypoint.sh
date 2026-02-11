#!/bin/sh
set -e

if [ -n "$DATABASE_URL" ] || [ -n "$DB_HOST" ]; then
  echo "Waiting for PostgreSQL..."
  host="${DB_HOST:-localhost}"
  port="${DB_PORT:-5432}"
  for i in $(seq 1 30); do
    if python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
  s.connect(('$host', $port))
  s.close()
  exit(0)
except Exception:
  exit(1)
" 2>/dev/null; then
    echo "PostgreSQL is ready."
    break
  fi
  if [ $i -eq 30 ]; then
    echo "Timeout waiting for PostgreSQL."
    exit 1
  fi
  sleep 1
  done
fi

echo "Initializing database..."
python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from app.db.session import init_db
init_db()
print('Database initialized.')
"

exec "$@"
