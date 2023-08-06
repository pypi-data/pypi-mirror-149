import pymongo
import datetime
import pandas as pd

class MongoReader(object):
    def __init__(self, connection_string, db_name="Archive"):
        self.connection_string = connection_string
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def get_cursor_for_collection(self, collection_name, filter={}, projection=None, skip=0, limit=5000,
                                  sort=None, batch_size=100):
        collection = self.get_collection(collection_name)
        return collection.find(filter, limit=limit, skip=skip, sort=sort, batch_size=batch_size)

    def get_document(self, collection_name, filter, sort):
        cursor = self.get_cursor_for_collection(collection_name, filter, sort=sort)
        for doc in cursor.limit(1):
            return doc

    def get_document_as_series(self, collection_name, filter, sort, idx_field: str, data_field: str, header="value") -> pd.DataFrame:
        doc = self.get_document(collection_name, filter, sort)
        return self.__convert_doc_to_series(doc[data_field], header)

    def __convert_doc_to_series(self, doc, header="value") -> pd.DataFrame:
        series = pd.Series(doc)
        df = pd.DataFrame({'id': series.index, header: series.values})
        df.id = df.id.map(int)
        return df

