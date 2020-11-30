# doormate

## Set Up Environment
- Install virtualenv
- `virtualenv venv`
- Activate Environment:
    - unix: `source venv/bin/activate`
- `pip install -r requirements.txt - r requirements_dev.txt`

## Set Up SQLite
- `python doormate/manage.py makemigrations`
- `python doormate/manage.py migrate`
- `python doormate/manage.py makemigrations main`
- `python doormate/manage.py migrate main`

## Run Mosquitto
- docker: `docker run -it --name mosquitto -p 1883:1883 eclipse-mosquitto`

## Run Configuration Server
- `python doormate/manage.py runserver 0.0.0.0:8000`

## Run Scheduler (Django Command)
- `python doormate/manage.py scheduler`

## Add a library
- Add library name to requirements.in (or requirement_dev.in)
- `pip-compile requirements.in` (or requirement_dev.in)
- `pip-sync requirements.txt requirements_dev.txt`
