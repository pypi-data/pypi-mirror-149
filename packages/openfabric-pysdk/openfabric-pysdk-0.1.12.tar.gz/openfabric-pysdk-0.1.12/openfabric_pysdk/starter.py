import logging
import pathlib

from flask import Flask, app, render_template
from flask_cors import CORS

from openfabric_pysdk.config import manifest_config
from openfabric_pysdk.manager import OpenfabricManager

OpenfabricApp = Flask(__name__, template_folder=f"{pathlib.Path(__file__).parent}/templates")
CORS(OpenfabricApp)


@OpenfabricApp.route("/")
def index():
    return render_template("index.html", manifest=manifest_config.all())


class OpenfabricStarter:

    @staticmethod
    def ignite(debug, host, port=5000):
        # Setup logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        service = OpenfabricManager(OpenfabricApp)

        # Setup socket services
        service.install_execution_socket('/app')

        # Setup reset services
        service.install_execution_rest('/app')
        service.install_config_rest('/config')
        service.install_specs__rest('/swagger')
        service.install_manifest_rest('/manifest')
        service.install_benchmark_rest('/benchmark')

        # Install configuration
        service.install_configuration()

        service.run(debug=debug, host=host, port=port)
