#!/bin/bash

set -e

cd /home/gamixlp/gymtracker

source .venv/bin/activate

python src/generate_graphs.py
python src/generate_site.py

git add studios/ docs/ src/ requirements.txt .gitignore daily_push.sh

if git diff --cached --quiet; then
  echo "Keine Änderungen zum Pushen."
  exit 0
fi

git commit -m "Update gym graphs"
git push
