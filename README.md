# WOOPPAY TEST

## Info

This service provides retrieving, filtering and paginated displaying TV-shows and movies data.
It also has admin panel which allows you to create, delete, edit shows data
and also to download it in `csv` format.

## Requirements:
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

copy .env file (if you want to change some variables, 
make sure to apply changes to both .env files 
in the project root directory and in the `src/` directory)
    
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