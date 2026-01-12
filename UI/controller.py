import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD = None

    def handleCreaGrafo(self, e):
        dMinText = self._view._txtInDurata.value
        if dMinText == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione valore minimo di durata non inserito.", color="red"))
            return
        try:
            dMin = int(dMinText)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione valore inserito non valido", color="red"))
            return

        self._model.buildGraph(dMin)
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"il grafo è costituti da numero di nodi : {n} e un numero archi: {a}"))
        self._fillDD(self._model.getAllNodes())


        self._view.update_page()


    def handleAnalisiComp(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione Album non selezionato", color="red"))
            return
        size, dTotCC = self._model.getInfoConnessa(self._choiceDD)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceDD}, ha {size} nodi e una durata totale {dTotCC}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        pass

    def _fillDD(self, listOfNodes):
        listOfNodes.sort(key= lambda x: x.Title)
        listOfOptions = map(lambda x: ft.dropdown.Option(text= x.Title,
                                                         on_click= self._readDDValue,
                                                         data=x ), listOfNodes)
        # se no posso fare cosi
        """
        listOfOptions = []
        for n in listOfNodes:
            listOfOptions.append(ft.dropdown.Option(text= n.Titile,
                                                         on_click= self._readDDValue,
                                                         data=n ))
                                                        """

        self._view._ddAlbum.options = list(listOfOptions)

    def _readDDValue(self, e):
        if e.control.data is None:
            print("Errore")
            self._choiceDD = None
        self._choiceDD = e.control.data