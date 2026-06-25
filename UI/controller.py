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

    def handleCompConnessa(self, e):
        obj_id = int(self._view._txtIdOggetto.value)
        size = self._model.getConnectedComponent(obj_id)
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa contiene {size} vertici."))
        self._view.update_page()

    def handleIdOggetto(self, e):
        self._view.txt_result.controls.clear()
        try: obj_id = int(self._view._txtIdOggetto.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserisci un numero intero valido!", color="red"))
            self._view.update_page()
            return
        if self._model.checkNodeExists(obj_id):
            self._view.txt_result.controls.append(ft.Text("Object_id corretto!", color="green"))
            self._view._btnCompConnessa.disabled = False
        else:
            self._view.txt_result.controls.append(ft.Text("Object_id non esistente nel grafo!", color="red"))
            self._view._btnCompConnessa.disabled = True
        self._view.update_page()

