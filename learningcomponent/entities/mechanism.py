import pickle
import numpy as np

from repositories.cassandra import CassandraRepository

class Mechansim():
    ''' Entitiy object that is to be stored in the Cassandra Table Mechansim
    '''

    def __init__(self, clf, encoder, timestamp):
        self.clf = clf
        self.encoder = encoder
        self.timestamp = timestamp
    
    def save(self):
        # TODO: save to cassandra
        filename = './classifiers/dt_clf.sav'
        pickle.dump(self.clf, open(filename, 'wb'))
        # pickle.load(open('./classifiers/dt_clf.sav', 'rb'))))
        np.save('./classifiers/svcsequenceclasses.npy', self.encoder.classes_)
