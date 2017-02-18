"""Utility functions common to all client APIs."""

import error

import urllib
import urllib2


def _query_string(dict):
  """Get a query string from a dictionary."""
  return '&'.join(
    name + '=' + urllib.quote(value.encode('utf8'))
    for name, value in dict.iteritems())


def urlopen(base_url, query=None):
  """Wrapper around urllib2.urlopen.

  Args:
    base_url: The base URL for the request.
    query: A dictionary of query parameters (dict, optional).

  Returns:
    A file like object.

  Raises:
    error.Error if something goes wrong.
  """
  url = base_url + ('?' + _query_string(query) if query else '')
  try:
    return urllib2.urlopen(url)
  except (urllib2.URLError, urllib2.HTTPError) as e:
    raise error.Error(str(e))


def urlread(base_url, query=None):
  """Read the content of an URL.

  Args:
    base_url: The base URL for the request.
    query: A dictionary of query parameters (dict, optional).

  Returns:
    A string.

  Raises:
    error.Error if something goes wrong.
  """
  try:
    return urlopen(base_url, query).read()
  except IOError as e:
    raise error.Error(str(e))
