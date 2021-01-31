#!/bin/bash

if [ ! -d ".python" ]; then
    echo "Setting up environment..."
    apt install -y python3 python3-venv
    python3 -m venv .python
    chmod -R 755 .python
    .python/bin/activate
    .python/bin/pip3 install flask kubernetes influxdb_client deepdiff pyArango pandas tornado streamz
fi

.python/bin/activate

if [ -d "agent/src" ]; then
    CODE_DIRECTORY="src"
else
    CODE_DIRECTORY="lib"
fi

SERVICE="$1"
if [ "$SERVICE" == "" ]; then
    SERVICE="agent"
fi

ACTION="$2"
if [ "$ACTION" == "" ]; then
    ACTION="run"
fi

if [ -f $SERVICE/$CODE_DIRECTORY/$SERVICE.py ]; then
    ACTION="run"
fi

if [ "$ACTION" == "run" ]; then
    cd $SERVICE
    ../.python/bin/python3 $CODE_DIRECTORY/$SERVICE.py "${@:2}"
    cd ..
fi
