#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y wget xfonts-75dpi xfonts-base

# Download and install wkhtmltopdf
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb || true
apt-get install -f -y
rm wkhtmltox_0.12.6.1-2.jammy_amd64.deb

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 