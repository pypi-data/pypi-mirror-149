from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, session
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from openfabric_pysdk.loader import ConfigSchema, config_callback_function
from openfabric_pysdk.transport.rest import OpenfabricExecutionRestApi
from openfabric_pysdk.config import manifest_config, state_config
from openfabric_pysdk.transport.socket import OpenfabricSocket
from openfabric_pysdk.toolset import OpenfabricConfigRestApi, OpenfabricManifestRestApi, OpenfabricBenchmarkRestApi


#######################################################
#  Core transport class manager
#######################################################
class OpenfabricManager:
    __app: Flask = None
    __api: Api = None
    __docs: FlaskApiSpec = None
    __socket: OpenfabricSocket = None

    def __init__(self, app: Flask):
        self.__app = app
        self.__api = Api(app)
        self.__docs = FlaskApiSpec(app)

    def install_specs__rest(self, endpoint):
        print(f"Install Specs REST endpoints on {endpoint}")
        specs = {
            'APISPEC_SPEC': APISpec(
                title="App " + manifest_config.get('name'),
                version=manifest_config.get('version'),
                plugins=[MarshmallowPlugin()],
                openapi_version='2.0.0',
                info=dict(
                    termsOfService='https://openfabric.ai/terms/',
                    contact=dict(name=manifest_config.get('organization'), url="https://openfabric.ai"),
                    description=manifest_config.get('description')),
            ),
            'APISPEC_SWAGGER_URL': f'/{endpoint}/',  # URI to access API Doc JSON
            'APISPEC_SWAGGER_UI_URL': f'/{endpoint}-ui/'  # URI to access UI of API Doc
        }
        self.__app.config.update(specs)

    def install_execution_rest(self, endpoint):
        print(f"Install Execution REST endpoints on {endpoint}")
        self.__api.add_resource(OpenfabricExecutionRestApi, endpoint)
        self.__docs.register(OpenfabricExecutionRestApi)

    def install_config_rest(self, endpoint):
        if ConfigSchema is None:
            print(f"No Config schema available")
            return
        print(f"Install Config REST endpoints on {endpoint}")
        self.__api.add_resource(OpenfabricConfigRestApi, endpoint)
        self.__docs.register(OpenfabricConfigRestApi)

    def install_manifest_rest(self, endpoint):
        print(f"Install Manifest REST endpoints on {endpoint}")
        self.__api.add_resource(OpenfabricManifestRestApi, endpoint)
        self.__docs.register(OpenfabricManifestRestApi)

    def install_benchmark_rest(self, endpoint):
        print(f"Install Benchmark REST endpoints on {endpoint}")
        self.__api.add_resource(OpenfabricBenchmarkRestApi, endpoint)
        self.__docs.register(OpenfabricBenchmarkRestApi)

    def install_execution_socket(self, endpoint):
        print(f"Install Execution SOCKET endpoints on {endpoint}")
        self.__socket = OpenfabricSocket(endpoint, session, self.__app)

    def install_configuration(self):
        print(f"Install APP configuration")
        if config_callback_function:
            state = state_config.get("app_config")
            if state is not None:
                config = ConfigSchema().load(state_config.get("app_config"))
                config_callback_function(config)

    def run(self, debug, host, port):
        self.__socket.run(debug=debug, host=host, port=port)
        # self.__app.run(debug=debug, host=host, port=port)
