#!/bin/sh

echo Building neptune...

rm -rf build
mkdir -p build/work/bin
mkdir -p build/work/lib

echo Compiling code...
python3 -c "import compileall; compileall.compile_dir('src')" | grep !Listing

cp src/*.pyc build/work/lib
cp resources/shell/* build/work/bin

echo Generating artifact...
tar -czf build/neptune-0.0.1.tar.gz -C build/work .

echo Building neptune complete.
