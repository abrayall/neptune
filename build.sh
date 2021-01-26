#!/bin/bash

source version.properties

version=$version-$(date '+%Y%m%d%H%M')
export version
echo Building neptune v$version...

rm -rf build

#echo Compiling code...
#python3 -c "import compileall; compileall.compile_dir('src')" | grep !Listing

services="agent timeseries inventory ui"
for service in $services
do
    mkdir -p build/work/$service/lib
    mkdir -p build/work/$service/bin
    mkdir -p build/work/$service/resources/kubernetes
    cp $service/src/*.py build/work/$service/lib 2>/dev/null
    cp $service/resources/shell/* build/work/$service/bin 2>/dev/null
    cp -r $service/resources/* build/work/$service/resources 2>/dev/null
    rm -rf build/work/$service/shell
    if [ -f $service/resources/kubernetes/$service.yaml ]; then
        envsubst < $service/resources/kubernetes/$service.yaml > build/work/$service/resources/kubernetes/$service.yaml
    fi
done

chmod -R 755 build/work

echo Generating artifact...
tar -czf build/neptune-$version.tar.gz -C build/work .

echo Generating docker images...
for service in $services
do
    if [ -f $service/resources/docker/$service.docker ]; then
        docker build -t neptune-$service:$version -f $service/resources/docker/$service.docker build/work/$service
    fi
done

echo Building neptune complete.
