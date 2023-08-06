#!/usr/bin/python3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np
import pandas as pd
import os
import types
import json
from . import solar_focus_trends_lib as sofoc
from common.models import VTCommandLineArgsBase
from common.api import virtual_trends_pb2
import google.protobuf.json_format as json_format
from common.api import common_models_pb2
from user_calculation import calculate as user_calc


class VirtualTrendRunner(ABC):
    def __init__(self, metadata_file: str):
        self.metadata = self.get_metadata(metadata_file)

    def calculate(self, start_date_utc: datetime, end_date_utc: datetime, inputs_from_solar_focus: pd.DataFrame = None) -> pd.DataFrame:
        res = user_calc(start_date_utc, end_date_utc, inputs_from_solar_focus)
        self.validate_res(res)
        return res
    
    def validate_res(self, res: pd.DataFrame):
        """
        Verify that result of this virtual trend match the defines outputs
        """
        expected = set([x.name for x in self.metadata.output_trends])
        results = set([x for x in res.columns])
        if len(expected) != len(results) or expected != results:
            raise Exception(
                "The calculated results map doesn't match the defined output tags: expected - {0}, received - {1}".format(expected, results))

    def execute(self, vtCommandLineArgs: VTCommandLineArgsBase, start_utc: datetime, end_utc: datetime) -> pd.DataFrame:
        """
        This is the executaion call for this VT calculation flow
        """
        query = sofoc.build_query( start_utc, end_utc,
            self.metadata.input_trends, self.metadata.calculation_method, self.metadata.sample_frequency)
        if len(query.trends_identifier) > 0:
            res:  List[TagTimeSeriesData] = sofoc.get_data(self.metadata.input_trends, query, vtCommandLineArgs)
            return self.calculate(query.start_date_utc.ToDatetime(), query.end_date_utc.ToDatetime(), res)
        else:
            return self.calculate(query.start_date_utc.ToDatetime(), query.end_date_utc.ToDatetime())

    def get_metadata(self, metadata_file: str) -> virtual_trends_pb2.VirtualTrendsModule:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            message = virtual_trends_pb2.VirtualTrendsModule()
            json_format.Parse(f.read(), message)
            return message

    def df_to_tag_time_series_data_arr(self, res: pd.DataFrame) -> virtual_trends_pb2.TimeSeriesQueryResult:
        time_series_query_result = virtual_trends_pb2.TimeSeriesQueryResult()
        col_index=0
        for trend_metadata in self.metadata.output_trends:
            tag_time_series_data = virtual_trends_pb2.TagTimeSeriesData()
            tag_time_series_data.trend_id.tag_type = common_models_pb2.IdentifierTypes.VIRTUAL
            tag_time_series_data.trend_id.virtual_tag_identifier.module_name = self.metadata.name
            tag_time_series_data.trend_id.virtual_tag_identifier.output_name = trend_metadata.name
            for index, row in res.iterrows():
                data_point = virtual_trends_pb2.DataPoint()
                data_point.time.FromDatetime(index)
                data_point.value = row[col_index]
                tag_time_series_data.time_series.append(data_point)
            time_series_query_result.results.append(tag_time_series_data)
            col_index+=1
        return time_series_query_result
