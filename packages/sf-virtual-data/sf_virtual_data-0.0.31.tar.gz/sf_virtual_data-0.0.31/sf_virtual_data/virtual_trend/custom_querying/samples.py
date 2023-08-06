#!/usr/bin/python3
import pandas as pd
from datetime import datetime, timedelta

def calculate(data: pd.DataFrame, start_utc: datetime, end_utc: datetime) -> pd.DataFrame:
    """
    User main code to calculate new virtual trends based on other trends

    Parameters
    ----------
    data: pd.DataFrame
        pandas DataFrame. columns are based on define_inputs()

    Returns
    -------
        pd.DataFrame
        pandas DataFrame. column must match the defined output as implemented in define_outputs() function
    """

    ################# User Code #########################

    # This returns output for 1 tag "HlstShortStatus.currentState" from Mongo collection
    res = read_from_mongo(start_utc, end_utc, timedelta(minutes= 5), "HlstShortStatus.currentState")

    # This returns output for 1 tag "OkCount" from Sql Server (CALS table)
    res = read_from_sql_server(start_utc, end_utc)

    ################# End of User Code ###################
    return res


def read_from_sql_server(start_utc: datetime, end_etc: datetime) -> pd.DataFrame:
    from .sql_reader import SqlReader
    date_format_to_sql_server = "%Y-%m-%d"
    query = '''SELECT T.MeasureTime  , Count(*) as OkCount FROM
                (SELECT heliostatId ,CONVERT(varchar, MeasureTime, 103) as MeasureTime
                FROM [NoorPA_SfincsData].[CMS_CALS].[Measurements]
                WHERE Status = 0
                and MeasureTime BETWEEN '{0}' AND '{1}'
                GROUP BY heliostatId , MeasureTime) T
            GROUP BY T.MeasureTime
            ORDER BY T.MeasureTime DESC
    '''.format(start_utc.strftime(date_format_to_sql_server), end_etc.strftime(date_format_to_sql_server))

    reader = SqlReader(SqlReader.create_sql_server_trusted_connection_string("site-sql-data", "NoorPA_SfincsData"))
    date_format_from_sql_server = "%d/%m/%Y"
    df = reader.get_df_from_db(query, "MeasureTime", date_format=date_format_from_sql_server)
    return df


def read_from_mongo(start_utc: datetime, end_utc: datetime, interval: timedelta, collection_name: str):
    from .mongo_reader import MongoReader
    reader = MongoReader("ConnectionString")
    query_start_time = start_utc
    ret = pd.DataFrame(columns=[collection_name])
    while (query_start_time < end_utc):
        query_end_time = query_start_time + interval
        if (query_end_time > end_utc):
            query_end_time = end_utc
        print("getting collections between {0} and {1}".format(query_start_time, {query_end_time}))
        df = reader.get_document_as_series(collection_name,  {'_id': {'$gt': query_start_time, '$lt': query_end_time}}, [("_id", -1)], "_id", "Data")
        num_of_sleep = df[df["value"]==5].count()["value"]
        ret.loc[query_start_time] = num_of_sleep
        query_start_time = query_start_time + interval
    return ret
