import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapAlbum={}




    def buildGraph(self,durata):
        nodes=DAO.getAlbumSoglia(durata)
        for album in nodes:
           self._idMapAlbum[album.AlbumId]=album
        self._graph.add_nodes_from(nodes)
        allEdges=DAO.getAllEdges(self._idMapAlbum)
        self._graph.add_edges_from(allEdges)
        return self._graph

    def graphDetails(self):
        return self._graph.number_of_nodes(),self._graph.number_of_edges()