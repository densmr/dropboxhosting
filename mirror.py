#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Denis Pushkin

__author__='Denis Pushkin (github.com/densmr)'

# This code is a reduction / adaptation of DropbProx project (http://code.google.com/p/dropbprox/)
# by Paulo Jerônimo (http://paulojeronimo.com)
# held specifically to add default page for site hostings

# Set up your Dropbox prefix (e.g. dl.dropbox.com/u/123456 where 123456 — your Dropbox number):
DROPBOX_PREFIX ='dl.dropbox.com/spa/7k4i6qqjxq9yxvc/site/public'
DEBUG = False
HTTP_PREFIX = "http://"
DEFAULT_PAGE = "index.html"
IGNORE_HEADERS = frozenset([
  'set-cookie',
  'expires',
  'cache-control',
  # Ignore hop-by-hop headers
  'connection',
  'keep-alive',
  'proxy-authenticate',
  'proxy-authorization',
  'te',
  'trailers',
  'transfer-encoding',
  'upgrade',
])

import logging
import wsgiref.handlers

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.runtime import apiproxy_errors

class MirroredContent(object):
  def __init__(self, original_address, translated_address,
               status, headers, data, base_url):
    self.original_address = original_address
    self.translated_address = translated_address
    self.status = status
    self.headers = headers
    self.data = data
    self.base_url = base_url

  @staticmethod
  def fetch_and_store(base_url, translated_address, mirrored_url):
    """Fetch a page.
    
    Args:
      base_url: The hostname of the page that's being mirrored.
      translated_address: The URL of the mirrored page on this site.
      mirrored_url: The URL of the original page. Hostname should match
        the base_url.
    
    Returns:
      A new MirroredContent object, if the page was successfully retrieved.
      None if any errors occurred or the content could not be retrieved.
    """
    logging.debug("Fetching '%s'", mirrored_url)
    try:
      response = urlfetch.fetch(mirrored_url)
    except (urlfetch.Error, apiproxy_errors.Error):
      logging.exception("Could not fetch URL")
      return None

    adjusted_headers = {}
    for key, value in response.headers.iteritems():
      adjusted_key = key.lower()
      if adjusted_key not in IGNORE_HEADERS:
        adjusted_headers[adjusted_key] = value

    return MirroredContent(
      base_url=base_url,
      original_address=mirrored_url,
      translated_address=translated_address,
      status=response.status_code,
      headers=adjusted_headers,
      data=response.content)
      

class MirrorHandler(webapp.RequestHandler):
  def get_relative_url(self):
    path = self.request.path
    logging.debug('Path = %s', path)
    if path == "/":
      return DROPBOX_PREFIX + path + DEFAULT_PAGE
    return DROPBOX_PREFIX + path

  def get(self, base_url = DEFAULT_PAGE):
    assert base_url
    logging.debug('User-Agent = "%s", Referrer = "%s"',
                  self.request.user_agent,
                  self.request.referer)
    logging.debug('Base_url = "%s", url = "%s"', base_url, self.request.url)
    translated_address = self.get_relative_url()
    logging.debug('Translated address = %s', translated_address)
    content = MirroredContent.fetch_and_store(base_url, translated_address, 
      HTTP_PREFIX + translated_address)
    if content is None:
      return self.error(404)
    for key, value in content.headers.iteritems():
      self.response.headers[key] = value
    self.response.out.write(content.data)


app = webapp.WSGIApplication([
  (r"/", MirrorHandler),
  (r"/([^/]+).*", MirrorHandler)
], debug=DEBUG)


def main():
  wsgiref.handlers.CGIHandler().run(app)


if __name__ == "__main__":
  main()
