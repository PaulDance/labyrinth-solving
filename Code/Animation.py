import tkinter
from Exploration import *
# Ce présent fichier permet de créer une interface graphique, d'animer les intelligences artificielles crées dans le fichier Exploration.py,
# de tracer un labyrinthe avancé, de créer de manière graphique un labyrinthe avancé, ...

winWidth = 1500				# Réglages de la fenêtre d'affichage.
winHeight = 900

root = tkinter.Tk()			# Initialisation de la fenêtre graphique.
root.title(string = "Labyrinthes")
root.resizable(height = False, width = False)
root.option_add('*tearOff', False)

canvas = tkinter.Canvas(root, width = winWidth, height = winHeight, bg = "white")
canvas.pack()
canvas.focus_set()


# Fonctions utilitaires :

def ajustementsAuto(lab):
	"""Renvoie les paramètres permettant de centrer le labyrinthe et d'avoir les cases du labyrinthes <lab> maximisées pour les dimensions de la fenêtre."""
	lMax = min((float(canvas["width"]) - 10) / (len(lab[0]) - 1), (float(canvas["height"]) - 10) / (len(lab) - 1))
	return (lMax,
	        (float(canvas["height"]) - 10 - (len(lab) - 1) * lMax) / 2 + 6,
	        (float(canvas["width"]) - 10 - (len(lab[0]) - 1) * lMax) / 2 + 6)


def tracerLabAvAuto(lab, modeEdition = False):
	"""Trace le labyrinthe avancé <lab> dans la zone de dessin <canvas>, avec les paramètres optimisés.
		Si <modeEdition> est True, les murs non présents sont affiché en gris clair."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	
	for i in range(len(lab)):
		for j in range(len(lab[0])):
			if lab[i][j][0]:
				canvas.create_line(j * lMax + ajustJ, i * lMax + ajustI, j * lMax + ajustJ, (i + 1) * lMax + ajustI, fill = "black", width = 2 * int(modeEdition) + 1)
			elif modeEdition and i != len(lab) - 1:
				canvas.create_line(j * lMax + ajustJ, i * lMax + ajustI, j * lMax + ajustJ, (i + 1) * lMax + ajustI, fill = "light grey", width = 1)
			if lab[i][j][1]:
				canvas.create_line(j * lMax + ajustJ, i * lMax + ajustI, (j + 1) * lMax + ajustJ, i * lMax + ajustI, fill = "black", width = 2 * int(modeEdition) + 1)
			elif modeEdition and j != len(lab[0]) - 1:
				canvas.create_line(j * lMax + ajustJ, i * lMax + ajustI, (j + 1) * lMax + ajustJ, i * lMax + ajustI, fill = "light grey", width = 1)


def tracerCheminPlusCourt(i1, j1, i2, j2, lab, couleurChemin = "red"):
	"""Trace les segments de couleur <couleurChemin> entres les différentes postion du chemin le plus court entre (i1,j1) et (i2,j2) dans <lab>"""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	chemin = cheminPlusCourt(i1, j1, i2, j2, lab)
	
	for i in range(0, len(chemin) - 1):
		canvas.create_line(chemin[i][1] * lMax + lMax/2 + ajustJ, chemin[i][0] * lMax + lMax/2 + ajustI,
						   chemin[i + 1][1] * lMax + lMax/2 + ajustJ, chemin[i + 1][0] * lMax + lMax/2 + ajustI,
						   fill = couleurChemin, width = lMax / 10, tag = "shortPath")


def tracerCarteDistances(i1, j1, lab):
	"""Affiche dans la fenêtre les distances de chaque case de <lab> à la case (i1, j1)."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	carte = carteDistances(i1, j1, lab)
	
	for i in range(len(carte)):
		for j in range(len(carte[0])):
			canvas.create_text(j * lMax + lMax/2 + ajustJ, i * lMax + lMax/2 + ajustI, text = str(carte[i][j]), fill = "red", tag = "distNum")


def tracerMarques(marques, lab):
	"""Fonction de debugging utile pour vérifier l'implémentation de l'algorithme de Trémaux."""
	canvas.delete("M")
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	
	for i in range(len(marques)):
		for j in range(len(marques[0])):
			canvas.create_text(j * lMax + lMax / 2 + ajustJ, i * lMax + lMax / 2 + ajustI, font = ("Fontana", 15), text = str(marques[i][j]), fill = "black", tag = "M")


