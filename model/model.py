import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.id_map_art_obj = {art_obj.object_id: art_obj for art_obj in DAO.getAllArtObjects()}

    def buildGraph(self):
        self.graph.clear()
        self.graph.add_nodes_from(self.id_map_art_obj.values())
        for u, v, w in DAO.getAllEdges():
            self.graph.add_edge((u, v, w))

    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getAllNodes(self):
        return self.graph.nodes()