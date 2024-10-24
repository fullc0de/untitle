import json
from pydantic import BaseModel
from app import task_models

class PydanticSerializer(json.JSONEncoder):   
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump() | {'__type__': type(obj).__name__}
        else:
            return json.JSONEncoder.default(self, obj)

def pydantic_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] in dir(task_models):
            cls = getattr(task_models, obj['__type__'])
            return cls.parse_obj(obj)
    return obj


# Encoder function      
def pydantic_dumps(obj):
    return json.dumps(obj, cls=PydanticSerializer)

# Decoder function
def pydantic_loads(obj):
    return json.loads(obj, object_hook=pydantic_decoder)