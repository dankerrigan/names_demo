# Riak Json Names Demo

## Requirements
+ riak_json_python_client
+ Python 2.7
+ Flask
+ Requests


## Getting started

    git clone https://github.com/dankerrigan/names_demo
    cd names_demo

### Load some data

    mkdir names_data
    wget http://www.ssa.gov/oact/babynames/state/namesbystate.zip

    cd names_data && unzip ../namesbystate.zip

    cd ../src
    python -m names.util.import_state_data ~/projects/names_demo/names_data/

### Run the web server

    ## Run the web server
    python run_web.py

### Search for names starting with N characters (Dan)

    curl http://localhost:5000/search/Dan

### Get name usage for all years in system

    curl http://localhost:5000/usage/Daniel

### Get the top or bottom N (1) names data for a State (WV)

    curl http://localhost:5000/popularity/state/WV/most/1
    curl http://localhost:5000/popularity/state/WV/least/1

### Get the top or bottom N (1) names for all 50 states

    curl http://localhost:5000/popularity/states/most/1
    curl http://localhost:5000/popularity/states/least/1

## Project Layout

+ Names data class is in src/names/data/names_data.py
+ User data class is in src/names/data/user_data.py
+ Web resources are defined in src/names/web/www.py
+ Static web resources are located in src/names/web/static
+ Web templates are located in src/names/web/templates