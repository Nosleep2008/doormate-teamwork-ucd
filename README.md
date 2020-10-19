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

## Run
- `python doormate/manage.py runserver 0.0.0.0:8000`

## Add a library
- Add library name to requirements.in (or requirement_dev.in)
- `pip-compile requirements.in` (or requirement_dev.in)
- `pip-sync requirements.txt requirements_dev.txt`
