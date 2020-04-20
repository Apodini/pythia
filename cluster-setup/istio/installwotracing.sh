#!/bin/bash
cd "$(dirname "$0")"
./istio-1.4.2/bin/istioctl manifest apply --set values.pilot.traceSampling=100 --set values.global.tracer.zipkin.address="jaeger-cassandra-collector.observability.svc.cluster.local:9411" --set values.kiali.enabled=true --set values.grafana.enabled=true
