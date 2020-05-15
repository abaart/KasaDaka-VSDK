release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn vsdk.wsgi --log-file -
