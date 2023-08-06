#!/usr/bin/python3
import argparse
import json
import os
from sf_virtual_data.common.api import virtual_tables_pb2_grpc
from sf_virtual_data.common.api import virtual_tables_pb2
from sf_virtual_data.common.api import solar_field_common_pb2
from sf_virtual_data.common import utils
from sf_virtual_data.common import models
import grpc
from datetime import datetime, timedelta
from sf_virtual_data.common.models import VTCommandLineArgsBase
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
import pandas as pd

def get_data(query: virtual_tables_pb2.VirtualTablesQuery, args: models.VTCommandLineArgsBase) -> virtual_tables_pb2.VirtualTablesInputsResult:
    channel = utils.get_grpc_channel_according_to_args(args)
    client = virtual_tables_pb2_grpc.VirtualTablesGrpcServiceStub(channel)
    res = client.GetData(query, metadata=[('x-api-key', f'{args.api_access_key}')])
    return res




def parse_input(cmd_line_args) -> (models.VTCommandLineArgsBase, datetime, timedelta, datetime, datetime):
    (base_cmd_line_args, extra_args) = utils.parse_input(cmd_line_args)
    parser = argparse.ArgumentParser(
        description='Input parameters to run virtual tables')
    parser.add_argument('--sfv-query-time-utc', action='store', required='--metadata' not in cmd_line_args,
                        dest='sfv_query_time_utc',
                        help='The sfv query time in UTC, format YYYY-MM-DD hh:mm:ss')
    parser.add_argument('--sfv-margin', action='store', required='--metadata' not in cmd_line_args,
                        dest='sfv_margin',
                        help='The sfv query margin time of the query in UTC, format hh:mm:ss')
    parser.add_argument('--trends-start-utc', action='store', required='--metadata' not in cmd_line_args,
                        dest='trends_start_utc',
                        help='Start time of the trends query in UTC, format YYYY-MM-DD hh:mm:ss')
    parser.add_argument('--trends-end-utc', action='store', required='--metadata' not in cmd_line_args,
                        dest='trends_end_utc',
                        help='End time of the trends query in UTC, format YYYY-MM-DD hh:mm:ss')
    args = parser.parse_args(extra_args)
    if args.sfv_query_time_utc is not None and args.sfv_margin is not None:
        sfv_query_time_utc = datetime.strptime(args.sfv_query_time_utc, TIME_FORMAT)
        sfv_margin = utils.parse_time(args.sfv_margin)
    else:
        query_time_utc = None
        margin = None
    if args.trends_start_utc is not None and args.trends_end_utc is not None:
        trends_start_utc = datetime.strptime(args.trends_start_utc, TIME_FORMAT)
        trends_end_utc = datetime.strptime(args.trends_end_utc, TIME_FORMAT)
    else:
        trends_start_utc = None
        trends_end_utc = None
    return base_cmd_line_args, sfv_query_time_utc, sfv_margin, trends_start_utc, trends_end_utc