def tracerPointsDepartArrivee(i1, j1, i2, j2, lab):
	"""Trace un carré jaune pour le départ en (i1,j1) de <lab> et un carré vert pour l'arrivée en (i2,j2)."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	canvas.create_rectangle(j1 * lMax + lMax/4 + ajustJ, i1 * lMax + lMax/4 + ajustI, j1 * lMax + 3*lMax/4 + ajustJ, i1 * lMax + 3*lMax/4 + ajustI, fill = "yellow", width = 1, tag = "start")
	canvas.create_rectangle(j2 * lMax + lMax/4 + ajustJ, i2 * lMax + lMax/4 + ajustI, j2 * lMax + 3*lMax/4 + ajustJ, i2 * lMax + 3*lMax/4 + ajustI, fill = "lime green", width = 1, tag = "end")


def initialiserPositionIAFleche(i1, j1, lab):
	"""Trace la flèche vers le nord en la position (i1,j1) de <lab>. Sert à l'initialisation de l'animation."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	return canvas.create_polygon(j1 * lMax + lMax/2 + ajustJ, i1 * lMax + lMax/4 + ajustI, j1 * lMax + lMax/4 + ajustJ, i1 * lMax + 3*lMax/4 + ajustI, j1 * lMax + 3*lMax/4 + ajustJ, i1 * lMax + 3*lMax/4 + ajustI, fill = "red", width = 1)


def deplacerIAFleche(IA, i, j, orientation, lab):
	"""Met à jour l'affichage graphique en déplaçant la flèche de la méthode <IA> vers la case (i,j) dans <lab> avec l'orientation <orientation>."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	
	if orientation == "N":			# Mettre la flèche dans le bon sens, pour être plus facilement compréhensible.
		canvas.coords(IA, j * lMax + lMax/2 + ajustJ, i * lMax + lMax/4 + ajustI, j * lMax + lMax/4 + ajustJ, i * lMax + 3*lMax/4 + ajustI, j * lMax + 3*lMax/4 + ajustJ, i * lMax + 3*lMax/4 + ajustI)
	if orientation == "W":
		canvas.coords(IA, j * lMax + lMax/4 + ajustJ, i * lMax + lMax/2 + ajustI, j * lMax + 3*lMax/4 + ajustJ, i * lMax + 3*lMax/4 + ajustI, j * lMax + 3*lMax/4 + ajustJ, i * lMax + lMax/4 + ajustI)
	if orientation == "S":
		canvas.coords(IA, j * lMax + 3*lMax/4 + ajustJ, i * lMax + lMax/4 + ajustI, j * lMax + lMax/4 + ajustJ, i * lMax + lMax/4 + ajustI, j * lMax + lMax/2 + ajustJ, i * lMax + 3*lMax/4 + ajustI)
	if orientation == "E":
		canvas.coords(IA, j * lMax + lMax/4 + ajustJ, i * lMax + lMax/4 + ajustI, j * lMax + lMax/4 + ajustJ, i * lMax + 3*lMax/4 + ajustI, j * lMax + 3*lMax/4 + ajustJ, i * lMax + lMax/2 + ajustI)


def ajouterAuChemin(i, j, surPlace, cheminParcouru, lab, couleur = "blue"):
	"""Ajoute au chemin <cheminParcouru> la position (i,j) de <lab> seulement si <surPlace> == True et trace le segment <couleur> adapté."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	
	if not surPlace:
		cheminParcouru.append([i, j])			# Pour afficher le chemin au fur et à mesure qu'il est parcouru, uniquement s'il y a eu mouvement et non pas dans le cas d'une simple rotation.
		canvas.create_line(cheminParcouru[-1][1] * lMax + lMax / 2 + ajustJ,
						   cheminParcouru[-1][0] * lMax + lMax / 2 + ajustI,
						   cheminParcouru[-2][1] * lMax + lMax / 2 + ajustJ,
						   cheminParcouru[-2][0] * lMax + lMax / 2 + ajustI,
						   fill = couleur, width = lMax / 20, tag = "AIpath")
		del cheminParcouru[0]


