#!/usr/bin/env bash

# ====================
# load environment variables from .env
# ====================

# auto-export all variables we load
set -a
# read the .env file and set variables
source .env
# stop auto-exporting after this
set +a

# ====================
# determine mode: dev or prod
# ====================

# first argument passed to script, default = "dev"
MODE=${1:-dev}

# ====================
# run uvicorn depending on mode
# ====================

if [ "$MODE" = "prod" ]; then
  # production mode: no auto-reload, multiple workers
  echo "🚀 Starting FastAPI in PRODUCTION mode..."
  exec uvicorn app.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS"
else
  # dev mode: auto-reload on code changes, single process
  echo "🛠 Starting FastAPI in DEVELOPMENT mode..."
  exec uvicorn app.main:app \
    --host "$HOST" \
    --port "$PORT" \
    --reload
fi
