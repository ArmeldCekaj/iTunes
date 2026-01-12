import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allNodi = []
        self._idMapAlbum = {}


    def buildGraph(self, durataMin):
        self._grafo.clear()
        self._allNodi = DAO.getAlbums(durataMin)
        self._grafo.add_nodes_from(self._allNodi)
        self._idMapAlbum = {n.AlbumId: n for n in self._allNodi}
        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)

    def getInfoConnessa(self, a1):
        cc = nx.node_connected_component(self._grafo, a1)
        return len(cc), self._getDurataTot(cc)
    def _getDurataTot(self, listOfNodes):
        sumDurata= 0
        for n in listOfNodes:
            sumDurata += n.dTot
        return sumDurata


    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes())