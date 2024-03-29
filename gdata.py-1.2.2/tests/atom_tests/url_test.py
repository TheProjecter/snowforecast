#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'api.jscudder (Jeff Scudder)'


import unittest
import atom.url


class UrlTest(unittest.TestCase):

  def testParseUrl(self):
    url = atom.url.parse_url('http://www.google.com/calendar/feeds')
    self.assertTrue(url.protocol == 'http')
    self.assertTrue(url.host == 'www.google.com')
    self.assertTrue(url.path == '/calendar/feeds')
    self.assertTrue(url.params == {})

    url = atom.url.parse_url('http://example.com:6091/calendar/feeds')
    self.assertTrue(url.protocol == 'http')
    self.assertTrue(url.host == 'example.com')
    self.assertTrue(url.port == '6091')
    self.assertTrue(url.path == '/calendar/feeds')
    self.assertTrue(url.params == {})
    
    url = atom.url.parse_url('/calendar/feeds?foo=bar')
    self.assertTrue(url.protocol is None)
    self.assertTrue(url.host is None)
    self.assertTrue(url.path == '/calendar/feeds')
    self.assertTrue(len(url.params.keys()) == 1)
    self.assertTrue('foo' in url.params)
    self.assertTrue(url.params['foo'] == 'bar')
    
    url = atom.url.parse_url('/calendar/feeds?my+foo=bar%3Dx')
    self.assertTrue(len(url.params.keys()) == 1)
    self.assertTrue('my foo' in url.params)
    self.assertTrue(url.params['my foo'] == 'bar=x')
   
  def testUrlToString(self):
    url = atom.url.Url(port=80)
    url.host = 'example.com'
    self.assertTrue(str(url), '//example.com:80')

    url = atom.url.Url(protocol='http', host='example.com', path='/feed')
    url.params['has spaces'] = 'sneaky=values?&!'
    self.assertTrue(url.to_string() == (
        'http://example.com/feed?has+spaces=sneaky%3Dvalues%3F%26%21'))

  def testGetRequestUri(self):
    url = atom.url.Url(protocol='http', host='example.com', path='/feed')
    url.params['has spaces'] = 'sneaky=values?&!'
    self.assertTrue(url.get_request_uri() == (
        '/feed?has+spaces=sneaky%3Dvalues%3F%26%21'))
    self.assertTrue(url.get_param_string() == (
        'has+spaces=sneaky%3Dvalues%3F%26%21'))

  def testComparistons(self):
    url1 = atom.url.Url(protocol='http', host='example.com', path='/feed', 
                        params={'x':'1', 'y':'2'})
    url2 = atom.url.Url(host='example.com', port=80, path='/feed', 
                        params={'y':'2', 'x':'1'})
    self.assertEquals(url1, url2)
    url3 = atom.url.Url(host='example.com', port=81, path='/feed', 
                        params={'x':'1', 'y':'2'})
    self.assert_(url1 != url3)
    self.assert_(url2 != url3)
    url4 = atom.url.Url(protocol='ftp', host='example.com', path='/feed',
                        params={'x':'1', 'y':'2'})
    self.assert_(url1 != url4)
    self.assert_(url2 != url4)
    self.assert_(url3 != url4)

     

if __name__ == '__main__':
  unittest.main()
