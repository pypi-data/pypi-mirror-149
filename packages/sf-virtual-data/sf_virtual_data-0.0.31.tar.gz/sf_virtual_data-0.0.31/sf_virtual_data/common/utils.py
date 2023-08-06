#!/usr/bin/python3
from sf_virtual_data.common import models as models
import grpc
from datetime import timedelta
import re
import argparse
import os
timedelta_regex = re.compile(r'((?P<hours>\d{2})):((?P<minutes>\d{2})):((?P<seconds>\d{2}))')
MAX_MESSAGE_LENGTH = 100 * 1024 * 1024

def get_grpc_channel_according_to_args(args: models.VTCommandLineArgsBase) -> grpc.Channel:
    if args.insecure:
        channel = grpc.insecure_channel(args.execution_url, options = [
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        ])
    else:
        credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(args.execution_url, credentials,  options = [
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        ])
    return channel

def parse_time(time_str) -> timedelta:
    parts = timedelta_regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

def parse_input(cmd_line_args) -> (models.VTCommandLineArgsBase, list):
    parser = argparse.ArgumentParser(
        description='Input parameters to run virtual data module')
    parser.add_argument('--api-access-key', action='store', required='--debug' in cmd_line_args,
                        dest='api_access_key',
                        help='virtual trends api aceess key')
    parser.add_argument('--insecure', action='store_true',
                        dest='insecure',
                        help='do not verfiy https certificate - used for SF execution')
    parser.add_argument('--cert', action='store',
                        dest='cert', default='cert.pem',
                        help='path to root CA relative to entry point file')
    parser.add_argument('--execution-url', dest='execution_url',
                        action='store', default='solarfocus.bseinc.com')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--metadata-file', dest='metadata_file',
                        action='store', default='metadata.json')
    parser.add_argument('--output-filename', action='store', required='--debug' not in cmd_line_args and '--metadata' not in cmd_line_args,
                        dest='output_filename',
                        help='Output filename to extract')
    args = parser.parse_known_args(cmd_line_args)
    known_args = args[0]
    execution_url = known_args.execution_url
    debug = known_args.debug if known_args.debug is not None else False
    insecure = known_args.insecure if known_args.insecure is not None else False
    metadata_file = known_args.metadata_file
    return (models.VTCommandLineArgsBase(metadata_file, execution_url, debug,
                             known_args.output_filename, known_args.api_access_key, insecure, known_args.cert), args[1])