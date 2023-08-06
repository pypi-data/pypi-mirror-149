import uuid

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import *


#######################################################
#  Execution API
#######################################################
class OpenfabricExecutionRestApi(MethodResource, Resource):

    @doc(description="Execute app and get response", tags=["Execution"])
    @use_kwargs(InputSchema, location='json')
    @marshal_with(OutputSchema)  # marshalling
    def post(self, *args) -> OutputClass:
        ray = OpenfabricExecutionRay(uuid.uuid4().hex)

        with MeasureBlockTime("OpenfabricExecutionRestApi::execution_callback_function"):
            input_value = list(args) if InputSchema().many is True else args[0]
            result = execution_callback_function(input_value, ray)

        return result
