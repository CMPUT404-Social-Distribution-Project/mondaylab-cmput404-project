release: python ./backend/manage.py migrate
web: cd socialapp && npm i && npm start && gunicorn backend.wsgi --log-file -
server: cd backend && npm i && npm start