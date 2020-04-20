import subprocess
import time
from entities.service import Service
from prediction_converter import PredictionConverterA

class Prediction():
    services: list
    timestamp: int

    def __init__(self, result):
        # TODO: self.model
        self.timestamp =  int(round(time.time() * 1000))
        self.converter = PredictionConverterA()
        self.services = self.converter.convert_prediction(result)

    def apply(self, threshold):
        for svc in self.services:
            svc.apply(threshold)

    def push_to_prometheus(self, registry, url):
        for svc in self.services:
            svc.push_to_prometheus(registry, url)
