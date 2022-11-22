release: python ./backend/manage.py migrate
web: node backend/app.js && gunicorn backend.wsgi --log-file -