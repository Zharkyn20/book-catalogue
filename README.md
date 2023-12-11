# Book Catalogue API

1. git clone

```
git clone git@github.com:Zharkyn20/book-catalogue.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```
or
```
make install
```

3. Prepare .env file:

```
cp example.env .env
```
or 
```
make env
```

4. Migrations:

```
python manage.py makemigrations
python manage.py migrate
```
or
```
make migrate
```

5. Run app:
```
python3 manage.py runserver
```
or

```
make run
```

6. Combine all:

```
make all
```