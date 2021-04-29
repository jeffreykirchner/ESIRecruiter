\#!/bin/bash
python manage.py migrate
apt-get -y install htop
apt-get -y install supervisor
mkdir /var/log/celery/
mkdir /var/log/supervisord/
supervisord -c supervisord.conf
supervisorctl reread
supervisorctl update
supervisorctl -c supervisord.conf
gunicorn --bind=0.0.0.0 --timeout 1800 --max-requests 500 --max-requests-jitter 10  ESIRecruiter.wsgi