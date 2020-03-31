import tkinter as tk
import pickle as pi
import os
from threading import Timer
from math import ceil

class SelectPartie(tk.Tk):
	"""
	Menu de lancement du jeu.
	Hérite de la classe des fenêtres Tkinter.
	"""
	def __init__(self):
		tk.Tk.__init__(self)
		self.title("Menu principal - Echecs et Maths")
		self.tk.call("wm", "iconphoto", self._w, tk.PhotoImage(file = os.path.join(".", "data/images/B_Reine.gif")))
		self.selectName()
	
	def selectName(self):
		"""
		Choix de la partie à charger / créer.
		"""
		self.resizable(False, False)
		choix_saves = os.listdir("data/saves")
		choix_saves.remove("global")
		self.choisir_save = tk.Label(self, text = "Sélectionnez la partie à charger", font = "Arial 14 bold")
		self.choisir_save.grid(row = 0, column = 0, columnspan = 2, sticky = "NSEW")
		self.choosen_save = tk.StringVar()
		self.liste_saves = tk.Listbox(self, listvariable = self.choosen_save, font = "Arial 12", bg = "white", height = 5, relief = tk.RAISED, selectmode = tk.SINGLE)
		self.liste_saves.insert(tk.END, *choix_saves)
		self.liste_saves.grid(row = 1, column = 0, rowspan = 3, sticky = "NSEW")
		self.charger = tk.Button(self, text = "Charger", fg = "green", bg = "#c8f0c5", font = "Arial 12", command = lambda: self.chargerPartie(nom = self.liste_saves.get(self.liste_saves.curselection())))
		self.charger.grid(row = 1, column = 1, sticky = "NSEW")
		self.supprimer = tk.Button(self, text = "Supprimer", fg = "red", bg = "#f2c0c0", font = "Arial 12", command = lambda: self.effacerPartie(self.liste_saves.get(self.liste_saves.curselection())))
		self.supprimer.grid(row = 2, column = 1, sticky = "NSEW")
		self.quitter = tk.Button(self, text = "Quitter", fg = "gray", bg = "#c5c1c1", font = "Arial 12", command = self.destroy)
		self.quitter.grid(row = 3, column = 1, sticky = "NSEW")
		self.nouvelle_partie = tk.Button(self, text = "Nouvelle partie", fg = "blue", bg = "#1496f3", font = "Arial 12", command = self.chargerPartie)
		self.nouvelle_partie.grid(row = 5, column = 0, columnspan = 2, sticky = "NSEW")
		self.nouvelle_partie.focus_set()
		self.nouvelle_partie.bind("<Return>", self.chargerPartie)
		self.protocol("WM_DELETE_WINDOW", self.vide)
	
	def effacerPartie(self, nom):
		"""
		Confirmation de la suppression d'une partie 'nom'.
		"""
		self.confirmer = tk.Toplevel(self)
		self.confirmer.title("Êtes-vous sûr ? - Echecs et Maths")
		self.confirmer.grab_set()
		self.confirmer.resizable(False, False)
		tk.Label(self.confirmer, text = "Êtes-vous sûr de vouloir supprimer cette sauvegarde ?", font = "Arial 12 bold").grid(row = 0, column = 0, columnspan = 2, sticky = "NSEW")
		tk.Button(self.confirmer, text = "Oui", fg = "green", bg = "#c8f0c5", font = "Arial 10", command = lambda: self.effacerPartie2(nom)).grid(row = 1, column = 0, sticky = "NSEW")
		self.non = tk.Button(self.confirmer, text = "Non", fg = "red", bg = "#f2c0c0", font = "Arial 10", command = self.fermerConfirmer)
		self.non.grid(row = 1, column = 1, sticky = "NSEW")
		self.non.focus_set()
		self.non.bind("<Return>", self.fermerConfirmer)
	
	def effacerPartie2(self, nom):
		"""
		Gestion de la suppression d'une partie 'nom'.
		"""
		self.confirmer.destroy()
		os.remove("data/saves/{nom}".format(nom = nom))
		self.liste_saves.delete(0, tk.END)
		choix_saves = os.listdir("data/saves")
		choix_saves.remove("global")
		self.liste_saves.insert(tk.END, *choix_saves)
	
	def fermerConfirmer(self, event = None):
		"""
		Destruction de la fenêtre de confirmation de suppression.
		"""
		self.confirmer.destroy()
	
	def chargerPartie(self, event = None, nom = None):
		"""
		Gestion du chargement d'une partie 'nom', et lecture des variables stocké dans 'data/saves/<nom>'.
		Mettre 'nom' à 'None' pour utiliser les paramètres par défaut à ainsi créer une nouvelle partie.
		"""
		self.destroy()
		if nom == None:
			data = {"pieces": {"A1": "B_Tour", "B1": "B_Cav", "C1": "B_Fou", "D1": "B_Roi", "E1": "B_Reine", "F1": "B_Fou", "G1": "B_Cav", "H1": "B_Tour", "A2": "B_Pion", "B2": "B_Pion", "C2": "B_Pion", "D2": "B_Pion", "E2": "B_Pion", "F2": "B_Pion", "G2": "B_Pion", "H2": "B_Pion", "A8": "N_Tour", "B8": "N_Cav", "C8": "N_Fou", "D8": "N_Roi", "E8": "N_Reine", "F8": "N_Fou", "G8": "N_Cav", "H8": "N_Tour", "A7": "N_Pion", "B7": "N_Pion", "C7": "N_Pion", "D7": "N_Pion", "E7": "N_Pion", "F7": "N_Pion", "G7": "N_Pion", "H7": "N_Pion"}, "pieces_eliminees": {"B": [], "N": []}, "i": {"B": 0, "N": 0}, "joueur": "B", "temps": {"sec": 0, "min": 0, "heure": 0}}
			nom_partie = "Nouvelle partie"
		else:
			nom_partie = nom
			with open("data/saves/{nom}".format(nom = nom_partie), "rb") as data:
				data = pi.Unpickler(data).load()
		
		Echecs_et_Maths = EchecsEtMaths(None, data, nom_partie) # Classe principale gérant une partie.
		Echecs_et_Maths.mainloop()
	
	def vide(self):
		"""
		Fonction vide pour empêcher la fermeture d'une fenêtre.
		Rappel de la méthode : .protocol("WM_DELETE_WINDOW", self.vide)
		"""
		pass

