import json

#######################################################
#  Concept class
#######################################################
from marshmallow import Schema, post_load


class OpenfabricConcept(object):

    def __init__(self, data, many=False, **kwargs):
        if type(data) is dict:
            for key in data:
                self.__setattr__(key, data[key])
