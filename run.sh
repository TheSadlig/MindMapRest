#!/bin/bash
set -m

function cleanup {
    # When exiting, we want to make sure that flask run is killed
    kill %1 2> /dev/null
    exit
}

function make_space {
    echo
    echo
}

trap cleanup EXIT

# Setting environment variables
export DATABASE_URI="sqlite:////tmp/mindmap.sqlite"
export FLASK_APP=./main.py

# !! Dependencies will be downloaded for the entire computer !!
pip install -r requirements.txt

make_space

nose2 --with-coverage

make_space

flask run&

sleep 3
response_code=`curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/isalive`

if [ "$response_code" -eq "418" ]; then
    make_space
    echo -e "\e[42m\e[30mThe server is now up&running\e[0m"
    make_space
fi

fg %1
