import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceAlbum = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        durataTxt =self._view._txtInDurata.value
        if durataTxt=="":
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Inserire una durata",color="red"))
            self._view._page.update()
            return

        try:
            durata=int(durataTxt)
        except ValueError:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore intero", color="red"))
            self._view._page.update()
            return

        if durata <0:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Inserire una durata maggiore di zero",color="red"))
            self._view._page.update()
            return
        self._grafo=self._model.buildGraph(durata)
        # for n in self._grafo.nodes:
        #     self._view._ddAlbum.options.append(
        #         ft.dropdown.Option(key=n.AlbumId, data=n.AlbumId, text=n.Title)
        #     )
        # for n in self._grafo.nodes:
        #     self._view._ddAlbum.options.append(
        #         ft.dropdown.Option(key=str(n.AlbumId), text=n.Title, data=n)  # `data=n` è fondamentale
        #     )

        self._fillDD(self._grafo.nodes)

        numNodes, numEdges= self._model.graphDetails()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("Grafo creato!"))
        self._view.txt_result.controls.append(ft.Text(f"#Vertici: {numNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"#Archi: {numEdges}"))
        self._view._btnAnalisiComp.disabled=False
        self._view.update_page()






    # def getSelectedAlbum(self, e):
    #     for n in self._grafo.nodes:
    #         print(n)
    #         self._view._ddAlbum.options.append(ft.dropdown.Option(data=n.AlbumId, text=n.Title, on_click=self.readDDAlbum))
    #         #self._view._ddAlbum.controls.options(ft.Text(nodes))
    #     self._view.update_page()

    # def getSelectedAlbum(self, e):


    # def readDDAlbum(self,e):
    #     if e.control.data is None:
    #         return
    #     else:
    #         self._choiceAlbum=e.control.data

    def handleAnalisiComp(self, e):
        # self._choiceAlbum = e.control.data
        self.sommaTempi=0
        # print(self._choiceAlbum)
        compConnessa= nx.node_connected_component(self._grafo,self._choiceDD )
        for a in compConnessa:
            self.sommaTempi+=a.dTot

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Componente connessa - {self._choiceDD.Title}"))
        self._view.txt_result.controls.append(ft.Text(f"Dimensione componente = {len(compConnessa)}"))
        self._view.txt_result.controls.append(ft.Text(f"Durata componente =  {self.sommaTempi}"))
        self._view.update_page()

    # def handleGetSetAlbum(self, e):
    #     sogliaTot=self._view._txtInSoglia.value
    #
    #     if sogliaTot == "":
    #         self._view.txt_result.clean()
    #         self._view.txt_result.controls.append(ft.Text("Inserire una soglia totale", color="red"))
    #         self._view._page.update()
    #         return
    #
    #     try:
    #         sogliaTot = int(sogliaTot)
    #     except ValueError:
    #         self._view.txt_result.clean()
    #         self._view.txt_result.controls.append(ft.Text("Inserire un valore intero", color="red"))
    #         self._view._page.update()
    #         return
    #
    #     if sogliaTot < 0:
    #         self._view.txt_result.clean()
    #         self._view.txt_result.controls.append(ft.Text("Inserire una durata maggiore di zero", color="red"))
    #         self._view._page.update()
    #         return
    #
    #     compConnessa = nx.node_connected_component(self._grafo, self._choiceDD)  # <<< NUOVO >>>
    #     compConnessa = list(compConnessa)
    #     compConnessa.sort(key=lambda a: a.dTot)  # <<< NUOVO >>>
    #
    #     self._bestSet = []  # <<< NUOVO >>>
    #     self._search([], compConnessa, sogliaTot, 0, self._choiceDD)  # <<< NUOVO >>>
    #
    #     durataFinale = sum(a.dTot for a in self._bestSet)  # <<< NUOVO >>>
    #
    #     self._view.txt_result.clean()
    #     self._view.txt_result.controls.append(ft.Text("Set di album selezionato:", color="green"))  # <<< NUOVO >>>
    #     for album in self._bestSet:  # <<< NUOVO >>>
    #         self._view.txt_result.controls.append(ft.Text(f"{album.Title} - {album.dTot} min"))  # <<< NUOVO >>>
    #     self._view.txt_result.controls.append(ft.Text(f"Totale album: {len(self._bestSet)}"))  # <<< NUOVO >>>
    #     self._view.txt_result.controls.append(ft.Text(f"Durata complessiva: {durataFinale} min"))  # <<< NUOVO >>>
    #     self._view.update_page()

    def _search(self, parziale, rimanenti, soglia, somma):
        if somma > soglia:
            return

        if len(parziale) > len(self._bestSet):
            self._bestSet = list(parziale)

        for album in rimanenti:
            if album in parziale:
                continue
            parziale.append(album)
            self._search(parziale, rimanenti, soglia, somma + album.dTot)
            parziale.pop()

    def _readDDValue(self, e):
        if e.control.data is None:
            print("error in reading dd")
            self._choiceDD = None
        self._choiceDD = e.control.data

    def _fillDD(self, listOfNodes):
        ciao=list(self._grafo.nodes)
        ciao.sort(key=lambda x: x.Title)
        listOfOptions = map(lambda x: ft.dropdown.Option(text=x.Title,
                                                         on_click=self._readDDValue,
                                                         data=x
                                                         ), listOfNodes)
        # listOfOptions = []
        # for n in listOfNodes:
        #     listOfOptions.append(ft.dropdown.ption(text = n.Title,
        #                                                  on_click= self._readDDValue,
        #                                                  data = n
        #                                                  ))
        self._view._ddAlbum.options = list(listOfOptions)

    def handleGetSetAlbum(self, e):
        sogliaTot = self._view._txtInSoglia.value

        if sogliaTot == "":
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Inserire una soglia totale", color="red"))
            self._view._page.update()
            return

        try:
            sogliaTot = int(sogliaTot)
        except ValueError:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore intero", color="red"))
            self._view._page.update()
            return

        if sogliaTot < 0:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Inserire una durata maggiore di zero", color="red"))
            self._view._page.update()
            return

        if self._choiceDD is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("Selezionare un album dalla tendina", color="red"))
            self._view.update_page()
            return

        compConnessa = list(nx.node_connected_component(self._grafo, self._choiceDD))
        compConnessa.sort(key=lambda a: a.dTot)

        self._bestSet = []

        # ✅ Chiamata corretta: partiamo con a1 già incluso
        self._search([self._choiceDD], compConnessa, sogliaTot, self._choiceDD.dTot)

        durataFinale = sum(a.dTot for a in self._bestSet)

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("Set di album selezionato:", color="green"))
        for album in self._bestSet:
            self._view.txt_result.controls.append(ft.Text(f"{album.Title} - {album.dTot} min"))
        self._view.txt_result.controls.append(ft.Text(f"Totale album: {len(self._bestSet)}"))
        self._view.txt_result.controls.append(ft.Text(f"Durata complessiva: {durataFinale} min"))
        self._view.update_page()

