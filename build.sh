#!/bin/bash

source version.properties

version=$version-$(date '+%Y%m%d%H%M')
echo Building neptune v$version...

rm -rf build
mkdir -p build/work/bin
mkdir -p build/work/lib
mkdir -p build/work/resources/telegraf
mkdir -p build/work/resources/kubernetes
mkdir -p build/work/resources/influxdb
mkdir -p build/work/resources/fluentd

#echo Compiling code...
#python3 -c "import compileall; compileall.compile_dir('src')" | grep !Listing

cp src/*.py build/work/lib
cp resources/shell/* build/work/bin
cp -R resources/telegraf build/work/resources/telegraf
cp -R resources/influxdb build/work/resources
cp -R resources/kubernetes build/work/resources

export version
envsubst < resources/kubernetes/agent.yaml > build/work/resources/kubernetes/agent.yaml
envsubst < resources/kubernetes/timeseries.yaml > build/work/resources/kubernetes/timeseries.yaml
chmod -R 755 build/work

echo Generating artifact...
tar -czf build/neptune-$version.tar.gz -C build/work .

echo Generating docker images...
docker build -t neptune-agent:$version -f resources/docker/agent.docker build/work
docker build -t neptune-timeseries:$version -f resources/docker/timeseries.docker build/work

echo Building neptune complete.
