from .serialize import load
from io import StringIO, BytesIO

class Resolver:
  def __init__(self, get, upsert, delete=None):
    self.get = get
    self.upsert = upsert
    self.delete = delete
  
  def diff(self, newNs, oldNs = []):
    oldNames = set([e['name'] for e in oldNs])
    newNames = set([e['name'] for e in newNs])
    for n in list(oldNames - newNames):
      self.delete(n)
    for e in newNs:
      if e.get('value') is not None:
        k = 'value'
      elif e.get('key') is not None:
        k = 'key'
      needsUpsert = True
      for e2 in oldNs:
        if e2['name'] == e['name']:
          needsUpsert = (e[k] != e2[k])
      if needsUpsert:
        if k == 'key':
          data = self.get(e[k])
          v = load(BytesIO(data), e['serializationType'])
        else:
          data = e['value']
          v = load(StringIO(data), e['serializationType'])        
        self.upsert(e['name'], v)
