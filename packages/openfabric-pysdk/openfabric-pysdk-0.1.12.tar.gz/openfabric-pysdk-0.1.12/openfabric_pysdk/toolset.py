from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from openfabric_pysdk import benchmark
from openfabric_pysdk.config import manifest_config, state_config
from openfabric_pysdk.loader import *


#######################################################
#  Config API
#######################################################
class OpenfabricConfigRestApi(MethodResource, Resource):

    @doc(description="Get APP configuration", tags=["Developer"])
    @marshal_with(ConfigSchema)
    def get(self) -> ConfigClass:
        with MeasureBlockTime("OpenfabricConfigRestApi::get"):
            state = state_config.get("app_config")
            if state is None:
                return None
            config = ConfigSchema().load(state)
            print(f'Reading config {config}')
            return config

    @doc(description="Set APP configuration", tags=["Developer"])
    @use_kwargs(ConfigSchema, location='json')
    @marshal_with(ConfigSchema)  # marshalling
    def post(self, *args) -> ConfigClass:
        with MeasureBlockTime("OpenfabricConfigRestApi::post"):
            config = list(args) if ConfigSchema().many is True else args[0]
            state_config.set("app_config", ConfigSchema().dump(config))
            print(f'Writing config {config}')
            if config_callback_function:
                config_callback_function(config)
            return config


#######################################################
#  Manifest API
#######################################################
class OpenfabricManifestSchema(Schema):
    name = fields.String(description="App name")
    version = fields.String(description="App version")
    description = fields.String(description="APP description")
    organization = fields.String(description="APP organization")
    sdk = fields.String(description="APP sdk")
    overview = fields.String(description="APP overview")
    input = fields.String(description="APP input")
    output = fields.String(description="APP output")

    def __init__(self):
        super().__init__(many=False)


class OpenfabricManifestRestApi(MethodResource, Resource):

    @doc(description="Get APP manifest", tags=["Developer"])
    @marshal_with(OpenfabricManifestSchema)  # marshalling
    def get(self):
        with MeasureBlockTime("OpenfabricManifestRestApi::get"):
            return manifest_config.all()


#######################################################
#  Benchmark API
#######################################################


class OpenfabricBenchmarkSchema(Schema):
    name = fields.String()
    avg = fields.String()
    count = fields.String()
    stddev = fields.String()
    min = fields.String()
    max = fields.String()

    def __init__(self):
        super().__init__(many=True)


class OpenfabricBenchmarkRestApi(MethodResource, Resource):

    @doc(description="Get APP benchmarks", tags=["Developer"])
    @marshal_with(OpenfabricBenchmarkSchema)  # marshalling
    def get(self):
        with MeasureBlockTime("OpenfabricBenchmarkRestApi::get"):
            return benchmark.get_all_timings_json()
