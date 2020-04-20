import subprocess
import re
from prometheus_client import Gauge, push_to_gateway

class Service():
    svc_name: str
    svc_count: int
    needed_replicas: int
    prometheus_gauge: Gauge
    namespace: str

    def __init__(self, svc_name, svc_count, namespace):
        self.svc_name = svc_name
        self.svc_count = svc_count
        self.namespace = namespace

    def apply(self, threshold):
        self.needed_replicas = -(-self.svc_count // threshold)
        print("Scaling {} to {} replicas...".format(self.svc_name, self.needed_replicas))
        # TODO: adapt path to bash script
        subprocess.Popen(["bash", "./scripts/kubectlscale.sh", self.namespace, self.svc_name, str(self.needed_replicas)])

    def push_to_prometheus(self, registry, url):
        try:
            self.prometheus_gauge = Gauge('scaling_{}'.format(re.sub(r'\W+', '', self.svc_name)), 'Last predicted amount of needed instanes of microservice {}'.format(self.svc_name), registry=registry)
        except:
            pass
        self.prometheus_gauge.set(self.needed_replicas)
        push_to_gateway('{}:9091'.format(url), job='prediction-maker', registry=registry)