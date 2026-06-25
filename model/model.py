import copy
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.id_map_art_obj = {art_obj.object_id: art_obj for art_obj in DAO.getAllArtObjects()}

        self.best_path = []
        self.best_score = 0

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

    def cerca_cammino(self, obj_id, LUN):
        self.best_path = []
        self.best_score = -1

        nodo_partenza = self.id_map_art_obj[obj_id]
        target_class = nodo_partenza.classification
        parziale = [nodo_partenza]

        self._ricorsione(parziale, LUN, target_class)

        return self.best_path, self.best_score

    def _ricorsione(self, parziale, LUN, target_class):

        # CASO TERMINALE / OBIETTIVO
        if len(parziale) == LUN:
            score = self.get_score(parziale)
            if score > self.best_score:
                self.best_score = score
                self.best_path = copy.deepcopy(parziale)
            return

        # GENERAZIONE MOSSE
        ultimo_nodo = parziale[-1]
        mosse_possibili = self.graph.neighbors(ultimo_nodo)

        # CICLO FOR E BACKTRACKING
        for mossa in mosse_possibili:
            if mossa not in parziale and self.is_valid(mossa, target_class):
                parziale.append(mossa)
                self._ricorsione(parziale, LUN, target_class)
                parziale.pop()

    def is_valid(self, mossa, target_class):
        return True if mossa.classification == target_class else False

    def get_score(self, parziale):
        score = 0
        for i in range(len(parziale) - 1):
            nodo_corrente = parziale[i]
            nodo_successivo = parziale[i + 1]
            score += self.graph[nodo_corrente][nodo_successivo]['weight']
        return score
