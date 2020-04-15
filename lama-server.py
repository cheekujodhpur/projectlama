from game import GameMaster
from twisted.internet import reactor, endpoints
from twisted.web import server
import sys

if __name__ == "__main__":
    g = GameMaster()
    endpoint = endpoints.TCP4ServerEndpoint(reactor, 1144)
    endpoint.listen(server.Site(g))
    reactor.run()
