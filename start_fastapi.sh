#!/bin/bash

set -e

# Start FastAPI service
echo "🚀 start Knowledge Graph Demo API..."
uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
