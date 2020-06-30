#!/bin/sh

echo Building neptune...

rm -rf build
mkdir -p build/work/bin
mkdir -p build/work/lib
mkdir -p build/work/resources/telegraf

#echo Compiling code...
#python3 -c "import compileall; compileall.compile_dir('src')" | grep !Listing

cp src/*.py build/work/lib
cp resources/shell/* build/work/bin
cp -R resources/telegraf build/work/resources/telegraf
chmod -R 755 build/work

echo Generating artifact...
tar -czf build/neptune-0.0.1.tar.gz -C build/work .

echo Generating docker images...
docker build -t neptune-agent -f resources/docker/agent.docker build/work

echo Building neptune complete.