def posClickLab(lab, mouseEvent):
	"""Retourne la position (i, j) du labyrinthe <lab> où l'événement souris s'est produit."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	
	for i in range(len(lab)):
		for j in range(len(lab[0])):
			if lMax * i + ajustI <= mouseEvent.y < lMax * (i + 1) + ajustI and lMax * j + ajustJ <= mouseEvent.x < lMax * (j + 1) + ajustJ:
				return (i, j)

def interfaceEdition(h, l, lab = []):
	"""Ouvre une interface graphique permettant de modifier à la souris un labyrinthe avancé initialement vide, et le renvoyer enfin.
		Clic gauche pour le mur de gauche, clic droit pour celui du haut."""
	if lab == []:
		lab = creerLabAv(l, h)
	
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	
	def switchLeftWall(mouseEvent):
		i, j = posClickLab(lab, mouseEvent)
		lab[i][j][0] = not lab[i][j][0]
		canvas.delete("all")
		tracerLabAvAuto(lab, modeEdition = True)
	
	def switchUpWall(mouseEvent):
		i, j = posClickLab(lab, mouseEvent)
		lab[i][j][1] = not lab[i][j][1]
		canvas.delete("all")
		tracerLabAvAuto(lab, modeEdition=True)
	
	root.bind("<Button-1>", switchLeftWall)
	root.bind("<Button-3>", switchUpWall)
	tracerLabAvAuto(lab, modeEdition = True)
	root.mainloop()
	
	return lab


def augmenterVitesseAnimation(event):
	"""Fonction utilisé par l'animation de l'interface graphique quand on appuie au clavier sur la flèche du haut pour l'accélérer."""
	global tempsPause
	if tempsPause >= 11:
		tempsPause -= 10

def diminuerVitesseAnimation(event):
	"""Fonction utilisé par l'animation de l'interface graphique quand on appuie au clavier sur la flèche du haut pour la ralentir."""
	global tempsPause
	tempsPause += 10

def terminerAnimation(event):
	"""Fonction utilisé par l'animation de l'interface graphique quand on appuie au clavier sur entrée pour terminer l'animation."""
	global tempsPause
	tempsPause = 0

def switchPause(event):
	"""Fonction utilisé par l'animation de l'interface graphique quand on appuie au clavier sur espace pour la mettre en pause."""
	global enPause
	enPause = not enPause


# Fonctions principales d'animation des IA :

def animerIACheminPlusCourt(i1, j1, i2, j2, lab, couleurChemin = "light red"):
	"""Prend en entrée une case de départ (i1,j1) et une d'arrivée (i2,j2) dans <lab> et gère l'animation de la méthode du chemin le plus court."""
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	chemin = cheminPlusCourt(i1, j1, i2, j2, lab)
	tracerPointsDepartArrivee(i1, j1, i2, j2, lab)
	IA = canvas.create_oval(j1 * lMax + lMax/4 + ajustJ, i1 * lMax + lMax/4 + ajustI, j1 * lMax + 3*lMax/4 + ajustJ, i1 * lMax + 3*lMax/4 + ajustI, fill = "red", width = 1)
	cheminParcouru = [[i1, j1]]
	index = 0
	
	def Rec():
		nonlocal index
		global tempsPause, enPause
		
		if not enPause:
			if index == len(chemin) - 1:
				return
			else:
				canvas.coords(IA, chemin[index][1] * lMax + lMax/4 + ajustJ, chemin[index][0] * lMax + lMax/4 + ajustI, chemin[index][1] * lMax + 3*lMax/4 + ajustJ, chemin[index][0] * lMax + 3*lMax/4 + ajustI)
				ajouterAuChemin(chemin[index][0], chemin[index][1], False, cheminParcouru, lab, couleurChemin)
				index += 1
				canvas.after(tempsPause, Rec)
		else:
			canvas.after(100, Rec)
	
	Rec()



