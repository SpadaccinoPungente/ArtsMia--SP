import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._view.txt_result.controls.clear()
        self._model.buildGraph()
        n_nodes, n_edges = self._model.getGraphDetails()
        if not n_nodes:
            self._view.txt_result.controls.append(ft.Text("Errore durante la creazione del grafo", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente!\n{n_nodes} nodi e {n_edges} archi.", color="green"))
        self._view.update_page()

    def handleCompConnessa(self,e):
        pass

    def handleIdOggetto(self, e):
        self._view.txt_result.controls.clear()
        if self._view._txtIdOggetto.value in self._model.getAllNodes():
            self._view.txt_result.controls.append(ft.Text("Object_id corretto!", color="green"))
            self._view._btnCompConnessa.disabled = False
        self._view.txt_result.controls.append(ft.Text("Object_id non esistente!", color="red"))
        self._view._btnCompConnessa.disabled = True
        self._view.update_page()

