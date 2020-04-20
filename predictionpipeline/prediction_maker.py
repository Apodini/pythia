import pickle
import numpy as np
from sklearn import preprocessing

class PredictionMaker():
    
    def __init__(self):
        # load tree/model and clusters from learning subsystem at the start of pipeline?
        # TODO: get from cassandra instead of files!
        self.model = pickle.load(open('./classifiers/dt_clf.sav', 'rb'))

        # load prefitted labelencoder
        self.le = preprocessing.LabelEncoder()
        self.le.classes_ = np.load('./classifiers/svcsequenceclasses.npy', allow_pickle=True)

    def make_prediction(self, df):
        result = self.model.predict(df[['currentclusternumber']].values)
        result_svc = list(self.le.inverse_transform(result))
        return result_svc