def animerIATenirGauche(i1, j1, i2, j2, lab, couleurChemin = "blue"):
	"""Prend en entrée une case de départ (i1,j1) et une d'arrivée (i2,j2) dans <lab> et gère l'animation de la méthode de la main gauche."""
	orientation = "N"
	tracerPointsDepartArrivee(i1, j1, i2, j2, lab)
	IA = initialiserPositionIAFleche(i1, j1, lab)
	cheminParcouru = [[i1, j1]]
	i, j = i1, j1
	
	def Rec():
		nonlocal i, j, orientation
		global tempsPause, enPause
		
		if not enPause:
			if i == i2 and j == j2:
				return
			else:
				i, j, orientation, surPlace = prochainePositionIATenirGauche(i, j, orientation, lab)			# Faire la mise à jour des données : position suivante et nouvelle orientation.
				deplacerIAFleche(IA, i, j, orientation, lab)
				ajouterAuChemin(i, j, surPlace, cheminParcouru, lab, couleurChemin)
				canvas.after(tempsPause, Rec)
		else:
			canvas.after(100, Rec)
	
	Rec()



def animerIAInvariante(i1, j1, i2, j2, lab, couleurChemin = "blue"):
	"""Prend en entrée une case de départ (i1,j1) et une d'arrivée (i2,j2) dans <lab> et gère l'animation de la méthode invariante."""
	i, j = i1, j1
	orientation = "N"
	tracerPointsDepartArrivee(i1, j1, i2, j2, lab)
	IA = initialiserPositionIAFleche(i1, j1, lab)
	cheminParcouru = [[i1, j1]]
	
	def Rec():
		nonlocal i, j, orientation
		global tempsPause, enPause
		
		if not enPause:
			if i == i2 and j == j2:
				return
			else:
				i, j, orientation, surPlace = prochainePositionIAInvariante(i, j, orientation, lab)			# Faire la mise à jour des données : position suivante et nouvelle orientation.
				deplacerIAFleche(IA, i, j, orientation, lab)
				ajouterAuChemin(i, j, surPlace, cheminParcouru, lab, couleurChemin)
				canvas.after(tempsPause, Rec)
		else:
			canvas.after(100, Rec)
	
	Rec()



def animerIAMouvementAleatoire(i1, j1, i2, j2, lab, couleurChemin = "pink"):
	"""Prend en entrée une case de départ (i1,j1) et une d'arrivée (i2,j2) dans <lab> et gère l'animation de la méthode aléatoire."""
	i, j = i1, j1
	lMax, ajustI, ajustJ = ajustementsAuto(lab)
	tracerPointsDepartArrivee(i1, j1, i2, j2, lab)
	IA = canvas.create_oval(j1 * lMax + lMax/4 + ajustJ, i1 * lMax + lMax/4 + ajustI, j1 * lMax + 3*lMax/4 + ajustJ, i1 * lMax + 3*lMax/4 + ajustI, fill = "red", width = 1)
	cheminParcouru = [[i1, j1]]
	
	def Rec():
		nonlocal i, j
		global tempsPause, enPause
		
		if not enPause:
			if i == i2 and j == j2:
				return
			else:
				i, j, surPlace = prochainePositionIAMouvementAleatoire(i, j, lab)			# Faire la mise à jour des données : position suivante et nouvelle orientation.
				canvas.coords(IA, j * lMax + lMax/4 + ajustJ, i * lMax + lMax/4 + ajustI, j * lMax + 3*lMax/4 + ajustJ, i * lMax + 3*lMax/4 + ajustI)
				ajouterAuChemin(i, j, surPlace, cheminParcouru, lab, couleurChemin)
				canvas.after(tempsPause, Rec)
		else:
			canvas.after(100, Rec)
	
	Rec()



def animerIAPledge(i1, j1, i2, j2, lab, couleurChemin = "light green"):
	"""Prend en entrée une case de départ (i1,j1) et une d'arrivée (i2,j2) dans <lab> et gère l'animation de l'algorithme de Pledge."""
	i, j = i1, j1
	orientation = "N"
	counter = 0
	tracerPointsDepartArrivee(i1, j1, i2, j2, lab)
	IA = initialiserPositionIAFleche(i1, j1, lab)
	cheminParcouru = [[i1, j1]]
	
	def Rec():
		nonlocal i, j, orientation, counter
		global tempsPause, enPause
		
		if not enPause:
			if i == i2 and j == j2:
				return
			else:
				i, j, orientation, counter, surPlace = prochainePositionIAPledge(i, j, orientation, counter, lab)			# Faire la mise à jour des données : position suivante, nouvelle orientation et nouveau compteur de Pledge.
				deplacerIAFleche(IA, i, j, orientation, lab)
				ajouterAuChemin(i, j, surPlace, cheminParcouru, lab, couleurChemin)
				canvas.after(tempsPause, Rec)
		else:
			canvas.after(100, Rec)
	
	Rec()
	