class EchecsEtMaths(tk.Tk):
	"""
	Gestion de la partie.
	Hérite de la classe des fenêtres Tkinter.
	
	'data' correspond aux données de la partie chargée, dans un dictionnaire :
	- 'pieces' : Liste des pièces et de leur case ;
	- 'pieces_eliminees' : Liste des pièces éliminées selon leur couleur ;
	- 'i' : Index des pièces éliminées ;
	- 'joueur' : Couleur du joueur à qui c'est le tour de jouer ;
	- 'temps' : Durée totale de la partie.
	
	'name' désigne le nom de la partie.
	"""
	def __init__(self, parent, data, name):
		tk.Tk.__init__(self, parent)
		self.parent = parent
		try:
			self.pieces = data["pieces"]
		except KeyError:
			self.pieces = {"A1": "B_Tour", "B1": "B_Cav", "C1": "B_Fou", "D1": "B_Roi", "E1": "B_Reine", "F1": "B_Fou", "G1": "B_Cav", "H1": "B_Tour", "A2": "B_Pion", "B2": "B_Pion", "C2": "B_Pion", "D2": "B_Pion", "E2": "B_Pion", "F2": "B_Pion", "G2": "B_Pion", "H2": "B_Pion", "A8": "N_Tour", "B8": "N_Cav", "C8": "N_Fou", "D8": "N_Roi", "E8": "N_Reine", "F8": "N_Fou", "G8": "N_Cav", "H8": "N_Tour", "A7": "N_Pion", "B7": "N_Pion", "C7": "N_Pion", "D7": "N_Pion", "E7": "N_Pion", "F7": "N_Pion", "G7": "N_Pion", "H7": "N_Pion"}
		try:
			self.pieces_eliminees = data["pieces_eliminees"]
		except KeyError:
			self.pieces_eliminees = {"B": [], "N": []}
		try:
			self.i = data["i"]
		except KeyError:
			self.i = {"B": 0, "N": 0}
		try:
			self.joueur = data["joueur"]
		except KeyError:
			self.joueur = "B"
		try:
			self.temps = data["temps"]
		except KeyError:
			self.temps = {"sec": 0, "min": 0, "heure": 0}
		self.nom_partie = name
		self.title("{nom} ({heure:02}:{min:02}:{sec:02}) - Echecs et Maths".format(nom = self.nom_partie, heure = self.temps["heure"], min = self.temps["min"], sec = self.temps["sec"]))
		self.tk.call("wm", "iconphoto", self._w, tk.PhotoImage(file = os.path.join(".", "data/images/B_Reine.gif")))
		self.timer()
		self.initialisation()
	
	def timer(self):
		"""
		Fonction qui gère le temps de la partie.
		S'execute toutes les secondes à partir du moment où elle est lancée.
		"""
		self.temps["sec"] += 1
		if self.temps["sec"] == 60:
			self.temps["min"] += 1
			self.temps["sec"] = 0
		if self.temps["min"] == 60:
			self.temps["heure"] += 1
			self.temps["min"] = 0
		self.title("{nom} ({heure:02}:{min:02}:{sec:02}) - Echecs et Maths".format(nom = self.nom_partie, heure = self.temps["heure"], min = self.temps["min"], sec = self.temps["sec"]))
		Timer(1, self.timer).start()
	
	def initialisation(self):
		"""
		Initialisation des variables, des objets et de la fenêtre.
		"""
		self.grid()
		self.grab_set()
		self.focus_set()
		
		self.plateau = tk.Frame(self, width = ceil(4*self.winfo_screenheight()/5), height = ceil(4*self.winfo_screenheight()/5))
		self.plateau.grid_propagate(0)
		self.plateau.grid(row = 1, column = 0, sticky = "NSEW")
		
		self.table = tk.Frame(self, width = ceil(2*self.winfo_screenheight()/5), height = ceil(4*self.winfo_screenheight()/5))
		self.table.grid_propagate(0)
		self.table.grid(row = 1, column = 1, sticky = "NSEW")
		
		self.lettres = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}
		self.chiffres = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8}
		self.pieces_images = {"Vide": tk.PhotoImage(file = "data/images/Vide.gif"), "B_Pion": tk.PhotoImage(file = "data/images/B_Pion.gif"), "B_Tour": tk.PhotoImage(file = "data/images/B_Tour.gif"), "B_Cav": tk.PhotoImage(file = "data/images/B_Cav.gif"), "B_Reine": tk.PhotoImage(file = "data/images/B_Reine.gif"), "B_Fou": tk.PhotoImage(file = "data/images/B_Fou.gif"), "B_Roi": tk.PhotoImage(file = "data/images/B_Roi.gif"), "N_Pion": tk.PhotoImage(file = "data/images/N_Pion.gif"), "N_Tour": tk.PhotoImage(file = "data/images/N_Tour.gif"), "N_Cav": tk.PhotoImage(file = "data/images/N_Cav.gif"), "N_Reine": tk.PhotoImage(file = "data/images/N_Reine.gif"), "N_Fou": tk.PhotoImage(file = "data/images/N_Fou.gif"), "N_Roi": tk.PhotoImage(file = "data/images/N_Roi.gif")}
		
		self.tour_a_tour = {"B": "N", "N": "B"}
		self.couleurs = {"B": "blanches", "N": "noires"}
		self.liste_choix = ["Tour", "Cav", "Reine", "Fou"]
		
		self.deplacement_pion = {"N_Pion": {"C": [-2, -1], "S": "7"}, "B_Pion": {"C": [1, 2], "S": "2"}}
		self.deplacement_cav_roi = {"Cav": {"L": [2, 2, -2, -2, 1, -1, 1, -1], "C": [1, -1, 1, -1, 2, 2, -2, -2]}, "Roi": {"L": [-1, -1, -1, 0, 0, 1, 1, 1], "C": [-1, 0, 1, -1, 1, -1, 0, 1]}}
		self.deplacement_tour_fou_reine = {"Tour": {"L": [0, 0, 1, -1, 0, 0, 0, 0], "C": [1, -1, 0, 0, 0, 0, 0, 0]}, "Fou": {"L": [1, 1, -1, -1, 0, 0, 0, 0], "C": [1, -1, 1, -1, 0, 0, 0, 0]}, "Reine": {"L": [0, 0, 1, -1, 1, 1, -1, -1], "C": [1, -1, 0, 0, 1, -1, 1, -1]}}
		
		self.cases = {}
		self.ancienne_case = {}
		self.image_piece = []
		self.case_selectionnee = ""
		for i in range(64):
			self.image_piece.append("")
		
		self.initialisationPlateau()
		self.initialisationTable()
		
		for i in range(4):
			self.table.grid_columnconfigure(i, weight = 5)
		for i in range(8):
			self.table.grid_rowconfigure(i, weight = 5)
		
		for C in range(8):
			tk.Label(self.plateau, text = "{lettre}".format(lettre = self.lettres[C+1]), font = "Arial 10").grid(row = 0, column = C+1, sticky = "NSEW")
		
		for L in range(8):
			tk.Label(self.plateau, text = "{chiffre}".format(chiffre = L+1), font = "Arial 10").grid(row = L+1, column = 0, sticky = "NSEW")
		
		self.plateau.grid_columnconfigure(0, weight = 1)
		self.plateau.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(0, weight = 4)
		
		self.labelVariable = tk.StringVar()
		self.labelVariable.set("Aux pièces {couleur} de jouer.".format(couleur = self.couleurs[self.joueur]))
		label = tk.Label(self, textvariable = self.labelVariable, font = "Arial 12 bold underline")
		label.grid(row = 0, column = 0, sticky = "EW")
		
		tk.Label(self, text = "Pièces éliminées :", font = "Arial 12 underline").grid(row = 0, column = 1, sticky = "NSEW")
		
		self.protocol("WM_DELETE_WINDOW", self.fermer)
		self.resizable(False, False)
		self.update()
	
	def fermer(self):
		"""
		Gestion de la fermeture de la fenêtre et du menu de sauvegarde.
		"""
		self.confirmation_fermer = tk.Toplevel(self)
		self.confirmation_fermer.title("Sauvegarder - Echecs et Maths")
		self.confirmation_fermer.grab_set()
		self.confirmation_fermer.focus_set()
		self.confirmation_fermer.resizable(False, False)
		for i in range(3):
			self.confirmation_fermer.grid_columnconfigure(i, weight = 1)
		for i in range(2):
			self.confirmation_fermer.grid_rowconfigure(i, weight = i + 1)
		self.ask_save_txt = tk.StringVar()
		self.ask_save_txt.set("Sauvegarder la partie en cours ?")
		self.ask_save = tk.Label(self.confirmation_fermer, textvariable = self.ask_save_txt, font = "Arial 14 bold")
		self.ask_save.grid(row = 0, column = 0, columnspan = 3, sticky = "NSEW")
		self.non = tk.Button(self.confirmation_fermer, text = "Non", fg = "red", bg = "#f2c0c0", font = "Arial 12", command = self.destroy)
		self.non.grid(row = 1, column = 0, sticky = "NSEW")
		self.oui = tk.Button(self.confirmation_fermer, text = "Oui", fg = "green", bg = "#c8f0c5", font = "Arial 12", command = self.chooseName)
		self.oui.grid(row = 1, column = 1, sticky = "NSEW")
		self.oui.focus_set()
		self.oui.bind("<Return>", self.chooseName)
		self.annuler = tk.Button(self.confirmation_fermer, text = "Annuler", fg = "gray", bg = "#c5c1c1", font = "Arial 12", command = self.confirmation_fermer.destroy)
		self.annuler.grid(row = 1, column = 2, sticky = "NSEW")
		self.confirmation_fermer.protocol("WM_DELETE_WINDOW", self.vide)
	
	def chooseName(self, event = None):
		"""
		Choix du nom de la sauvegarde.
		"""
		self.ask_save_txt.set("Nom de la partie :")
		self.non.destroy()
		self.oui.destroy()
		self.nom = tk.StringVar()
		self.saisir_nom = tk.Entry(self.confirmation_fermer, textvariable = self.nom, font = "Arial 12")
		self.saisir_nom.grid(row = 1, column = 0, columnspan = 2, sticky = "NSEW")
		self.saisir_nom.focus_set()
		if self.nom_partie != None:
			self.nom.set(self.nom_partie)
			self.saisir_nom.select_range(0, tk.END)
		self.valider = tk.Button(self.confirmation_fermer, text = "Valider", fg = "green", bg = "#c8f0c5", font = "Arial 12", command = self.sauvegarderPartie)
		self.valider.grid(row = 2, column = 0, columnspan = 3, sticky = "NSEW")
		self.saisir_nom.bind("<Return>", self.sauvegarderPartie)
	
	def sauvegarderPartie(self, event = None):
		"""
		Vérification du nom choisi.
		"""
		liste_saves = os.listdir("data/saves")
		if self.nom.get() == "global":
			self.ask_save_txt.set("Nom impossible. Nom de la partie :")
			self.saisir_nom.focus_set()
			self.saisir_nom.select_range(0, tk.END)
		elif self.nom.get() in liste_saves:
			self.ecraser_partie = tk.Toplevel(self.confirmation_fermer)
			self.ecraser_partie.title("Êtes-vous sûr ? - Echecs et Maths")
			tk.Label(self.ecraser_partie, text = "Une sauvegarde portant ce nom existe déjà. Voulez-vous la remplacer ?", font = "Arial 14").grid(row = 0, column = 0, columnspan = 2, sticky = "NSEW")
			tk.Button(self.ecraser_partie, text = "Non", fg = "red", bg = "#f2c0c0", font = "Arial 12", command = self.ecraser_partie.destroy).grid(row = 1, column = 0, sticky = "NSEW")
			self.ecraser = tk.Button(self.ecraser_partie, text = "Oui", fg = "green", bg = "#c8f0c5", font = "Arial 12", command = self.sauvegarderPartie2)
			self.ecraser.grid(row = 1, column = 1, sticky = "NSEW")
			self.ecraser_partie.protocol("WM_DELETE_WINDOW", self.vide)
			self.ecraser_partie.grab_set()
			self.ecraser.focus_set()
			self.ecraser.bind("<Return>", self.sauvegarderPartie2)
			self.ecraser_partie.mainloop()
		else:
			self.sauvegarderPartie2()
	
	def sauvegarderPartie2(self, event = None):
		"""
		Sauvegarde réelle des données de la partie.
		"""
		saved_data = {"pieces": self.pieces, "pieces_eliminees": self.pieces_eliminees, "i": self.i, "joueur": self.joueur, "temps": self.temps}
		try:
			with open("data/saves/{nom}".format(nom = self.nom.get()), "wb") as data:
				pi.Pickler(data).dump(saved_data)
		except FileNotFoundError:
			open("data/saves/{nom}".format(nom = self.nom.get()), "w").close()
			self.sauvegarderPartie2()
		self.destroy()
	
	def initialisationPlateau(self):
		"""
		Création visuelle du plateau et de ses cases.
		"""
		for L in range(8):
			for C in range(8):
				if (L % 2 == 0 and C % 2 == 0) or (L % 2 == 1 and C % 2 == 1):
					couleur = "white"
				else:
					couleur = "black"
				if self.caseOccupee("{colonne}{ligne}".format(colonne = self.lettres[C+1], ligne = L+1)):
					piece = self.pieces["{colonne}{ligne}".format(colonne = self.lettres[C+1], ligne = L+1)]
				else:
					piece = "Vide"
				self.cases["{colonne}{ligne}".format(colonne = self.lettres[C+1], ligne = L+1)] = tk.Button(self.plateau, image = self.pieces_images[piece], command = lambda l = L+1, c = self.lettres[C+1]: self.detectCaseClic("{colonne}{ligne}".format(colonne = c,ligne = l)), bg = couleur)
				self.cases["{colonne}{ligne}".format(colonne = self.lettres[C+1], ligne = L+1)].grid(row = L+1, column = C+1, sticky = "NSEW")
				
				self.plateau.grid_columnconfigure(C+1, weight = 5)
				self.plateau.grid_rowconfigure(L+1, weight = 5)
	
	def initialisationTable(self):
		"""
		Affichage des pièces déjà éliminées au lancement d'une partie.
		"""
		for c in self.couleurs.keys():
			for i in range(16):
				if c == "B":
					R = 8 - ceil((i + 0.5) / 4)
				else:
					R = ceil((i + 0.5) / 4) - 1
				try:
					p = self.pieces_eliminees[c][i]
				except IndexError:
					p = "Vide"
				tk.Label(self.table, image = self.pieces_images[p]).grid(row = R, column = int(4 * ((i / 4) - int(i / 4))), sticky = "NSEW")
	
	def eliminerPiece(self, piece):
		"""
		Détection et affichage de l'élimination d'une pièce 'piece' du plateau.
		"""
		if piece[0] == "B":
			R = 8 - ceil((self.i[piece[0]] + 0.5) / 4)
		else:
			R = ceil((self.i[piece[0]] + 0.5) / 4) - 1
		tk.Label(self.table, image = self.pieces_images[piece]).grid(row = R, column = int(4 * ((self.i[piece[0]] / 4) - int(self.i[piece[0]] / 4))), sticky = "NSEW")
		self.i[piece[0]] += 1
	
	def detectCaseClic(self, case):
		"""
		Détection du clic sur un case 'case'.
		Fonction liée à chacune des cases du plateau.
		"""
		if self.cases[case].cget("bg") == "green":
			self.deplacerPiece(self.case_from, case)
			for i in self.ancienne_case.keys():
				self.colorierCase(i, self.ancienne_case[i])
			self.ancienne_case = {}
		else:
			for i in self.ancienne_case.keys():
				self.colorierCase(i, self.ancienne_case[i])
			self.ancienne_case = {}
			if case != self.case_selectionnee:
				self.case_selectionnee = case
				try:
					if self.pieces[case][0] == self.joueur and self.caseOccupee(case):
						self.clickPiece(case, self.pieces[case][2:])
				except KeyError:
					pass
			else:
				self.case_selectionnee = ""
	
	def clickPiece(self, case, piece):
		"""
		Gestion de la coloration des cases sur lesquelles une pièce 'piece' sur une case 'case' peut ou non se déplacer.
		"""
		self.case_from = case
		
		if piece == "Pion": # Cas d'un pion.
			if self.pieces[case][0] == "N":
				x = self.deplacement_pion[self.pieces[case]]["C"][1]
			else:
				x = self.deplacement_pion[self.pieces[case]]["C"][0]
			if case[1] == self.deplacement_pion[self.pieces[case]]["S"]:
				for i in range(len(self.deplacement_pion[self.pieces[case]]["C"])):
					temp_case = int(case[1]) + self.deplacement_pion[self.pieces[case]]["C"][i]
					temp_case = "{lettre}{chiffre}".format(lettre = case[0], chiffre = temp_case)
					if not(self.caseOccupee(temp_case)) and ((self.pieces[case][0] == "B" and not(self.caseOccupee("{lettre}{chiffre}".format(lettre = case[0], chiffre = int(case[1]) + self.deplacement_pion[self.pieces[case]]["C"][0])))) or (self.pieces[case][0] == "N" and not(self.caseOccupee("{lettre}{chiffre}".format(lettre = case[0], chiffre = int(case[1]) + self.deplacement_pion[self.pieces[case]]["C"][1]))))):
						self.colorierCase(temp_case, "green")
			else:
				try:
					temp_case = int(case[1]) + x
					temp_case = "{lettre}{chiffre}".format(lettre = case[0], chiffre = temp_case)
					try:
						test_case_vide = self.pieces[temp_case]
					except KeyError:
						self.colorierCase(temp_case, "green")
				except KeyError:
					pass
			try:
				case_droite = "{lettre}{chiffre}".format(lettre = self.lettres[self.alphaNb(case[0]) + 1], chiffre = int(case[1]) + x)
			except KeyError:
				case_droite = "None"
			try:
				case_gauche = "{lettre}{chiffre}".format(lettre = self.lettres[self.alphaNb(case[0]) - 1], chiffre = int(case[1]) + x)
			except KeyError:
				case_gauche = "None"
			cases_cote = [case_droite, case_gauche]
			for case_test in cases_cote:
				try:
					if (self.pieces[case_test][0] == "B" and self.pieces[case][0] == "N") or (self.pieces[case_test][0] == "N" and self.pieces[case][0] == "B"):
						self.colorierCase(case_test, "green")
				except KeyError:
					pass
		
		elif piece == "Tour" or piece == "Fou" or piece == "Reine": # Cas d'une tour, d'un fou ou d'une reine.
			for j in range(8):
				for i in range(7):
					try:
						temp_case = "{lettre}{chiffre}".format(lettre = self.lettres[self.alphaNb(case[0]) + self.deplacement_tour_fou_reine[piece]["L"][j] * (i + 1)], chiffre = int(case[1]) + self.deplacement_tour_fou_reine[piece]["C"][j] * (i + 1))
						if not(self.caseOccupee(temp_case)):
							self.colorierCase(temp_case, "green")
						else:
							if (self.pieces[case][0] == "N" and self.pieces[temp_case][0] == "B") or (self.pieces[case][0] == "B" and self.pieces[temp_case][0] == "N"):
								self.colorierCase(temp_case, "green")
							break
					except KeyError:
						break
		
		elif piece == "Cav" or piece == "Roi": # Cas d'un cavalier ou d'un roi.
			for i in range(8):
				try:
					temp_case = "{lettre}{chiffre}".format(lettre = self.lettres[self.alphaNb(case[0]) + self.deplacement_cav_roi[piece]["L"][i]], chiffre = int(case[1]) + self.deplacement_cav_roi[piece]["C"][i])
					if not(self.caseOccupee(temp_case)) or (self.pieces[case][0] == "N" and self.pieces[temp_case][0] == "B") or (self.pieces[case][0] == "B" and self.pieces[temp_case][0] == "N"):
						self.colorierCase(temp_case, "green")
				except KeyError:
					pass
		
	def deplacerPiece(self, case_from, case_to):
		"""
		Gestion du déplacement d'une pièce d'une case 'case_from' à une case 'case_to' (lors du clic sur une case verte).
		"""
		try:
			self.pieces_eliminees[self.pieces[case_to][0]].append(self.pieces[case_to])
			piece_eliminee = self.pieces[case_to]
			elimination = True
		except KeyError:
			elimination = False
		img_piece_from = self.cases[case_from].cget("image")
		self.cases[case_from].config(image = self.pieces_images["Vide"])
		self.cases[case_to].config(image = img_piece_from)
		self.pieces[case_to] = self.pieces[case_from]
		del self.pieces[case_from]
		
		if (self.pieces[case_to] == "N_Pion" and case_to[1] == "1") or (self.pieces[case_to] == "B_Pion" and case_to[1] == "8"):
			self.choosePion(case_to, self.pieces[case_to][0])
		self.joueur = self.tour_a_tour[self.joueur]
		self.labelVariable.set("Aux pièces {couleur} de jouer.".format(couleur = self.couleurs[self.joueur]))
		
		if elimination == True:
			self.eliminerPiece(piece_eliminee)
	
	def colorierCase(self, case, couleur):
		"""
		Gestion de la coloration d'une case 'case' en couleur 'couleur'.
		"""
		self.ancienne_case[case] = self.cases[case].cget("bg")
		self.cases[case].config(bg = couleur)
	
	def alphaNb(self, lettre):
		"""
		Transformation d'une lettre 'lettre' en son chiffre correspondant.
		"""
		return self.chiffres[lettre]
	
	def nbAlpha(self, nb):
		"""
		Transformation d'un chiffre 'nb' en sa lettre correspondante.
		"""
		return self.lettres[nb]
	
	def caseOccupee(self, case):
		"""
		Détection de l'occupation ou non d'une case 'case'.
		"""
		try:
			test_case_vide = self.pieces[case]
			return True
		except KeyError:
			return False
	
	def choosePion(self, case, couleur):
		"""
		Gestion de la fenêtre permettant de choisir une pièce à la place d'un pion de couleur 'couleur' arrivé en case 'case' (bout de plateau).
		"""
		self.fenetre_choix_pion = tk.Toplevel(self)
		self.fenetre_choix_pion.grab_set()
		self.fenetre_choix_pion.focus_set()
		self.fenetre_choix_pion.resizable(False, False)
		tk.Label(self.fenetre_choix_pion, text = "Choisissez une pièce :", font = "Arial 12 underline").grid(row = 0, column = 0, columnspan = 5)
		self.choix_piece = tk.StringVar()
		for i in range(len(self.liste_choix)):
			tk.Radiobutton(self.fenetre_choix_pion, image = self.pieces_images["{couleur}_{piece}".format(couleur = couleur, piece = self.liste_choix[i])], variable = self.choix_piece, value = self.liste_choix[i], indicatoron = 0).grid(row = 1, column = i, sticky = "NSEW")
			self.fenetre_choix_pion.grid_columnconfigure(i, weight = 4)
			self.fenetre_choix_pion.grid_rowconfigure(i, weight = 4)
		tk.Button(self.fenetre_choix_pion, text = "Valider", font = "Arial 12", fg = "green", command = lambda: self.choosePion2(case, self.choix_piece.get(), couleur)).grid(row = 2, column = 0, columnspan = 5, sticky = "NSEW")
		self.fenetre_choix_pion.protocol("WM_DELETE_WINDOW", self.vide)

	def choosePion2(self, case, choix, couleur):
		"""
		Changement du pion de couleur 'couleur' sur la case 'case' en une piece 'choix'.
		"""
		if choix == "":
			pass
		else:
			self.fenetre_choix_pion.destroy()
			self.pieces[case] = "{couleur}_{choix}".format(couleur = couleur, choix = choix)
			self.cases[case].config(image = self.pieces_images["{couleur}_{choix}".format(couleur = couleur, choix = choix)])
	
	def vide(self):
		"""
		Fonction vide pour empêcher la fermeture d'une fenêtre.
		Rappel de la méthode : .protocol("WM_DELETE_WINDOW", self.vide)
		"""
		pass

if __name__ == "__main__":
	Lancer_Partie = SelectPartie()
	Lancer_Partie.mainloop()
