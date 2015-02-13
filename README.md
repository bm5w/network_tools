[![Travis](<travis_badge_url>)](<travis_badge_url>)
# network_tools
A simple HTTP server, which responds to HTTP 1.1 requests appropriately.
The server parses the request and responds accordingly.
Returns 200 OK response, header, and file if appropriate GET request is made.
Returns appropriate error if non GET or non HTTP 1.1 request is made.
If request for folder is called, server responds with a list of items
in that directory.

