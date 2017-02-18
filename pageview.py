"""Client API for WikiMedia pageview API.

This is using the Wiki API documented at:
https://wikitech.wikimedia.org/wiki/Analytics/PageviewAPI
"""

import formats
import utils

import datetime


# Values for access parameter
ALL_ACCESS = 'all-access'
DESKTOP = 'desktop'
MOBILE_APP = 'mobile-app'
MOBILE_WEB = 'mobile-web'

# Values for agent parameter
ALL_AGENTS = 'all-agents'
USER = 'user'
SPIDER = 'spider'
BOT = 'bot'

# Values for granularity parameter
DAILY = 'daily'
MONTHLY = 'monthly'


_SUPPORTED_FORMATS = set([formats.JSON])
_DEFAULT_PROJECT = 'en.wikipedia.org'
_WIKIMEDIA_API_URL = 'http://wikimedia.org/api/rest_v1/'


def _get(parameters, format=formats.JSON, parse=True):
  formats.check(format, _SUPPORTED_FORMATS)
  response = utils.urlread(_WIKIMEDIA_API_URL + '/'.join(parameters))
  return formats.parse(response, format, parse)


def _format_date(date):
  if isinstance(date, datetime.date):
    return date.strftime('%Y%m%d') + '00'
  else:
    return date + '00'


def get_article(title, start, end,
                project=_DEFAULT_PROJECT,
                access=ALL_ACCESS,
                agent=ALL_AGENTS,
                granularity=DAILY,
                **kwargs):
  """Get the views for an article."""
  return _get(['metrics', 'pageviews', 'per-article',
               project, access, agent, title, granularity,
               _format_date(start), _format_date(end)],
              **kwargs)


def _create_dict(items):
  if len(items) == 0:
    return None
  else:
    d = {}
    for key, value in items[0].iteritems():
      if key != 'timestamp' and key != 'views':
        d[key] = value
    d['views_by_timestamp'] = dict(
      (item.timestamp[:8], item.views) for item in items)
    return d


def get_article_as_dict(*args, **kwargs):
  response = get_article(*args, format=formats.JSON, parse=True, **kwargs)
  return _create_dict(response.items)


def get_aggregate(start, end,
                  project=_DEFAULT_PROJECT,
                  access=ALL_ACCESS,
                  agent=ALL_AGENTS,
                  granularity=DAILY,
                  **kwargs):
  """Get aggregated views for a project."""
  return _get(['metrics', 'pageviews', 'aggregate',
               project, access, agent, granularity,
               _format_date(start), _format_date(end)], **kwargs)


def get_aggregate_as_dict(*args, **kwargs):
  response = get_aggregate(*args, format=formats.JSON, parse=True, **kwargs)
  return _create_dict(response.items)


def _format_date_top(date):
  if isinstance(date, datetime.date):
    return date.strftime('%Y/%m/%d')
  else:
    return date[0:4] + '/' + date[4:6] + '/' + date[6:8]


def get_top_articles(date, project=_DEFAULT_PROJECT, access=ALL_ACCESS,
                     **kwargs):
  """Get top articles for a project."""
  return _get(['metrics', 'pageviews', 'top',
               project, access,
               _format_date_top(date)], **kwargs)

