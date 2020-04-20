from cassandra.cluster import Cluster

class CassandraRepository():
    """ Cassandra Repository """

    def __init__(self, url, keyspace):
        self.cassandra = Cluster([url])
        self.session = self.cassandra.connect(keyspace)


    def read(self, columns: str, table: str):
        """ reads from Cassandra Table"""
        rows = self.session.execute('select {} from jaeger_v1_datacenter3.{};'.format(columns, table))
        return rows


    def write(self, columns: str, table: str):
        pass

