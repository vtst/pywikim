"""Client API for WikiData."""


import formats
import utils


# *************************************************************************
# Get entity data


_GET_ENTITY_BASE_URL = 'https://www.wikidata.org/wiki/Special:EntityData/'
_GET_ENTITY_FORMATS = set([formats.JSON, formats.RDF, formats.TTL, formats.NT])


def get_entity(id, version=None, format=formats.JSON, parse=True):
  """Retrieve entity data from WikiData.

  See https://www.wikidata.org/wiki/Wikidata:Data_access#Linked_Data_interface

  Args:
    id: The entity ID (str)
    version: The entity version (str or int, optional)
    format: The response format (str, optional)
    parse: Whether to parse the response (boolean, optional)

  Returns:
    The response (str or object)
  """
  formats.check(format, _GET_ENTITY_FORMATS)
  url = _GET_ENTITY_BASE_URL + id + '.' + format
  query = {'version': str(version)} if version else None
  response = utils.urlread(url, query)
  return formats.parse(response, format, parse)


# *************************************************************************
# Wikidata query


_QUERY_FORMATS = set([formats.JSON, formats.XML])
_QUERY_URL = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'


def query(query, format=formats.JSON, parse=True):
  formats.check(format, _QUERY_FORMATS)
  query = {'format': format,
           'query': query}
  response = utils.urlread(_QUERY_URL, query)
  return formats.parse(response, format, parse)
