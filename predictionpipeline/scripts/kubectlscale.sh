#!/bin/bash
# TODO: auth kubectl
kubectl scale -n $1 deployment/$2 --replicas=$3