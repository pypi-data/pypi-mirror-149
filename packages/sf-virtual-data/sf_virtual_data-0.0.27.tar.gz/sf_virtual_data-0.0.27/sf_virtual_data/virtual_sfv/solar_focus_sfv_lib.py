#!/usr/bin/python3
import argparse
import json
import os

from google.protobuf.timestamp_pb2 import Timestamp
from common.api import virtual_sfv_pb2_grpc
from common.api import virtual_sfv_pb2
from common.api import solar_field_common_pb2
from common.api import common_models_pb2
from common import utils
import grpc
from datetime import datetime, timedelta
from common.models import VTCommandLineArgsBase
from sf_virtual_data.common.api.virtual_trends_pb2 import NONE
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
import pandas as pd
from google.protobuf import wrappers_pb2
import google.protobuf.json_format as json_format
from virtual_trend import solar_focus_trends_lib as virtual_trends_lib
from common.api import virtual_trends_pb2
from google.protobuf import duration_pb2

from typing import List


def build_query(query_time_utc: datetime, margin: timedelta, defined_inputs: List[common_models_pb2.VirtualModuleInputTag],  calculation_method: solar_field_common_pb2.SfvCalculationMethod) -> virtual_sfv_pb2.VirtualSfvInputsQuery:
    res = virtual_sfv_pb2.VirtualSfvInputsQuery()
    sfv_query = virtual_sfv_pb2.SfvQuery(calculation_method=calculation_method)
    data_points_inputs =[]
    for input in defined_inputs:
        if input.raw_id.tag_type == common_models_pb2.NUMERIC_PER_SFO:
            new_id = common_models_pb2.TagsIdentifierBase()
            new_id.tag_type = common_models_pb2.NUMERIC
            new_id.tag_identifier.CopyFrom(common_models_pb2.TagIdentifier(id = input.raw_id.sfo_tag_identifier.tag_id))
            sfv_query.tags_descriptions.append(new_id)
        else:
            data_points_inputs.append(input)
    sfv_query.query_time_utc.FromDatetime(query_time_utc)
    sfv_query.margin.FromTimedelta(margin)
    res.sfv_tags_query.CopyFrom(sfv_query)
    data_points_query = virtual_trends_lib.build_query( query_time_utc - margin, query_time_utc + margin, data_points_inputs, NONE, duration_pb2.Duration())
    res.data_points_inputs.CopyFrom(data_points_query)
    return res

def get_data(query: virtual_sfv_pb2.VirtualSfvInputsQuery, args: VTCommandLineArgsBase) -> virtual_sfv_pb2.VirtualSfvInputsResult:
    channel = utils.get_grpc_channel_according_to_args(args)
    client = virtual_sfv_pb2_grpc.VirtualSfvGrpcServiceStub(channel)
    res = client.GetData(query, metadata=[('x-api-key', f'{args.api_access_key}')])
    problematics = res.sfv_tags.problematic_tags
    if len(problematics) > 0:
        raise Exception(f"Didn't get data for {len(problematics)} tags, reasons: {problematics}")
    return res


def proto_float_to_number(float_value:wrappers_pb2.FloatValue) -> float:
    return float_value.value

def solar_field_to_df(defined_inputs: List[common_models_pb2.VirtualModuleInputTag], sf_dto: solar_field_common_pb2.SolarFieldDto = None) -> pd.DataFrame:
    res: pd.DataFrame = pd.DataFrame()
    if len(defined_inputs) == 0:
        return res
    problematics = sf_dto.problematic_tags
    if len(problematics) > 0:
        raise Exception(
            f"Didn't get data for {len(problematics)} tags, reasons: {json_format.MessageToJson(sf_dto)}")
    if (sf_dto == None):
        return res
    for tag_data in sf_dto.data:
        tag_variable = ""
        for input_tag in defined_inputs:
            if input_tag.raw_id.tag_identifier.id == tag_data.tag_id.tag_identifier.id:
                tag_variable = input_tag.variable_name
                break
        values_list = []
        for float_nullable_value in enumerate(tag_data.nullable_data):
            values_list.append(float_nullable_value[1])
        res[tag_variable] = values_list
        res[tag_variable] = res[tag_variable].apply(proto_float_to_number)
    return res

def plot_series(series: pd.Series, helio_radius=0.05, color_map: str = 'turbo'):
    # Get layout and shift
    layout_df = pd.read_csv("HeliostatsLayout.csv").set_index("Id")
    import matplotlib.pyplot as plt
    rdf = pd.Series([0 for i in range(layout_df.index.size)])
    for idx, item in enumerate(series):
        rdf[idx] = item
    im = plt.scatter(x =layout_df["E"], y = layout_df["N"],c=rdf,s = helio_radius,  cmap=plt.cm.get_cmap(color_map, 255))
    plt.colorbar(im)
    plt.show()

def solar_field_to_update_time(defined_inputs: List[common_models_pb2.VirtualModuleInputTag], sf_dto: solar_field_common_pb2.SolarFieldDto = None) -> pd.DataFrame:
    res: pd.DataFrame = pd.DataFrame()
    if len(defined_inputs) == 0:
        return res
    problematics = sf_dto.problematic_tags
    if len(problematics) > 0:
        raise Exception(
            f"Didn't get data for {len(problematics)} tags, reasons: {json_format.MessageToJson(sf_dto)}")
    if (sf_dto == None):
        return res
    times = []
    for tag_data in sf_dto.data:
        tag_variable = ""
        for input_tag in defined_inputs:
            if input_tag.raw_id == tag_data.tag_id:
                tag_variable = input_tag.variable_name
                break
        times.append(tag_data.update_time.ToMilliseconds())
    res[tag_variable] = times
    return res


def parse_input(cmd_line_args) -> VTCommandLineArgsBase:
    (base_cmd_line_args, extra_args) = utils.parse_input(cmd_line_args)
    parser = argparse.ArgumentParser(
        description='Input parameters to run virtual sfv')
    parser.add_argument('--query_time_utc', action='store', required='--metadata' not in cmd_line_args,
                        dest='query_time_utc',
                        help='The query time in UTC, format YYYY-MM-DD hh:mm:ss')
    parser.add_argument('--margin', action='store', required='--metadata' not in cmd_line_args,
                        dest='margin',
                        help='The margin time of the query in UTC, format hh:mm:ss')
    args = parser.parse_args(extra_args)
    if args.query_time_utc is not None and args.margin is not None:
        query_time_utc = datetime.strptime(args.query_time_utc, TIME_FORMAT)
        margin = utils.parse_time(args.margin)
    else:
        query_time_utc = None
        margin = None
    return (base_cmd_line_args, query_time_utc, margin)
