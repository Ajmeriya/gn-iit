#!/bin/bash
# Start script for Render deployment
cd /opt/render/project/src/models || cd "$(dirname "$0")"
export PYTHONPATH="${PWD}:${PYTHONPATH}"
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 ai_service:app

