#!/usr/bin/python3
import os,sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np
import pandas as pd
import json
import math
from sys import argv
from sf_virtual_data.virtual_trend import solar_focus_trends_lib as sofoc
from sf_virtual_data.virtual_trend.virtual_trend_runner import VirtualTrendRunner
from sf_virtual_data.common.api import common_models_pb2
from sf_virtual_data.common.api import virtual_trends_pb2
from user_calculation import calculate as user_calc
from user_calculation import plot as user_plot

def main(cmd_line_args=argv[1:]) -> pd.DataFrame:
    base_cmd_line_args, start_utc, end_utc  = sofoc.parse_input(cmd_line_args)
    vt = VirtualTrendRunner(base_cmd_line_args.metadata_file)
    res = vt.execute(base_cmd_line_args, start_utc, end_utc)
    tagTimeSeriesData = vt.df_to_tag_time_series_data_arr(res)
    if not base_cmd_line_args.debug:
        with open(base_cmd_line_args.output_filename, 'wb') as bin_file:
            bin_text = tagTimeSeriesData.SerializeToString()
            bin_file.write(bin_text)
    else:
        user_plot(res)
        
    return res


if __name__ == "__main__":
    """
    Example of script run:  python virtual_trend_entry_point.py --start-utc "2020-10-07 02:00:00" --end-utc "2020-10-07 16:00:00" --debug --api-access-key "<your_api_access_key>"
    or run with IDE run-time args  ["--start-utc","2020-10-07 02:00:00", "--end-utc", "2020-10-07 16:00:00", "--debug", "--api-access-key", "<your_api_access_key>"]
    """
    main()
