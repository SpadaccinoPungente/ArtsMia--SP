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
            if u in self.id_map_art_obj and v in self.id_map_art_obj:
                nodo_u = self.id_map_art_obj[u]
                nodo_v = self.id_map_art_obj[v]
                self.graph.add_edge(nodo_u, nodo_v, weight=w)

    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getAllNodes(self):
        return self.graph.nodes()

    def checkNodeExists(self, obj_id):
        return obj_id in self.id_map_art_obj

    def getConnectedComponent(self, obj_id):
        nodo = self.id_map_art_obj[obj_id]
        component = nx.node_connected_component(self.graph, nodo)
        return len(component)