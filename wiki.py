"""Client API for reading the content of wikipedia pages.

This is using the Wiki API documented at:
https://www.mediawiki.org/wiki/API:Main_page
"""

import formats
import utils


_SUPPORTED_FORMATS = set([formats.JSON, formats.XML])
_DEFAULT_PROJECT = 'en.wikipedia.org'


def _get_url(project):
  return 'https://' + project + '/w/api.php'


def _get_titles(title, titles):
  if title:
    if titles:
      raise error.Error('title and titles cannot be both supplied')
    else:
      return title
  else:
    if titles:
      return '|'.join(titles)
    else:
      raise error.Error('title or titles must be supplied.')
      

def _query(query, title=None, titles=None, project=_DEFAULT_PROJECT,
           format=formats.JSON, parse=True):
  formats.check(format, _SUPPORTED_FORMATS)
  full_query = {'format': format,
                'action': 'query',
                'titles': _get_titles(title, titles)}
  full_query.update(query)
  response = utils.urlread(_get_url(project), full_query)
  return formats.parse(response, format, parse)


def get_page(**kwargs):
  query = {'rvprop': 'content', 'prop': 'revisions'}
  return _query(query, **kwargs)


def get_intro_text(**kwargs):
  query = {'prop': 'extracts', 'exintro': '', 'explaintext': ''}
  return _query(query, **kwargs)
