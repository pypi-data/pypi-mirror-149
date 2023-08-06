#!/usr/bin/python3

class VTCommandLineArgsBase:
    def __init__(self, metadata_file, execution_url, debug, output_filename, api_access_key, insecure, cert):
        self.metadata_file = metadata_file
        self.execution_url = execution_url
        self.debug = debug
        self.output_filename = output_filename
        self.api_access_key = api_access_key
        self.insecure = insecure
        self.cert = cert
