#!/bin/bash

python manage.py dumpdata jwt_auth --output jwt_auth/seeds.json --indent=2;
python manage.py dumpdata descriptions --output descriptions/seeds.json --indent=2;
python manage.py dumpdata mails --output mails/seeds.json --indent=2;
python manage.py dumpdata quizs --output quizs/seeds.json --indent=2;