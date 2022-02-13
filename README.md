# WOOPPAY TEST
Requirements:
- `python3.9` or higher
- `make` utility
- `docker-compose`

## Visit site

Site is available [here](http://135.125.191.18/)
Admin page is [here](http://135.125.191.18/admin/)

_Admin user credentials_:
    
- username - `admin`
- password - `admin`

_Regular user credentials_:

- username - `username`
- password - `password`


## Installation

clone repository

    git clone https://github.com/Marik28/wooppay-test
    cd wooppay-test

activate virtual environment

    python3.9 -m venv venv
    source venv/bin/activate

copy .env file
    
    cp .env-exapmle .env && cp .env-example src/.env

start docker container
    
    make up

apply migrations
    
    make migrate
    make makemigrations
    make migrate

insert example data
    
    make insert-data

optionally - create admin user
    
    make createsuperuser