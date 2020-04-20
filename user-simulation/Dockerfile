FROM python:3.7

RUN pip install locustio faker

ADD locustfile.py /config/locustfile.py

ENV LOCUST_FILE /config/locustfile.py

EXPOSE 8089

ENTRYPOINT ["locust --host http://istio-ingressgateway.istio-system.svc.cluster.local -f /config/locustfile.py --clients 50 --hatch-rate 5 --no-web"]