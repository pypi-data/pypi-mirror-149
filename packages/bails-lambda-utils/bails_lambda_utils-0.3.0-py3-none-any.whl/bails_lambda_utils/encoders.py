import json
import datetime
import re


class ModelEncoder(json.JSONEncoder):
    """
    Maps Pynamo models and other json to a json format lambda's can process
    """

    def default(self, obj):
        if hasattr(obj, "attribute_values"):
            return obj.attribute_values
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
