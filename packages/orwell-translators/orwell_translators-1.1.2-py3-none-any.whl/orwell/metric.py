from time import time

from .consts import TIMESTAMP_LENGTH


class Metric:

  def __init__ (self, title: str, value: str, properties: dict = None, timestamp: float = None, instance: str = ''):
    self._title = title
    self._value = value
    self._properties = properties if properties is not None else {}
    self._timestamp = time() if timestamp is None else timestamp
    
    if instance is not None: self._properties['instance'] = instance

    self._str_cache = None

  @property
  def title (self): 
    return self._title

  @property
  def value (self): 
    return self._value

  @property
  def properties (self): 
    return self._properties

  @property
  def timestamp (self): 
    return self._timestamp

  def __str__(self) -> str:
    if self._str_cache is None:
      value = self.value.replace('i', '')

      properties = ','.join(['%s="%s"' % (prop, value) for prop, value in self.properties.items()])

      timestamp = str(self.timestamp)[:TIMESTAMP_LENGTH]
      timestamp += ''.join(['0' for _ in range(TIMESTAMP_LENGTH-len(timestamp))])

      self._str_cache = "%s{%s} %s %s" % (self._title, properties, value, timestamp)

    return self._str_cache
