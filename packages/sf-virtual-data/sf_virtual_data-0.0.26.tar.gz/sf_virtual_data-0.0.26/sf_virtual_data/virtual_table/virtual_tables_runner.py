#!/usr/bin/python3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from sf_virtual_data import virtual_sfv
from . import solar_focus_tables_lib as sofoc
from sf_virtual_data.common.models import VTCommandLineArgsBase
from sf_virtual_data.common.api import virtual_tables_pb2
from sf_virtual_data.common.api import solar_field_pb2
from sf_virtual_data.common.api import solar_field_common_pb2
from sf_virtual_data.common.api import virtual_sfv_pb2
from sf_virtual_data.common.api import virtual_trends_pb2
from sf_virtual_data.common.api import common_models_pb2
from virtual_sfv import solar_focus_sfv_lib as virtual_sfv_lib
from virtual_trend import solar_focus_trends_lib as virtual_trends_lib
import google.protobuf.json_format as json_format
from google.protobuf import wrappers_pb2
from user_calculation import calculate as user_calc
import pandas as pd
from math import isnan
from google.protobuf import struct_pb2
from typing import Dict, List

class VirtualTablesRunner(ABC):
    def __init__(self, metadata_file: str):
        self.metadata = self.get_metadata(metadata_file)

    def get_metadata(self, metadata_file: str) -> virtual_tables_pb2.VirtualTablesModule:
        import os
        cwd = os.getcwd()
        metadata_file_path = os.path.join(cwd,metadata_file)
        with open(metadata_file_path, 'r', encoding='utf-8') as f:
            message = virtual_tables_pb2.VirtualTablesModule()
            json_format.Parse(f.read(), message)
            return message

    def build_query(self, sfv_query_time_utc: datetime, sfv_margin: timedelta, trends_start_utc: datetime, trends_end_utc: datetime) -> virtual_tables_pb2.VirtualTablesQuery:
        sfv_query = virtual_sfv_lib.build_query(sfv_query_time_utc, sfv_margin,self.metadata.input_sfv_tags, self.metadata.sfv_calculation_method)
        trends_query = virtual_trends_lib.build_query(trends_start_utc, trends_end_utc,self.metadata.input_trends, self.metadata.trends_calculation_method, self.metadata.sample_frequency)
        res = virtual_tables_pb2.VirtualTablesQuery(sfv_query = sfv_query, trends_query = trends_query)
        return res

    def calculate(self, sfv_query_time_utc: datetime, sfv_margin: timedelta, trends_start_utc: datetime, trends_end_utc: datetime, inputs_from_solar_focus: virtual_tables_pb2.VirtualTablesInputsResult = None) -> Dict[str, pd.DataFrame]:
        if inputs_from_solar_focus is None:
            res = user_calc(sfv_query_time_utc = sfv_query_time_utc, sfv_margin = sfv_margin, trends_start_utc = trends_start_utc, trends_end_utc = trends_end_utc)
        else:
            input_sfv_df = virtual_sfv_lib.solar_field_to_df(self.metadata.input_sfv_tags, inputs_from_solar_focus.sfv)
            input_trends_df = virtual_trends_lib.convert_trends_res_to_df(self.metadata.input_trends, inputs_from_solar_focus.trends)
            res = user_calc(sfv_query_time_utc = sfv_query_time_utc, sfv_margin = sfv_margin, trends_start_utc = trends_start_utc, trends_end_utc = trends_end_utc, trends_inputs_from_solar_focus = input_trends_df, sfv_inputs_from_solar_focus = input_sfv_df)
        self.validate_res(res)
        return res

    def validate_res(self, res: Dict[str, pd.DataFrame]):
        """
        Verify that result of this virtual sfv match the defines outputs
        """
        if len(res) != len(self.metadata.output_tables):
            raise Exception(f"Output result does not match output tags size")

        for output_md in self.metadata.output_tables:
            if (output_md.name not in res.keys()):
                raise Exception(f"Output name does not match output md name")


    def execute(self, vtCommandLineArgs: VTCommandLineArgsBase, sfv_query_time_utc, sfv_margin, trends_start_utc, trends_end_utc) -> List[pd.DataFrame]:
        """
        This is the execution call for this VT calculation flow
        """
        query: virtual_tables_pb2.VirtualTablesQuery = self.build_query(sfv_query_time_utc, sfv_margin, trends_start_utc, trends_end_utc)
        sfv_tags_query: virtual_sfv_pb2.SfvQuery = query.sfv_query.sfv_tags_query
        if len(sfv_tags_query.tags_descriptions) > 0 or len(query.trends_query.trends_identifier) > 0:
            res: virtual_tables_pb2.VirtualTablesInputsResult = sofoc.get_data(query, vtCommandLineArgs)
            return self.calculate(sfv_query_time_utc = sfv_tags_query.query_time_utc.ToDatetime(), sfv_margin= sfv_tags_query.margin.ToTimedelta(), trends_start_utc = query.trends_query.start_date_utc.ToDatetime(), trends_end_utc = query.trends_query.end_date_utc.ToDatetime(), inputs_from_solar_focus = res)
        else:
            return self.calculate(sfv_query_time_utc = sfv_tags_query.query_time_utc.ToDatetime(), sfv_margin= sfv_tags_query.margin.ToTimedelta(), trends_start_utc = query.trends_query.start_date_utc.ToDatetime(), trends_end_utc = query.trends_query.end_date_utc.ToDatetime())
