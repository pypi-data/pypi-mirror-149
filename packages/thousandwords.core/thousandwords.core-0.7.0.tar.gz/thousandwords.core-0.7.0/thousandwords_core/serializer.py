from .serialize import dump
import ast
from io import BytesIO, StringIO
from base64 import b64encode

class NsEntry(dict):
  def __init__(self, name, serType, value = None, key = None):
    self['name'] = name
    self['serializationType'] = serType
    if value is not None:
      self['value'] = value
    if key is not None:
      self['key'] = key

class Serializer:
  def __init__(self, put_handler, pretty=False):
    """use pretty for reader-friendly serialization (json, csv, ...) instead of pickle"""
    self.put = put_handler
    self._ns = []
    self.pretty = pretty
  
  def appendNs(self, name, ser, key=None, value=None):
    self._ns.append({
      "name": name,
      "serializationType": ser,
      "key": key,
      "value": value,
    })
  
  def appendStatement(self, stmt):
    if isinstance(stmt, (ast.Import, ast.ImportFrom)):
      self._imports.append(stmt)
      if isinstance(stmt, ast.Import):
        self._modules[stmt.names[0].name] = stmt.names[0].asname or stmt.names[0].name
    else:
      self._statements.append(stmt)
  
  def appendAfterModuleStatement(self, mod, fn):
    self._moduleStatements.append((mod, fn))

  def add(self, name, obj):
    if self.pretty:
      raise NotImplementedError
    else:
      self.add_default(name, obj)
      
  def add_primitive(self, name, obj):
    value = BytesIO(); dump(obj, value, 'json')
    self.appendNs(name, 'json', value=value.getvalue())
  
  def add_collection(self, name, obj):
    value = StringIO(); dump(obj, value, 'json')
    key = self.put(name, value.getvalue().encode())
    self.appendNs(name, 'json', key=key)
  
  def add_dataframe(self, name, obj):
    value = StringIO(); dump(obj, value, 'json.DataFrame')
    key = self.put(name, value.getvalue().encode())
    self.appendNs(name, 'json.DataFrame', key=key)
  
  def add_series(self, name, obj):
    value = StringIO(); dump(obj, value, 'json.Series')
    key = self.put(name, value.getvalue().encode())
    self.appendNs(name, 'json.Series', key=key)
  
  def add_default(self, name, obj):
    value = BytesIO(); dump(obj, value, 'cloudpickle')
    is_small = value.getbuffer().nbytes < (2 ** 10) * 0.66
    if is_small:
      value = b64encode(value.getvalue()).decode()
      self.appendNs(name, 'b64.cloudpickle', value=value)
    else:
      key = self.put(name, value.getvalue())
      self.appendNs(name, 'cloudpickle', key=key)
    
  @property
  def ns(self):
    return self._ns
