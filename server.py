
import cherrypy

import matching_server
from matching_server import MatchingServer

if __name__ == '__main__':
    cherrypy.quickstart(MatchingServer())
