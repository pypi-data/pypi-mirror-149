import pickle
import cloudpickle
import json
from base64 import b64decode

def dump(obj, fp, type):
  if type == "json.DataFrame":
    raise NotImplementedError
  elif type == "json.Series":
    raise NotImplementedError
  elif type == "json":
    return json.dump(obj, fp)
  elif type == "cloudpickle":
    return cloudpickle.dump(obj, fp)

def load(fp, type):
  if type == "json.DataFrame":
    raise NotImplementedError
  elif type == "json.Series":
    raise NotImplementedError
  elif type == "json":
    return json.load(fp)
  elif type == "cloudpickle":
    return pickle.load(fp)
  elif type == "b64.cloudpickle":
    return pickle.loads(b64decode(fp.read()))

