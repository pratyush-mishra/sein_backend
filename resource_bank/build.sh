#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate
# Create superuser if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth.models import Member
import os
if not Member.objects.filter(username=os.environ.get('ADMIN_EMAIL', 'admin')).exists():
    Member.objects.create_superuser(
        email=os.environ.get('ADMIN_EMAIL', 'info@seinglasgow.org.uk'),
        password=os.environ.get('ADMIN_PASSWORD', 'IvanSuliJani2022!')
    )
    print('Superuser created')
EOF