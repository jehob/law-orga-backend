# law-orga-backend

# General

Backend for Law&Orga of (Refugee) Law Clinics in Germany

A project of Refugee Law Clinics Deutschland e.V. and Dominik Walser

© Dominik Walser, AGPL-3.0


This project contains a backend based on Django-Rest-Framework. It uses Amazon S3 as file-storage.
Corresponding environment variables have to be set.

# Quickstart

To run this server locally follow these steps.

## Prerequisites

Python with version 3.6.5

Using virtualenv or venv is recommended (your own python installation doesn't get polluted)

## Getting ready
Run these commands:

`pip install requirements_dev.txt`

`python manage.py makemigrations` (despite all should be up to date)

`python manage.py migrate`

`python manage.py populate_deploy_db` (generates essential data in database)

`python manage.py create_dummy_data` (created dummy data for first login)

`python manage.py migrate_to_encryption` (encrypts all dummy data -> command gets unified later)


## Environment variables

To get the server running properly you have to add these environment variables too.
Best would be to add these to your IDE and then run the server through it.

Most env variables are needed for the connection with S3 from AWS and an email provider. Just use the corresponding values here.


| Name        | Description           |
| ------------- |:-------------:|
| DJANGO_SETTINGS_MODULE   | use 'backend.settings' |
| AWS_ACCESS_KEY_ID      |  -     |
| AWS_SECRET_ACCESS_KEY | -      |
| AWS_S3_REGION_NAME | -      |
| AWS_S3_BUCKET_NAME | -      |
| URL | url for redirection if wrong request to backend, eg '127.0.0.1:3000' for local frontend     |
| EMAIL_HOST_PASSWORD | -      |
| EMAIL_HOST_USER | -      |
| EMAIL_PORT | -      |
| EMAIL_USER_TLS | -      |
| EMAIL_USE_SSL | -      |
| EMAIL_HOST | -      |
| EMAIL_ADDRESS | most probably same as EMAIL_HOST_USER      |


## Run server

use this command to run the server

`python manage.py runserver`

