import json
import logging
import zlib
from typing import Dict

from flask import Flask, request
from flask_socketio import SocketIO, Namespace, emit

from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import *


#######################################################
#  Execution Socket
#######################################################

class OpenfabricSocket(Namespace):
    __socket_io = None
    __session = None
    __app = None
    __rays: Dict[str, OpenfabricExecutionRay] = None

    def __init__(self, socket_namespace, socket_session, app: Flask):
        super().__init__(socket_namespace)
        self.__session = socket_session
        # Set this variable to "threading", "eventlet" or "gevent" to test the
        # different async modes, or leave it set to None for the application to choose
        # the best option based on installed packages.
        async_mode = "eventlet"
        self.__socket_io = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
        self.__socket_io.on_namespace(self)
        self.__app = app
        self.__rays = dict()

    def run(self, debug, host, port):
        self.__socket_io.run(self.__app, host=host, debug=debug, port=port)

    def on_execute(self, data):
        # Uncompress data
        with MeasureBlockTime("OpenfabricSocket::decompress"):
            uncompressed = zlib.decompress(data)
            request_payload = uncompressed.decode('utf-8')
            dictionary = json.loads(request_payload)
            header = dictionary['header']
            body = dictionary['body']
            session_id = header['session-id']

        if self.__rays.get(session_id) is None:
            self.__rays[session_id] = OpenfabricExecutionRay(session_id)
        ray = self.__rays[session_id]

        # Execute
        with MeasureBlockTime("OpenfabricSocket::execution_callback_function"):
            input_value = InputSchema().load(body)
            result = execution_callback_function(input_value, ray)
            output_value = OutputSchema().dump(result)

        with MeasureBlockTime("OpenfabricSocket::response"):
            emit('response', output_value)

    def on_connect(self):
        logging.info(f'Client connected {request.sid} on {request.host}')

    def on_disconnect(self):
        logging.info(f'Client disconnected {request.sid} on {request.host}')
