import os
from itertools import groupby
import pandas as pd
import numpy as np
from sklearn import preprocessing

from repositories.cassandra import CassandraRepository

class DataPreprocessor():
    ''' Responsible for retrieving and preprocessing the tracing data
    '''
    def __init__(self):
        ''' init Cassandra Repository and Label Encoder
        '''
        url = os.getenv('CASSANDRA_URL')
        self.cassandra = CassandraRepository(url=url, keyspace='jaeger_v1_datacenter3')
        self.le = preprocessing.LabelEncoder()
        self.le2 = preprocessing.LabelEncoder()

    def get_data(self):
        ''' get data from Cassandra Table Traceslong
        '''
        # pycassandra
        def pandas_factory(colnames, rows):
            return pd.DataFrame(rows, columns=colnames)

        self.cassandra.session.row_factory = pandas_factory
        self.cassandra.session.default_fetch_size = None

        # read from Cassandra table traceslong and write to pandas df
        rslt = self.cassandra.read(table='traceslong', columns='traceid, sessionid, servicessequence, starttime')
        df = rslt._current_rows
        return df

    def preprocess_data(self, df):
        ''' Preprocess data returning a pandas dataframe
        '''
        df = df.drop_duplicates()
        df = df[pd.notnull(df['sessionid'])]

        # encode services sequence to cluster
        df['servicessequence'] = df['servicessequence'].apply(lambda x: str(x).split(','))
        # no duplicates in svcsequence or no consecutive elements
        # df['servicessequence'] = df['servicessequence'].apply(lambda x: [k for k,_g in groupby(x)])
        df['servicessequence'] = df['servicessequence'].apply(lambda x: list(dict.fromkeys(x)))
        seperator = ','
        df['servicessequence'] = df['servicessequence'].apply(lambda x: seperator.join(x))
        df['currentclusternumber'] = self.le.fit_transform(df['servicessequence'])

        # get correct sessionid
        # TODO: fix some cookies don't get parsed correctly!
        df.loc[:, 'sessionid'] = df['sessionid'].apply(lambda x: str(x).split('=s%3A')[1].split(';')[0].split('.')[0] if 'md.sid' in x else x)

        # init full_df for storing all rows after preprocessing
        full_df = pd.DataFrame(columns=['sessionid', 'nextcluster', 'starttime'])

        # group by sessionid and determine nextcluster and clustersequence
        grouped_df = df.sort_values('starttime').groupby('sessionid')
        i = 0
        for k, v in grouped_df:
            # nextcluster is currentclusternumber of next trace
            v.loc[:, 'nextcluster'] = v.currentclusternumber.shift(-1, fill_value=0)
            v = v.reset_index()
            v['clustersequence'] = ''

            # this solution considers not only currentcluster to predict next, but also previous clusters (but without same cluster repetitively)
            currentclusterlist = list(v['currentclusternumber'].values)
            nextclusterlist = []
            seperator = ","

            for i in range(len(v)):
                nextclusterlist.append(str(currentclusterlist[i]))
                nextclusterlist = [x[0] for x in groupby(nextclusterlist)]
                # only consider last n elements
                nextclusterlist = nextclusterlist[-6:]
                # next_cluster_list = next_cluster_list[:(len(next_cluster_list)-1)]
                nextclusterstr = seperator.join(nextclusterlist)
                v.at[i, 'clustersequence'] = nextclusterstr
            # print(v[["sessionid","starttime", "currentclusternumber", "servicessequence", "clustersequence", "nextcluster"]].head(50))

            # add preprocessed grouped df to full_df
            full_df = full_df.append(v, ignore_index=True)
            i += 1

        if full_df.empty == False:
            # full_df = full_df.drop(['traceid'], axis=1)
            full_df.currentclusternumber = full_df.currentclusternumber.astype(int)
            full_df = full_df[full_df.sessionid != '']
            print(full_df.head())

            # encode clustersequence
            # print(full_df.clustersequence)
            full_df['clustersequence'] = self.le2.fit_transform(full_df['clustersequence'])
            np.save('./classifiers/clustersequenceclasses.npy', self.le2.classes_)
            # print(clustersequenceclasses)

        return full_df