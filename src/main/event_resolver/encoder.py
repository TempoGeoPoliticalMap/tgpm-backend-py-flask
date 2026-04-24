import json

from openapi_models.models.base_model import Model


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return o.to_dict()
        return super().default(o)
