#!/usr/bin/python3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from . import solar_focus_sfv_lib as sofoc
from sf_virtual_data.common.models import VTCommandLineArgsBase
from sf_virtual_data.common.api import virtual_sfv_pb2
from sf_virtual_data.common.api import solar_field_common_pb2
from sf_virtual_data.common.api import common_models_pb2
import google.protobuf.json_format as json_format
from google.protobuf import wrappers_pb2
from user_calculation import calculate as user_calc
from user_calculation import plot as user_plot
import pandas as pd
from math import isnan
from google.protobuf import struct_pb2
from virtual_trend import solar_focus_trends_lib as virtual_trends_lib
from typing import Dict

class VirtualSfvRunner(ABC):
    def __init__(self, metadata_file: str):
        self.metadata = self.get_metadata(metadata_file)

    def get_metadata(self, metadata_file: str) -> virtual_sfv_pb2.VirtualSfvModule:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            message = virtual_sfv_pb2.VirtualSfvModule()
            json_format.Parse(f.read(), message)
            return message


    def calculate(self, vtCommandLineArgs: VTCommandLineArgsBase, query_time_utc: datetime, margin: timedelta, inputs_from_solar_focus: virtual_sfv_pb2.VirtualSfvInputsResult = None) -> pd.DataFrame:
        sfv_inputs = []
        data_points_inputs = []
        for input in self.metadata.input_tags:
            if input.raw_id.tag_type == common_models_pb2.NUMERIC_PER_SFO:
                new_input = common_models_pb2.VirtualModuleInputTag(raw_id = common_models_pb2.TagsIdentifierBase(tag_identifier =common_models_pb2.TagIdentifier(id = input.raw_id.sfo_tag_identifier.tag_id)),
                tag_name = input.tag_name, source_name = input.source_name, source_id = input.source_id, variable_name = input.variable_name )
                sfv_inputs.append(new_input)
            else:
                data_points_inputs.append(input)

        input_sfv_df = sofoc.solar_field_to_df(sfv_inputs, inputs_from_solar_focus.sfv_tags)
        input_data_points: Dict[str, float] ={}
        input_data_points_df = virtual_trends_lib.convert_trends_res_to_df(data_points_inputs, inputs_from_solar_focus.data_points)
        closest_idx = input_data_points_df.index[input_data_points_df.index.get_loc(query_time_utc, method='nearest')]
        for input in data_points_inputs:
            input_data_points[input.variable_name] = input_data_points_df[input.variable_name][closest_idx]
        inputUpdateTime = sofoc.solar_field_to_update_time(sfv_inputs, inputs_from_solar_focus.sfv_tags)
        res = user_calc(query_time_utc, margin, input_data_points, input_sfv_df, inputUpdateTime)
        resSolarFieldDto = self.__df_to_solar_field__(res)
        self.validate_res(resSolarFieldDto, inputs_from_solar_focus.sfv_tags)
        if vtCommandLineArgs.debug:
            user_plot(res)
        return resSolarFieldDto

    def validate_res(self, res: solar_field_common_pb2.SolarFieldDto, inputs_from_solar_focus: solar_field_common_pb2.SolarFieldDto = None):
        """
        Verify that result of this virtual sfv match the defines outputs
        """
        if len(res.data) != len(self.metadata.output_tags):
            raise Exception(f"Output result does not match output tags size")

        if inputs_from_solar_focus is None:
            return

        for i in range(0, len(self.metadata.output_tags)):
            output_md_name = self.metadata.output_tags[i].name
            output_name = res.data[i].tag_id.virtual_tag_identifier.output_name
            if (output_md_name != output_name):
                raise Exception(f"Output name does not match output md name")

        layout_size = len(inputs_from_solar_focus.data[0].nullable_data)
        for tag in res.data:
            if len(tag.nullable_data) != layout_size:
                raise Exception(f"Output result does not match layout size")

    def execute(self, vtCommandLineArgs: VTCommandLineArgsBase, query_time_utc: datetime, margin: timedelta) -> solar_field_common_pb2.SolarFieldDto:
        """
        This is the execution call for this VT calculation flow
        """
        query: virtual_sfv_pb2.VirtualSfvInputsQuery = sofoc.build_query(query_time_utc, margin,self.metadata.input_tags, self.metadata.calculation_method)
        if len(query.sfv_tags_query.tags_descriptions) > 0:
            res: virtual_sfv_pb2.VirtualSfvInputsResult = sofoc.get_data(query, vtCommandLineArgs)
            return self.calculate(vtCommandLineArgs = vtCommandLineArgs, query_time_utc = query.sfv_tags_query.query_time_utc.ToDatetime(), margin = query.sfv_tags_query.margin.ToTimedelta(), inputs_from_solar_focus = res)
        else:
            return self.calculate(vtCommandLineArgs = vtCommandLineArgs, query_time_utc = query.sfv_tags_query.query_time_utc.ToDatetime(), margin = query.sfv_tags_query.margin.ToTimedelta())

    def __number_to_proto_float__(self, number) -> wrappers_pb2.FloatValue:
        fv = wrappers_pb2.FloatValue()
        fv.value = number
        return fv

    def __df_to_solar_field__(self, dF: pd.DataFrame) -> solar_field_common_pb2.SolarFieldDto:
        output_res = solar_field_common_pb2.SolarFieldDto()
        for output_tag in self.metadata.output_tags:
            tag_data = solar_field_common_pb2.TagData()
            data = dF[output_tag.name]
            data = data.apply(self.__number_to_proto_float__)
            tag_id = common_models_pb2.VirtualTagIdentifier()
            tag_data.tag_id.virtual_tag_identifier.module_name = self.metadata.name
            tag_data.tag_id.virtual_tag_identifier.output_name = output_tag.name
            tag_data.tag_id.tag_type = common_models_pb2.IdentifierTypes.VIRTUAL
            tag_data.nullable_data.extend(data)
            output_res.data.append(tag_data)
        return output_res