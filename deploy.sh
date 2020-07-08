#!/bin/bash

source version.properties
version=$version-$(date '+%Y%m%d%H%M')

./build.sh

echo Deploying neptune...
echo Deploying neptune-agent into minikube...
minikube cache add neptune-agent:$version
kubectl apply -f build/work/resources/kubernetes/agent.yaml

echo Deploying neptune-timeseries into minikube...
minikube cache add neptune-timeseries:$version
kubectl apply -f build/work/resources/kubernetes/timeseries.yaml
