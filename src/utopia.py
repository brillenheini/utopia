#! /usr/bin/env python

# Copyright (C) 2009 Stefan Schweizer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""The Utopia Machine.

Repeatedly search the web for 'Utopie', send a random result to a printer and
open it in a browser. Exceptions are logged to twitter. Configuration in
settings.py.

Created for zweintopf for their installation at the Absolutely Free exhibition
in Graz.

    http://www.zweintopf.net/
    http://www.absolutely-free.at/

"""

import logging
import random
import signal
import subprocess
import sys
import time
import urllib2
import webbrowser

import yahoo.search.web

from settings import *

class YahooSearcher(object):
    """Search the web with Yahoo."""

    def __init__(self, app_id, proxy=None):
        self.searcher = yahoo.search.web.WebSearch(app_id)
        if proxy:
            handler = urllib2.ProxyHandler({"http" : proxy})
            opener = urllib2.build_opener(handler)
            self.searcher.install_opener(opener)

    def search(self, query, results=10, start=1,
               language="de", format="html", adult_ok=1):
        logging.info("Search parameters: query=%s, results=%d, "
                     "start=%d, language=%s, format=%s, adult_ok=%d",
                     query, results, start, language, format, adult_ok)
        self.searcher.query = query
        self.searcher.results = results
        self.searcher.start = start
        self.searcher.language = language
        self.searcher.format = format
        self.searcher.adult_ok = adult_ok
        self.results = self.searcher.get_results()
        return self.results

    def parse(self, xml=None):
        if xml is None:
            xml = self.results
        return self.searcher.parse_results(xml)

    def printXML(self):
        if self.results:
            print self.results.toxml()

class Printer(object):
    def printResult(self, result):
        proc = subprocess.Popen("lp", shell=True, stdin=subprocess.PIPE)
        # Switching the printer to bold wastes less paper
        proc.communicate("\x1B\x45" + self.formatResult(result))

    def formatResult(self, result):
        return (result.Title   + "\n\n" + \
               result.Url + "\n\n" + \
               result.Summary + "\n\n" + \
               "\n\n\n\n\n\n\n\n\n\n\n\n").encode("utf-8")

def handler(signalnum, frame):
    logging.warn("Utopia Machine stopped")
    logging.info("---------------------------")
    sys.exit()

def main():
    signal.signal(signal.SIGTERM, handler)
    logging.warn("Starting Utopia Machine")
    searcher = YahooSearcher(YAHOO_APP_ID)
    printer = Printer()

    max = (SEARCH_MAX_RESULTS - SEARCH_RESULTS) / SEARCH_RESULTS
    logging.debug("Maximum for random: %d", max)
    while True:
        try:
            start = random.randint(0, max) * SEARCH_RESULTS + 1
            searcher.search(SEARCH_QUERY, SEARCH_RESULTS, start)
            results = searcher.parse()
            logging.debug("Search returned %d results",
                          results.totalResultsReturned)

            for result in results:
                logging.debug(result.Title)
                printer.printResult(result)
                webbrowser.open(result.Url)
                time.sleep(SEARCH_INTERVAL)
        except SystemExit:
            raise
        except:
            logging.exception("An unexpected error occured")
            raise

if __name__ == "__main__":
    main()

