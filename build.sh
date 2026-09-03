#!/bin/bash
set -e

# 1. Install dependencies
pip install -r requirements.txt
npm ci

# 2. Run uptime monitor (writes public/sites-data.json)
python3 uptime.py

# 3. Build the Vue site
npm run build

echo "Build complete. Output in ./public"
