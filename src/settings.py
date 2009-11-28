# Logging configuration
import logging
import logging.config
import twitterlog
logging.utopialog = twitterlog
logging.config.fileConfig("logging.conf")

# Search for this query
SEARCH_QUERY = "Utopie"

# Number of results returned from a single web search. The starting result is
# a random multiple of SEARCH_RESULTS + 1 (e.g. 1, 11, 21... for 10).
SEARCH_RESULTS = 10

# Maximum number of results considered. If SEARCH_RESULTS=10 and
# SEARCH_MAX_RESULTS=1000, the last results will be 991 to 1000.
SEARCH_MAX_RESULTS = 1000

# Wait for this interval between printing two results (in seconds)
SEARCH_INTERVAL = 30

# Yahoo application ID
YAHOO_APP_ID = "12345678"

