import pyodbc
import pandas as pd


class SqlReader:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def create_connection(self):
        return pyodbc.connect(self.connection_string)

    def get_df_from_db(self, query: str, sfo_column: str, date_format="%d/%m/%Y"):
        conn = self.create_connection()
        df = pd.read_sql(query, conn)
        # set date column as index column
        df.set_index(sfo_column, inplace=True)
        return df

    @staticmethod
    def create_sql_server_trusted_connection_string(server: str, db_name: str):
        return "Driver=SQL Server Native Client 11.0;Server={0};Database={1};Trusted_Connection=yes;".format(server, db_name)    
    @staticmethod
    def create_sql_server_connection_string(server: str, db_name: str, username: str, password: str):
        return "DRIVER=ODBC Driver 17 for SQL Server;SERVER={0};DATABASE={1};UID={2};PWD={3};".format(server, db_name, username, password)