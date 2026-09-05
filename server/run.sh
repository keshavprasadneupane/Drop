#!/bin/sh
set -e
# Start Uvicorn bound to 0.0.0.0 so Docker can route traffic into the container
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload