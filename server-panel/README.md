# Setup project

```bash
cd project_root
py -m venv venv
source venv/Scripte/activate
pip install -r requirements.txt
pip freeze > requirements.txt
python manage.py makemigrations Boards users
```
Note :
before running migration you have to add HStoreExtention inside Boards migration file <br>
helper reference :  https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/operations/#create-postgresql-extensions
```bash
python manage.py migrate
```

# ENV confige

```env
DEBUG= set 1 as True or 0 as False
SECRET_KEY= ' Your Django secret key '
POSTGRES_DB= database name
POSTGRES_USER= database username
POSTGRES_PASSWORD= database password
POSTGRES_PORT= database port server
POSTGRES_HOST= database ip server
PORT= server port
```