def animerIATremaux(i1, j1, i2, j2, lab, couleurChemin = "gold"):
	"""Prend en entrée une case de départ (i1,j1) et une d'arrivée (i2,j2) dans <lab> et gère l'animation de l'algorithme de Trémaux."""
	orientation = "S"
	tracerPointsDepartArrivee(i1, j1, i2, j2, lab)
	IA = initialiserPositionIAFleche(i1, j1, lab)
	i, j = i1, j1
	cheminParcouru = [[i1, j1]]
	marques = grilleMarques(lab)
	marquePrec = 0
	
	def Rec():
		nonlocal i, j, orientation, marques, marquePrec
		global tempsPause, enPause
		
		if not enPause:
			if i == i2 and j == j2:
				return
			else:				# Faire la mise à jour des données : position suivante, nouvelle orientation et nouvelle marque en cours. :
				i, j, orientation, surPlace, marquePrec = prochainePositionIATremaux(i, j, orientation, marques, marquePrec, lab)
				deplacerIAFleche(IA, i, j, orientation, lab)
				ajouterAuChemin(i, j, surPlace, cheminParcouru, lab, couleurChemin)
				canvas.after(tempsPause, Rec)
		else:
			canvas.after(100, Rec)
	
	Rec()


def confMenus():
	"""
	A faire :
		Choix génération labyrinthe : vide, aléatoire, parfait, parfaitRB, persque parfait -> à terminer
		Option carte distances -> terminer affichage au bon moment
		Option couleur chemin plus court + terminer affichage chemin plus court au bon moment
	"""
	menuBar = tkinter.Menu(root)			# Barre des menus
	root['menu'] = menuBar
	
	menuLab = tkinter.Menu(menuBar)			# Menu des réglages du labyrinthe.
	menuBar.add_cascade(menu = menuLab, label = "Labyrinthe")
	winLabOpened = False					# Variable sentinelle pour éviter d'ouvrir deux fois la même fenêtre.
	labHeight, labWidth = 20, 30			# Taille par défaut du labyrinthe.
	iDepart, jDepart, iArrivee, jArrivee = 0, 0, labHeight - 1, labWidth - 1
	lab = creerLabAv(labWidth, labHeight)	# Labyrinthe vide par défaut.
	tracerLabAvAuto(lab)
	tracerPointsDepartArrivee(iDepart, jDepart, iArrivee, jArrivee, lab)
	
	def winLab():							# Ouvre une petite fenêtre pour régler la taille du labyrinthe.
		nonlocal winLabOpened, labHeight, labWidth, iDepart, jDepart, iArrivee, jArrivee, lab
		
		if not winLabOpened:
			winLabOpened = True
			top = tkinter.Toplevel(root)
			top.geometry("180x100+{0}+{1}".format(root.winfo_x() + 10, root.winfo_y() + 60))
			top.resizable(width = False, height = False)
			top.title("Lab")
			top.focus_set()
			
			def killWinLab():
				nonlocal winLabOpened
				winLabOpened = False
				top.destroy()
			
			top.protocol("WM_DELETE_WINDOW", killWinLab)
			
			tkinter.Label(top, text = "Hauteur").pack(anchor = "w")
			entryHeight = tkinter.Entry(top)
			entryHeight.insert(0, labHeight)
			entryHeight.pack()
			
			tkinter.Label(top, text = "Largeur").pack(anchor = "w")
			entryWidth = tkinter.Entry(top)
			entryWidth.insert(0, labWidth)
			entryWidth.pack()
			
			def actAndQuit():
				nonlocal labHeight, labWidth, lab, iDepart, jDepart, iArrivee, jArrivee
				labWidth, labHeight = int(entryWidth.get()), int(entryHeight.get())
				lab = creerLabParfait(labWidth, labHeight)
				canvas.delete("all")
				tracerLabAvAuto(lab)
				
				if not (0 <= iDepart <= labHeight - 1 and 0 <= jDepart <= labWidth - 1 and 0 <= iArrivee <= labHeight - 1 and 0 <= jArrivee <= labWidth - 1):
					iDepart, jDepart, iArrivee, jArrivee = 0, 0, labHeight - 1, labWidth - 1
				
				tracerPointsDepartArrivee(iDepart, jDepart, iArrivee, jArrivee, lab)
				
				if checkCheminPlusCourt.get():
					tracerCheminPlusCourt(iDepart, jDepart, iArrivee, jArrivee, lab)
				
				killWinLab()
			
			okButton = tkinter.Button(top, text = "OK", command = actAndQuit)
			okButton.pack()
	
	def pointLabStartEnd():
		nonlocal iDepart, jDepart, iArrivee, jArrivee, lab
		
		def setStart(mouseEvent):
			nonlocal iDepart, jDepart, iArrivee, jArrivee, lab
			
			try: iDepart, jDepart = posClickLab(lab, mouseEvent)
			except: pass
			
			canvas.delete("start")
			canvas.delete("end")
			tracerPointsDepartArrivee(iDepart, jDepart, iArrivee, jArrivee, lab)
		
		def setEnd(mouseEvent):
			nonlocal iDepart, jDepart, iArrivee, jArrivee, lab
			
			try: iArrivee, jArrivee = posClickLab(lab, mouseEvent)
			except: pass
			
			canvas.delete("start")
			canvas.delete("end")
			tracerPointsDepartArrivee(iDepart, jDepart, iArrivee, jArrivee, lab)
		
		def freeBinds(event):
			root.unbind("<Button-1>")
			root.unbind("<Button-3>")
			root.unbind("<Escape>")
			
			if checkCheminPlusCourt.get():
				canvas.delete("shortPath")
				tracerCheminPlusCourt(iDepart, jDepart, iArrivee, jArrivee, lab)
			
			if checkCarteDistances.get():
				canvas.delete("distNum")
				tracerCarteDistances(iArrivee, jArrivee, lab)
		
		root.bind("<Button-1>", setStart)
		root.bind("<Button-3>", setEnd)
		root.bind("<Escape>", freeBinds)
		tracerPointsDepartArrivee(iDepart, jDepart, iArrivee, jArrivee, lab)
	
	
	menuLab.add_command(label = "Taille...", command = winLab)
	menuLab.add_command(label = "Départ et arrivée...", command = pointLabStartEnd)
	menuLabType = tkinter.Menu(menuLab)
	menuLab.add_cascade(menu = menuLabType, label = "Type")
	checkLabType = tkinter.StringVar(value = "empty")
	menuLabType.add_radiobutton(label = "Vide", variable = checkLabType, value = "empty")
	menuLabType.add_radiobutton(label = "Parfait", variable = checkLabType, value = "perfect")
	menuLabType.add_radiobutton(label = "Parfait RB", variable = checkLabType, value = "perfectRB")
	menuLabType.add_radiobutton(label = "Presque parfait", variable = checkLabType, value = "almostPerfect")
	
	
	menuDisplay = tkinter.Menu(menuBar)
	menuBar.add_cascade(menu = menuDisplay, label = "Affichage")
	checkCheminPlusCourt = tkinter.BooleanVar(value = True)
	menuDisplay.add_checkbutton(label = "Chemin le plus court", variable = checkCheminPlusCourt, onvalue = True, offvalue = False,
								command = lambda: tracerCheminPlusCourt(iDepart, jDepart, iArrivee, jArrivee, lab) if checkCheminPlusCourt.get() else canvas.delete("shortPath"))
	checkCarteDistances = tkinter.BooleanVar(value = False)
	menuDisplay.add_checkbutton(label = "Carte des distances", variable = checkCarteDistances, onvalue = True, offvalue = False,
								command = lambda: tracerCarteDistances(iArrivee, jArrivee, lab) if checkCarteDistances.get() else canvas.delete("distNum"))
	
	menuBar.add_separator()
	winIAOpened = False
	
	def winIA():
		nonlocal winIAOpened
		
		if not winIAOpened:
			winIAOpened = True
			top = tkinter.Toplevel(root)
			top.geometry("180x100+{0}+{1}".format(root.winfo_x() + 10, root.winfo_y() + 60))
			top.resizable(width = False, height = False)
			top.title("IA")
			top.focus_set()
			
			def killWinIA():
				nonlocal winIAOpened
				winIAOpened = False
				top.destroy()
			
			top.protocol("WM_DELETE_WINDOW", killWinIA)
			
			buttonAlea = tkinter.Checkbutton(top, text = "Aléatoire", variable = checkAlea, onvalue = True, offvalue = False)
			buttonMainGauche = tkinter.Checkbutton(top, text = "Main Gauche", variable = checkMainGauche, onvalue = True, offvalue = False)
			buttonPledge = tkinter.Checkbutton(top, text = "Pledge", variable = checkPledge, onvalue = True, offvalue = False)
			buttonTremaux = tkinter.Checkbutton(top, text = "Trémaux", variable = checkTremaux, onvalue = True, offvalue = False)
			
			buttonAlea.pack(anchor = "w")
			buttonMainGauche.pack(anchor = "w")
			buttonPledge.pack(anchor = "w")
			buttonTremaux.pack(anchor = "w")
	
	menuBar.add_command(label = "IA", command = winIA)
	menuBar.add_separator()
	
	menuIAAlea = tkinter.Menu(menuBar)
	menuBar.add_cascade(menu = menuIAAlea, label = "Aléatoire")
	checkAlea = tkinter.BooleanVar(value = False)
	menuIAAlea.add_checkbutton(label = "Activée", variable = checkAlea, onvalue = True, offvalue = False)
	menuCouleurAlea = tkinter.Menu(menuIAAlea)
	menuIAAlea.add_cascade(menu = menuCouleurAlea, label = "Couleur")
	couleurAlea = tkinter.StringVar(value = "pink")
	menuCouleurAlea.add_radiobutton(label = "Par défaut : rose", variable = couleurAlea, value = "pink")
	menuCouleurAlea.add_radiobutton(label = "Bleu", variable = couleurAlea, value = "blue")
	menuCouleurAlea.add_radiobutton(label = "Vert", variable = couleurAlea, value = "light green")
	menuCouleurAlea.add_radiobutton(label = "Rouge", variable = couleurAlea, value = "red")
	menuCouleurAlea.add_radiobutton(label = "Jaune", variable = couleurAlea, value = "gold")
	
	menuIAMainGauche = tkinter.Menu(menuBar)
	menuBar.add_cascade(menu = menuIAMainGauche, label = "Main Gauche")
	checkMainGauche = tkinter.BooleanVar(value = False)
	menuIAMainGauche.add_checkbutton(label = "Activée", variable = checkMainGauche, onvalue = True, offvalue = False)
	menuCouleurMainGauche = tkinter.Menu(menuIAMainGauche)
	menuIAMainGauche.add_cascade(menu = menuCouleurMainGauche, label = "Couleur")
	couleurMainGauche = tkinter.StringVar(value = "blue")
	menuCouleurMainGauche.add_radiobutton(label = "Par défaut : bleu", variable = couleurMainGauche, value = "blue")
	menuCouleurMainGauche.add_radiobutton(label = "Vert", variable = couleurMainGauche, value = "light green")
	menuCouleurMainGauche.add_radiobutton(label = "Rouge", variable = couleurMainGauche, value = "red")
	menuCouleurMainGauche.add_radiobutton(label = "Rose", variable = couleurMainGauche, value = "pink")
	menuCouleurMainGauche.add_radiobutton(label = "Jaune", variable = couleurMainGauche, value = "gold")
	
	menuIAPledge = tkinter.Menu(menuBar)
	menuBar.add_cascade(menu = menuIAPledge, label = "Pledge")
	checkPledge = tkinter.BooleanVar(value = False)
	menuIAPledge.add_checkbutton(label = "Activée", variable = checkPledge, onvalue = True, offvalue = False)
	menuCouleurPledge = tkinter.Menu(menuIAPledge)
	menuIAPledge.add_cascade(menu = menuCouleurPledge, label = "Couleur")
	couleurPledge = tkinter.StringVar(value = "light green")
	menuCouleurPledge.add_radiobutton(label = "Par défaut : vert", variable = couleurPledge, value = "light green")
	menuCouleurPledge.add_radiobutton(label = "Bleu", variable = couleurPledge, value = "blue")
	menuCouleurPledge.add_radiobutton(label = "Rouge", variable = couleurPledge, value = "red")
	menuCouleurPledge.add_radiobutton(label = "Rose", variable = couleurPledge, value = "pink")
	menuCouleurPledge.add_radiobutton(label = "Jaune", variable = couleurPledge, value = "gold")
	
	menuIATremaux = tkinter.Menu(menuBar)
	menuBar.add_cascade(menu = menuIATremaux, label = "Trémaux")
	checkTremaux = tkinter.BooleanVar(value = False)
	menuIATremaux.add_checkbutton(label = "Activée", variable = checkTremaux, onvalue = True, offvalue = False)
	menuCouleurTremaux = tkinter.Menu(menuIATremaux)
	menuIATremaux.add_cascade(menu = menuCouleurTremaux, label = "Couleur")
	couleurTremaux = tkinter.StringVar(value = "gold")
	menuCouleurTremaux.add_radiobutton(label = "Par défaut : jaune", variable = couleurTremaux, value = "gold")
	menuCouleurTremaux.add_radiobutton(label = "Bleu", variable = couleurTremaux, value = "blue")
	menuCouleurTremaux.add_radiobutton(label = "Vert", variable = couleurTremaux, value = "light green")
	menuCouleurTremaux.add_radiobutton(label = "Rouge", variable = couleurTremaux, value = "red")
	menuCouleurTremaux.add_radiobutton(label = "Rose", variable = couleurTremaux, value = "pink")
	
	def startAnimation():
		global enPause, tempsPause
		nonlocal lab, iDepart, jDepart, iArrivee, jArrivee
		
		enPause = True
		tempsPause = 201
		
		if checkCheminPlusCourt.get():
			tracerCheminPlusCourt(iDepart, jDepart, iArrivee, jArrivee, lab)
		
		if checkCarteDistances.get():
			tracerCarteDistances(iArrivee, jArrivee, lab)
		
		if checkAlea.get():
			animerIAMouvementAleatoire(iDepart, jDepart, iArrivee, jArrivee, lab, couleurChemin = couleurAlea.get())
		if checkMainGauche.get():
			animerIATenirGauche(iDepart, jDepart, iArrivee, jArrivee, lab, couleurChemin = couleurMainGauche.get())
		if checkPledge.get():
			animerIAPledge(iDepart, jDepart, iArrivee, jArrivee, lab, couleurChemin = couleurPledge.get())
		if checkTremaux.get():
			animerIATremaux(iDepart, jDepart, iArrivee, jArrivee, lab, couleurChemin = couleurTremaux.get())
	
	menuBar.add_separator()
	menuBar.add_command(label = "Démarrer", command = startAnimation)


