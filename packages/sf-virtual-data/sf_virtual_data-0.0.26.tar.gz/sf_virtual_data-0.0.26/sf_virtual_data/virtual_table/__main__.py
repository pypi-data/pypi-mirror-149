#!/usr/bin/python3
import os,sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from datetime import datetime, timedelta
import pandas as pd
from sys import argv
from sf_virtual_data.virtual_table import solar_focus_tables_lib as sofoc
from sf_virtual_data.virtual_table.virtual_tables_runner import VirtualTablesRunner
from sf_virtual_data.common.api import virtual_sfv_pb2
from sf_virtual_data.common.api import solar_field_common_pb2
import zipfile

def main(cmd_line_args=argv[1:]) -> pd.DataFrame:
    base_cmd_line_args, sfv_query_time_utc, sfv_margin, trends_start_utc, trends_end_utc = sofoc.parse_input(cmd_line_args)
    vt = VirtualTablesRunner( base_cmd_line_args.metadata_file)
    res = vt.execute(base_cmd_line_args, sfv_query_time_utc, sfv_margin, trends_start_utc, trends_end_utc)
    if not base_cmd_line_args.debug:
        with zipfile.ZipFile(base_cmd_line_args.output_filename, 'w') as myzip:
            for name, table in res.items():
                csv_name = name + ".csv"
                table.to_csv(csv_name)
                myzip.write(csv_name)
    return res


if __name__ == "__main__":
    """
    Example of script run:  python virtual_tables_entry_point.py --query_time_utc "2020-10-07 02:00:00" --margin "00:01:00" --debug --api-access-key "<your_api_access_key>"
    or run with IDE run-time args  ["--query_time_utc","2020-10-07 02:00:00", "--margin", "00:01:00", "--debug", "--api-access-key", "<your_api_access_key>"]

    """
    main()
