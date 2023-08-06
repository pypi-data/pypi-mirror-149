#!/usr/bin/python3
import os,sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from datetime import datetime, timedelta
import pandas as pd
from sys import argv
from sf_virtual_data.virtual_sfv import solar_focus_sfv_lib as sofoc
from sf_virtual_data.virtual_sfv.virtual_sfv_runner import VirtualSfvRunner
from sf_virtual_data.common.api import virtual_sfv_pb2
from sf_virtual_data.common.api import solar_field_common_pb2

def main(cmd_line_args=argv[1:]) -> pd.DataFrame:
    vtCommandLineArgs, query_time_utc, margin = sofoc.parse_input(cmd_line_args)
    vt = VirtualSfvRunner(vtCommandLineArgs.metadata_file)
    res = vt.execute(vtCommandLineArgs, query_time_utc, margin)
    if not vtCommandLineArgs.debug:
        with open(vtCommandLineArgs.output_filename, 'wb') as bin_file:
            bin_text = res.SerializeToString()
            bin_file.write(bin_text)
    return res


if __name__ == "__main__":
    """
    Example of script run:  python virtual_sfv_entry_point.py --query_time_utc "2020-10-07 02:00:00" --margin "00:01:00" --debug --api-access-key "<your_api_access_key>"
    or run with IDE run-time args  ["--query_time_utc","2020-10-07 02:00:00", "--margin", "00:01:00", "--debug", "--api-access-key", "<your_api_access_key>"]

    """
    main()
