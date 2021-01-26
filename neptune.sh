#!/bin/bash

if [ ! -d ".python" ]; then
    echo "Setting up environment..."
    apt install -y python3 python3-venv
    python3 -m venv .python
    chmod -R 755 .python
    .python/bin/activate
    .python/bin/pip3 install flask kubernetes influxdb_client deepdiff pyArango pandas
fi

.python/bin/activate

if [ -d "src" ]; then
    CODE_DIRECTORY="src"
else
    CODE_DIRECTORY="lib"
fi

ACTION="$1"
if [ "$ACTION" == "" ]; then
    ACTION="run"
fi

if [ -f $CODE_DIRECTORY/$1.py ]; then
    ACTION="run"
    CODE="$1"
fi

if [ "$ACTION" == "run" ]; then
    .python/bin/python3 $CODE_DIRECTORY/$CODE.py "${@:2}"
fi
