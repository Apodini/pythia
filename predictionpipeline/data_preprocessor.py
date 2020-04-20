import os
import pandas as pd
import numpy as np
from sklearn import preprocessing
from repositories.cassandra import CassandraRepository

class DataPreprocessor():
    def __init__(self):
        url = os.getenv('CASSANDRA_URL')
        self.cassandra = CassandraRepository(url=url, keyspace='jaeger_v1_datacenter3')
        self.le = preprocessing.LabelEncoder()
        self.le.classes_ = np.load('./classifiers/svcsequenceclasses.npy', allow_pickle=True)
    
    def get_data(self):
        df = pd.DataFrame(columns=['traceid', 'sessionid', 'servicessequence', 'starttime'])

        # get tracing data from Cassandra from tracesshort
        # pycassandra
        def pandas_factory(colnames, rows):
            return pd.DataFrame(rows, columns=colnames)

        self.cassandra.session.row_factory = pandas_factory
        self.cassandra.session.default_fetch_size = None

        rslt = self.cassandra.read(table='tracesshort', columns='traceid, sessionid, servicessequence, starttime')
        df = rslt._current_rows
        return df

    def preprocess_data(self, df):
        df = df.drop_duplicates()
        # apply data preprocessing, determine cluster of each request
        df['servicessequence'] = df['servicessequence'].apply(lambda x: str(x).split(','))
        # no duplicates in svcsequence or no consecutive elements
        # df['servicessequence'] = df['servicessequence'].apply(lambda x: [k for k,_g in groupby(x)])
        df['servicessequence'] = df['servicessequence'].apply(lambda x: list(dict.fromkeys(x)))
        seperator = ','
        df['servicessequence'] = df['servicessequence'].apply(lambda x: seperator.join(x))
        # TODO: handling unkown labels
        df = df[df.servicessequence != 'front-end,orders,carts,user,payment']
        df['currentclusternumber'] = self.le.transform(df['servicessequence'])

        return df
