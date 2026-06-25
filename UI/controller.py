import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self.sel_obj_id = None

    def handleAnalizzaOggetti(self, e):
        self._view.txt_result.controls.clear()
        self._model.buildGraph()
        n_nodes, n_edges = self._model.getGraphDetails()
        if not n_nodes:
            self._view.txt_result.controls.append(ft.Text("Errore durante la creazione del grafo", color="red"))
            return
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente!\n{n_nodes} nodi e {n_edges} archi.", color="green"))
        self._view.update_page()

    def handleCompConnessa(self, e):
        self._view.txt_result.controls.clear()

        if self._model.graph.number_of_nodes() == 0:
            self._model.buildGraph()

        if self.sel_obj_id is None:
            self._view.txt_result.controls.append(ft.Text("Inserisci e verifica prima un ID oggetto!", color="red"))
            self._view.update_page()
            return

        dim_comp = self._model.getConnectedComponent(self.sel_obj_id)
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa contiene {dim_comp} vertici."))

        if dim_comp >= 2:
            self._view._ddLun.options = [ft.dropdown.Option(str(n)) for n in range(2, dim_comp + 1)]
            self._view._ddLun.disabled = False
            self._view._btnCerca.disabled = False
        else:
            self._view.txt_result.controls.append(ft.Text("Dimensione insufficiente per cercare cammini.", color="red"))
            self._view._ddLun.disabled = True
            self._view._btnCerca.disabled = True

        self._view.update_page()

    def handleIdOggetto(self, e):
        self._view.txt_result.controls.clear()
        try: self.sel_obj_id = int(self._view._txtIdOggetto.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Inserisci un numero intero valido!", color="red"))
            self._view.update_page()
            return
        if self._model.checkNodeExists(self.sel_obj_id):
            self._view.txt_result.controls.append(ft.Text("Object_id valido!", color="green"))
            self._view._btnCompConnessa.disabled = False
        else:
            self._view.txt_result.controls.append(ft.Text("Object_id non esistente nel grafo!", color="red"))
            self._view._btnCompConnessa.disabled = True
        self._view.update_page()

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()

        if not self._view._ddLun.value:
            self._view.txt_result.controls.append(ft.Text("Seleziona una lunghezza LUN dal menu!", color="red"))
            self._view.update_page()
            return

        lun = int(self._view._ddLun.value)
        cammino_ottimo, peso_totale = self._model.cerca_cammino(self.sel_obj_id, lun)

        if not cammino_ottimo:
            self._view.txt_result.controls.append(ft.Text("Nessun cammino trovato.", color="orange"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino massimo trovato! Peso totale: {peso_totale}", color="green"))
            cammino_ordinato = sorted(cammino_ottimo, key=lambda x: x.object_name)
            for obj in cammino_ordinato:
                self._view.txt_result.controls.append(ft.Text(f"{obj.object_name} (ID: {obj.object_id})"))
        self._view.update_page()

