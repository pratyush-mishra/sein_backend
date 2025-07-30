#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell << EOF
from users.models import Member
import os
admin_email = os.environ.get('ADMIN_EMAIL', 'info@seinglasgow.org.uk')
admin_username = os.environ.get('ADMIN_USERNAME', 'info@seinglasgow.org.uk')
admin_password = os.environ.get('ADMIN_PASSWORD', 'IvanSuliJani2022!')
if not Member.objects.filter(username=admin_username).exists():
    Member.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password
    )
    print('Superuser created')
EOF
