language: python
python:
- '3.7'
install:
- pip install -r requirements-travis.txt
script:
- python manage.py test

