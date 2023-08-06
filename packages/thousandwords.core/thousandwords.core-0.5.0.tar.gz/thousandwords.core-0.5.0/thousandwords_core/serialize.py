import pickle
import cloudpickle
import pandas as pd
import json
from io import BytesIO, StringIO
from base64 import b64decode

def dump(obj, fp, type):
  if type == "json.DataFrame":
    return obj.to_json(fp, orient="table")
  elif type == "json.Series":
    return obj.to_json(fp, orient="table")
  elif type == "json":
    return json.dump(obj, fp)
  elif type == "cloudpickle":
    return cloudpickle.dump(obj, fp)

def load(fp, type):
  if type == "json.DataFrame":
    return pd.read_json(fp, orient='table')
  elif type == "json.Series":
    return pd.read_json(fp, orient='table').squeeze()
  elif type == "json":
    return json.load(fp)
  elif type == "cloudpickle":
    return pickle.load(fp)
  elif type == "b64.cloudpickle":
    return pickle.loads(b64decode(fp.read()))