def confManuelle():
	"""Cette fonction regroupe les lignes utilisées manuellement pour l'animation."""
	hauteur, largeur = 10, 15
	iDepart, jDepart, iArrivee, jArrivee = 0, 0, hauteur - 1, largeur - 1
	
	# print(interfaceEdition(hauteur, largeur))
	labyrinthe = creerLabPresqueParfait(largeur, hauteur)
	tracerLabAvAuto(labyrinthe)
	#tracerPointsDepartArrivee(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)
	#initialiserPositionIAFleche(iDepart, jDepart, labyrinthe)
	#tracerCheminPlusCourt(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)
	#tracerCarteDistances(iArrivee, jArrivee, labyrinthe)
	#animerIACheminPlusCourt(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)
	#animerIATenirGauche(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)
	#animerIAPledge(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)
	#animerIAInvariante(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)
	#animerIAMouvementAleatoire(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)
	#animerIATremaux(iDepart, jDepart, iArrivee, jArrivee, labyrinthe)



root.bind("<Up>", augmenterVitesseAnimation)		# Aux touches fléchées haut et bas sont associées l'accélération de l'animation
root.bind("<Down>", diminuerVitesseAnimation)		# et son ralentissement.
root.bind("<Return>", terminerAnimation)			# La touche entrée sert à terminer le plus tôt possible l'animation (met le temps de pause à 0).
root.bind("<space>", switchPause)					# Espace permet de mettre en pause.

enPause = True										# Pour toutes les IA : une manière d'interrompre ou de reprendre l'animation.
tempsPause = 201									# Pour toutes aussi  : le temps en ms entre chaque mise à jour graphique.

confMenus()											# Ouvre directement une fenêtre avec des menus permettant l'accès graphique aux fonctions majeures.
#confManuelle()										# Regroupe simplement l'utilisation fonction par fonction du module. Incompatible avec les menus.
root.mainloop()										# Démarrage de l'application.