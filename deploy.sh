#!/bin/bash

source version.properties
version=$version-$(date '+%Y%m%d%H%M')

./build.sh

echo Deploying neptune...
echo Deploying neptune-agent into minikube...
#minikube cache add neptune-agent:$version
#kubectl apply -f build/work/agent/resources/kubernetes/agent.yaml

echo Deploying neptune-timeseries into minikube...
minikube cache add neptune-timeseries:$version
kubectl apply -f build/work/timeseries/resources/kubernetes/timeseries.yaml

echo Deploying neptune-inventory into minikube...
kubectl apply -f build/work/inventory/resources/kubernetes/inventory.yaml

echo Waiting for services to start...
while [ `kubectl get pods | grep 1/1 | wc -l` -ne 2 ]; do
    sleep 10
done

echo Launching browser...
minikube service neptune-timeseries
