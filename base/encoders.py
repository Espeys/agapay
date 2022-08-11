from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.db.models.fields.files import FieldFile, ImageFieldFile


import json



class ModelEncoder(DjangoJSONEncoder):

    def default(self, obj):

        if isinstance(obj, Model):
            model = model_to_dict(obj)

            for k, v in model.items():
                if type(v) in [FieldFile, ImageFieldFile]:
                    model[k] = str(v)
            return model

        return super().default(obj)


class ModelDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        raise Exception(obj)

# json.JSONDecoder(*, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None