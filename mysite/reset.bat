git clean -fxd .\media\uploads\*
git clean -fxd ..\mymodel\uploads\*

del db.sqlite3
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py createsuperuser --username a3 --email a3@c.com

PAUSE