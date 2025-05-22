#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
sudo apt-get update
sudo apt-get install -y wkhtmltopdf xvfb

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 