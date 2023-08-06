
#!/usr/bin/python3
import argparse
import json
import sys
import os
from common.models import VTCommandLineArgsBase
from common.api import virtual_trends_pb2_grpc
from common.api import virtual_trends_pb2
from common.api import common_models_pb2
from common import utils
from common import models
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
import grpc
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta
from google.protobuf.json_format import MessageToJson

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def build_query(start_utc: datetime,
                end_utc: datetime,
                defined_inputs: List[common_models_pb2.VirtualModuleInputTag],
                calculation_method: virtual_trends_pb2.CalculationMethod,
                sample_frequency:google_dot_protobuf_dot_duration__pb2.Duration ) -> virtual_trends_pb2.TimeSeriesQueryInput:
    res = virtual_trends_pb2.TimeSeriesQueryInput( calculation_method=calculation_method, sample_frequency=sample_frequency)
    for input in defined_inputs:
        res.trends_identifier.append(input.raw_id)
    if end_utc < start_utc:
        raise Exception("Query params error: end time - {0} is smaller than start time - {1}".format(end_utc, start_utc))
    res.start_date_utc.FromDatetime(start_utc)
    res.end_date_utc.FromDatetime(end_utc)
    return res

def get_data(defined_inputs: List[common_models_pb2.VirtualModuleInputTag], query: virtual_trends_pb2.TimeSeriesQueryInput, args: VTCommandLineArgsBase) -> pd.DataFrame:
    channel = utils.get_grpc_channel_according_to_args(args)
    client = virtual_trends_pb2_grpc.VirtualTrendsGrpcServiceStub(channel)
    res = client.GetData(query, metadata=[('x-api-key', f'{args.api_access_key}')])
    return convert_trends_res_to_df(defined_inputs, res)

def convert_trends_res_to_df(defined_inputs: List[common_models_pb2.VirtualModuleInputTag], trends_res: virtual_trends_pb2.TimeSeriesQueryResult) -> pd.DataFrame:
    problematics = trends_res.problematic_tags
    if len(defined_inputs) == 0:
        return pd.DataFrame()
    if len(problematics) > 0:
        raise Exception(
            f"Didn't get data for {len(problematics)} tags, reasons: {problematics}")
    df = pd.concat(map(lambda x: convert_sf_series_to_pandas(x.time_series), trends_res.results), axis=1, keys=map(
        lambda x: x.trend_id.SerializeToString(), trends_res.results))
    df = df.rename(lambda i: next(
            x for x in defined_inputs if x.raw_id.SerializeToString() == i).variable_name, axis='columns')
    return df


def convert_sf_series_to_pandas(data: List) -> pd.Series:
    index = pd.DatetimeIndex([x.time.ToDatetime() for x in data])
    vals = [x.value for x in data]
    return pd.Series(vals, index=index)

def plot(df: pd.DataFrame):
     import matplotlib.pyplot as plt
     df.plot()
     plt.legend(loc='best')
     plt.pause(60)

def parse_input(cmd_line_args) -> (VTCommandLineArgsBase, datetime, datetime ):
    (base_cmd_line_args, extra_args) = utils.parse_input(cmd_line_args)
    parser = argparse.ArgumentParser(
        description='Input parameters to run virtual trend')
    parser.add_argument('--start-utc', action='store', required='--metadata' not in cmd_line_args,
                        dest='start',
                        help='Start time of the query in UTC, format YYYY-MM-DD hh:mm:ss')
    parser.add_argument('--end-utc', action='store', required='--metadata' not in cmd_line_args,
                        dest='end',
                        help='End time of the query in UTC, format YYYY-MM-DD hh:mm:ss')
    args = parser.parse_args(extra_args)
    if args.start is not None and args.end is not None:
        start_utc = datetime.strptime(args.start, TIME_FORMAT)
        end_utc = datetime.strptime(args.end, TIME_FORMAT)
    else:
        start_utc = None
        end_utc = None
    return base_cmd_line_args,start_utc, end_utc
