#!/bin/bash

# to stop on first error
set -e

# Detect the OS
OS="$(uname)"

# Delete older .pyc files
# find . -type d \( -name env -o -name venv  \) -prune -false -o -name "*.pyc" -exec rm -rf {} \;

# Run required migrations
export FLASK_APP=core/server.py

# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/

# Run server
if [[ "$OS" == "Linux" || "$OS" == "Darwin" ]]; then
    gunicorn -c gunicorn_config.py core.server:app
else
    python -m waitress --listen=0.0.0.0:5000 core.server:app
fi
