import time
import os
import pickle
import yaml
import subprocess
import pandas as pd
import numpy as np
from sklearn import preprocessing
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

from data_preprocessor import DataPreprocessor
from prediction_maker import PredictionMaker
from entities.prediction import Prediction

class PredictionPipeline():

    def __init__(self):
        # load config file
        with open("./config/predictionconfig.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.interval = cfg['interval']
        self.threshold = cfg['single_threshold']
        # init DataPreprocessor
        self.data_preprocessor = DataPreprocessor()
        # init PredictionMaker
        self.prediction_maker = PredictionMaker()
        self.registry = CollectorRegistry()
        self.pushgateway_url = os.getenv('PUSHGATEWAY_URL')
        

    def run(self):
        while True:
            start_millis = int(round(time.time() * 1000))
            print("Starting pipeline...")

            # get data
            df = self.data_preprocessor.get_data()
            df = self.data_preprocessor.preprocess_data(df)
            
            if df.empty == False:

                # predict
                result = self.prediction_maker.make_prediction(df)
                end_millis = int(round(time.time() * 1000))
                prediction_millis = end_millis - start_millis
                prediction = Prediction(result)

                # apply changes to K8s Cluster
                prediction.apply(self.threshold)

                # push to prometheus gateway
                prediction.push_to_prometheus(self.registry, self.pushgateway_url)
                try:
                    g = Gauge('prediction_making_speed', 'Time in ms for making Prediction.', registry=registry)
                except:
                    pass
                g.set(prediction_millis)
                push_to_gateway('{}:9091'.format(self.pushgateway_url), job='prediction-maker', registry=registry)
                # sleep until next interval
                print("Prediction took {} ms.".format(prediction_millis))

            print("Going back to sleep for {} sec...".format(self.interval))
            time.sleep(self.interval)

if __name__ == "__main__":
    prediction_pipeline = PredictionPipeline()
    prediction_pipeline.run()