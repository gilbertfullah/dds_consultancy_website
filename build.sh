#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
# NOTE: migrate is intentionally run in the startCommand (render.yaml)
# so it always executes with DATABASE_URL fully injected at runtime.
