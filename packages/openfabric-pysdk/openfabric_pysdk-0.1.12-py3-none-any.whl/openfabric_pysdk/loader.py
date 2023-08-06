import importlib
from pydoc import locate

from marshmallow import Schema, fields

from openfabric_pysdk.benchmark import MeasureBlockTime
from openfabric_pysdk.config import execution_config


#######################################################
# Class loader utility class
#######################################################
class OpenfabricLoader:

    @staticmethod
    def import_class(name):
        return locate(name.__module__ + "." + name.__name__)

    @staticmethod
    def get_class(name):
        with MeasureBlockTime("OpenfabricLoader::get_class"):
            class_config = execution_config.get(name)
            if class_config is None:
                return None
            clazz = class_config['class']
            package = class_config['package']
            if clazz is None or package is None:
                return None
            module = importlib.import_module(package)
            return locate(module.__name__ + "." + clazz)

    @staticmethod
    def get_function(name):
        with MeasureBlockTime("OpenfabricLoader::get_function"):
            function_config = execution_config.get(name)
            if function_config is None:
                return None
            function = function_config['function']
            package = function_config['package']
            if function is None or package is None:
                return None
            module = importlib.import_module(package)
            print(module.__name__ + "." + function)
            return locate(module.__name__ + "." + function)


# Output concept
InputClass = OpenfabricLoader.get_class("input_class")
InputSchema = OpenfabricLoader.get_class("input_schema")

# Output concept
OutputClass = OpenfabricLoader.get_class("output_class")
OutputSchema = OpenfabricLoader.get_class("output_schema")

# Config concept
ConfigClass = OpenfabricLoader.get_class("config_class")
ConfigSchema = OpenfabricLoader.get_class("config_schema")

# Execution callback function
execution_callback_function = OpenfabricLoader.get_function("main_callback")

# Config callback function
config_callback_function = OpenfabricLoader.get_function("config_callback")
