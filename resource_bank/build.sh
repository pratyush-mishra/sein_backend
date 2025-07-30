#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate
# Create superuser if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth.models import User
import os
if not User.objects.filter(username=os.environ.get('ADMIN_USERNAME', 'admin')).exists():
    User.objects.create_superuser(
        username=os.environ.get('ADMIN_USERNAME', 'admin'),
        email=os.environ.get('ADMIN_EMAIL', 'info@seinglasgow.org.uk'),
        password=os.environ.get('ADMIN_PASSWORD', 'IvanSuliJani2022!')
    )
    print('Superuser created')
EOF