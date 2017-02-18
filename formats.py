"""Response formats and parsing."""

import error

import json
import xml.etree.ElementTree


# The various APIs support the following response formats.  (Note that not
# all APIs support all formats.)
JSON='json'
XML='xml'
RDF='rdf'
TTL='ttl'
NT='nt'


class JsonDict(object):
  """A read-only dictionary used to represent JSON objects.

  Properties can be accessed either by dot (foo.bar) or dictionarry syntax
  (foo['bar']).  Most dictionary methods are available as well.
  """
  def __init__(self, dict):
    self._dict = dict

  def __getattr__(self, name):
    return self._dict[name]

  def __getitem__(self, name):
    return self._dict[name]

  def __repr__(self):
    return self._dict.__repr__()

  def __str__(self):
    return str(self._dict)

  def __unicode__(self):
    return unicode(self._dict)

  def get(self, key, default=None):
    return self._dict.get(key, default)

  def has_key(self, key):
    return self._dict.hash_key(key)

  def items(self):
    return self._dict.items()

  def iteritems(self):
    return self._dict.iteritems()

  def iterkeys(self):
    return self._dict.iterkeys()

  def itervalues(self):
    return self._dict.itervalues()

  def keys(self):
    return self._dict.keys()

  def values(self):
    return self._dict.values()


def _parse_json(text):
  """Parse a JSON string."""
  try:
    return json.loads(text, object_hook=JsonDict)
  except ValueError as e:
    raise error.Error(str(e))


def _parse_xml(text):
  """Parse an XML string."""
  try:
    return xml.etree.ElementTree.fromstring(text)
  except xml.etree.ElementTree.ParseError as e:
    raise error.Error(str(e))

  
_PARSERS = {
  JSON: _parse_json,
  RDF: _parse_xml,
  XML: _parse_xml
}


def parse(text, format, parse=True):
  """Parse a string of the given format.

  Args:
    text: The string to parse.
    format: The format of the string to parse.
    parse: If False, the string is not parsed.

  Returns:
    The parsed string (if parse is True) or the string itself
    (if parse is False).

  Raises:
    error.Error if parsing fails.
  """
  if not parse or format not in _PARSERS:
    return text
  parser = _PARSERS[format]
  return parser(text)


def check(format, supported_formats):
  """Check format is in supported_formats."""
  if format not in supported_formats:
    raise error.Error('Unsupported format')
