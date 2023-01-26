#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata jwt_auth/seeds.json
python manage.py loaddata descriptions/seeds.json
python manage.py loaddata quizs/seeds.json
python manage.py loaddata mails/seeds.json

