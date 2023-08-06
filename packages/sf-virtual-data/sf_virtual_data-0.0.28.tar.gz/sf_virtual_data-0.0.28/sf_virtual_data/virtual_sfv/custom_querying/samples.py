#!/usr/bin/python3
import pandas as pd
from datetime import datetime, timedelta

def calculate(data: pd.DataFrame, start_utc: datetime, end_utc: datetime) -> pd.DataFrame:
    """
    User main code to calculate new virtual sfv based on other sfv's

    Parameters
    ---------
        pandas DataFrame. columns are based on define_inputs()

    Returns
    -------
        pd.DataFrame
        pandas DataFrame. column must match the defined output as implemented in define_outputs(value_column   """

    ################# User Code #########################

    # This returns value_column tag "HlstShortStatus.currentState" from Mongo collection
    # res = samples.read_from_mongo_closest_time(query_time_utc, margin,"_id","Data", "HlstShortStatus.currentState")

    # This returns output for 1 tag "AverageDnrWattPerSquareMetre" from Sql Server (CALS table)
    res = read_from_sql_server(start_utc, end_utc)

    ################# End of User Code ###################
    return res


def read_from_sql_server(query_time_utc: datetime, margin: timedelta) -> pd.DataFrame:
    from .sql_reader import SqlReader
    date_format_to_sql_server = "%Y-%m-%d"
    query = ''' SELECT * FROM (SELECT DISTINCT [HeliostatId], [AverageDnrWattPerSquareMetre], [MeasureTime], 
                    RANK() OVER (PARTITION BY [HeliostatId] ORDER BY MeasureTime DESC) dest_rank
                    FROM [NoorPA_SfincsData].[CMS_CALS].[Measurements]) T
	            where T.dest_rank = 1
    '''

    reader = SqlReader(SqlReader.create_sql_server_trusted_connection_string("site-sql-data", "NoorPA_SfincsData"))
    date_format_from_sql_server = "%d/%m/%Y"
    df = reader.get_df_from_db(query, "AverageDnrWattPerSquareMetre","HeliostatId", date_format=date_format_from_sql_server)
    return df


def read_from_mongo_closest_time(query_time_utc: datetime, margin: timedelta, timestamp_field:str, value_field:str, collection_name: str):
    from .mongo_reader import MongoReader
    reader = MongoReader("ConnectionString")
     # Make a query to the specific DB and Collection
    reader.get_collection(collection_name)
    pipeline = [{'$match' :{'{0}'.format(timestamp_field):{'$gte': query_time_utc-margin,'$lte': query_time_utc+margin}}},
                { '$addFields' : { 'distance': {'$abs': { '$subtract': [query_time_utc, '${0}'.format(timestamp_field)]}}}},
                { '$sort' : { 'distance' : 1 } },
                { '$limit' : 1 }
                ]  
    cursor = reader.get_collection(collection_name).aggregate(pipeline)
    # Expand the cursor and construct the DataFrame
    data = list(cursor)
    doc = data[0]
    df =  pd.DataFrame()
    df[value_field] = doc[value_field]
    return df