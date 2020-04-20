#!/bin/bash
cd "$(dirname "$0")"
kubectl create ns strimzi
kubectl create ns kafka
kubectl apply -f kafka
kubectl create ns mongodb
kubectl apply -f mongodb
jaeger/operator/apply.sh
kubectl create ns istio-system
kubectl apply -f istio/kiali-secret.yml
istio/installwotracing.sh