from Labyrinthes import *
# Ce présent fichier décrit les algorithme de résolutions de labyrinthe, créés dans le ficher Labyrinthes.py .
# Ils sont implémentés de la manière suivante : puisque l'interface graphique tkinter nécéssite de réaliser son
# affichage étape par étape (du fait de la fonction <myCanvas>.after(f, t)), il faut donc coder une fonction
# qui donne le pas à réaliser à partir d'une position en cours et d'autres paramètres liés à la méhtodes utilisée.
# Plus précisément, ces fonctions prennent au moins en entrée un labyrinthe avancé lab et une position (i,j) de lab,
# et renvoient la prochaine position que l'algorithme concerné génère.


# Les intelligences artificielles :

def prochainePositionIATenirGauche(i, j, orientation, lab):
	"""Renvoie la prochaine position selon la méthode de la main gauche à partir de (i,j) dans <lab> avec l'orientation <orientation>."""
	if orientation == "N":							# Structure générale :
		if not lab[i][j][0]:						# On essaie de tourner à gauche
			return i, j - 1, "W", False				# si on peut, on y va;
		elif not lab[i][j][1]:						# sinon, on essaie d'aller tout droit
			return i - 1, j, "N", False				# si on peut, on y va;
		else:										# sinon,
			return i, j, "E", True					# on tourne a droite.
				
	if orientation == "W":					# Pareil dans les autres cas d'orientation : juste d'autres coordonnées.
		if not lab[i + 1][j][1]:
			return i + 1, j, "S", False
		elif not lab[i][j][0]:
			return i, j - 1, "W", False
		else:
			return i, j, "N", True
	
	if orientation == "S":
		if not lab[i][j + 1][0]:
			return i, j + 1, "E", False
		elif not lab[i + 1][j][1]:
			return i + 1, j, "S", False
		else:
			return i, j, "W", True
	
	if orientation == "E":
		if not lab[i][j][1]:
			return i - 1, j, "N", False
		elif not lab[i][j + 1][0]:
			return i, j + 1, "E", False
		else:
			return i, j, "S", True



def prochainePositionIAInvariante(i, j, orientation, lab):
	"""Renvoie la prochaine position à partir de (i,j) dans <lab> avec l'orientation <orientation>
		selon une méthode que j'ai créée, mais qui ne fonctionne pas du tout : elle tourne en rond."""
	if orientation == "N":
		if not lab[i][j][1]:
			return i - 1, j, "N", False
		else:
			return i, j, "W", True
	if orientation == "W":
		if not lab[i][j][0]:
			return i, j - 1, "W", False
		else:
			return i, j, "S", True
	if orientation == "S":
		if not lab[i + 1][j][1]:
			return i + 1, j, "S", False
		else:
			return i, j, "E", True
	if orientation == "E":
		if not lab[i][j + 1][0]:
			return i, j + 1, "E", False
		else:
			return i, j, "N", True



def prochainePositionIAMouvementAleatoire(i, j, lab):
	"""Renvoie une prochaine position aléatoire à partir de (i,j) dans <lab>."""
	NWSE = ("N", "W", "S", "E")
	direction = NWSE[random.randint(0, 3)]
	
	if direction == "N":
		if not lab[i][j][1]:
			return i - 1, j, False
		else:
			return i, j, True
	if direction == "W":
		if not lab[i][j][0]:
			return i, j - 1, False
		else:
			return i, j, True
	if direction == "S":
		if not lab[i + 1][j][1]:
			return i + 1, j, False
		else:
			return i, j, True
	if direction == "E":
		if not lab[i][j + 1][0]:
			return i, j + 1, False
		else:
			return i, j, True



def prochainePositionIAPledge(i, j, orientation, counter, lab):
	"""Renvoie la prochaine position indiquée par l'algorithme de Pledge à partir de (i,j) dans <lab>, avec l'<orientation> et le <counter>."""
	if orientation == 'N':
		if counter == 0:											# Si on est pas encore rentré dans l'algorithme de Pledge,
			if not lab[i][j][1]:									# S'il n'y a pas de mur en face,
				return i - 1, j, 'N', 0, False						# on avance.
			else:
				return i, j, 'W', -1, True							# Sinon, on tourne à gauche.
		else:														# Si on est entré = conpteur non nul,
			if not lab[i][j + 1][0]:								# S'il n'y a pas de mur à droite,
				return i, j + 1, 'E', counter + 1, False			# on tourne et on y va.
			elif not lab[i][j][1]:									# Sinon, s'il n'y a pas de mur en face,
				return i - 1, j, 'N', counter, False				# on avance.
			else:
				return i, j, 'W', counter - 1, False				# Sinon, on tourne à gauche.
	
	if orientation == 'W':											# Même idée.
		if counter == 0:
			if not lab[i][j][0]:
				return i, j - 1, 'W', 0, False
			else:
				return i, j, 'S', -1, True
		else:
			if not lab[i][j][1]:
				return i - 1, j, 'N', counter + 1, False
			elif not lab[i][j][0]:
				return i, j - 1, 'W', counter, False
			else:
				return i, j, 'S', counter - 1, False
	
	if orientation == 'S':											# Idem.
		if counter == 0:
			if not lab[i + 1][j][1]:
				return i + 1, j, 'S', 0, False
			else:
				return i, j, 'E', -1, True
		else:
			if not lab[i][j][0]:
				return i, j - 1, 'W', counter + 1, False
			elif not lab[i + 1][j][1]:
				return i + 1, j, 'S', counter, False
			else:
				return i, j, 'E', counter - 1, False
	
	if orientation == 'E':											# Idem.
		if counter == 0:
			if not lab[i][j + 1][0]:
				return i, j + 1, 'E', 0, False
			else:
				return i, j, 'N', -1, True
		else:
			if not lab[i + 1][j][1]:
				return i + 1, j, 'S', counter + 1, False
			elif not lab[i][j + 1][0]:
				return i, j + 1, 'E', counter, False
			else:
				return i, j, 'N', counter - 1, False



def orientationOpposee(orientation):
	"""Renvoie l'orientation cardinale opposée à <orientation> donnée en entrée."""
	if orientation == "N":
		return "S"
	elif orientation == "E":
		return "W"
	elif orientation == "S":
		return "N"
	else:
		return "E"


def orientationAssociee(i, j, pos):
	"""Renvoie l'orientation nécéssaire pour se déplacer de (i, j) vers <pos>."""
	if pos[0] == i - 1 and pos[1] == j:
		return "N"
	elif pos[0] == i and pos[1] == j + 1:
		return "E"
	elif pos[0] == i + 1 and pos[1] == j:
		return "S"
	else:
		return "W"

def positionAssociee(i, j, orientation):
	"""Renvoie la position que l'on atteint en partant de (i,j) avec l'<orientation>."""
	if orientation == "N":
		return i - 1, j
	elif orientation == "E":
		return i, j + 1
	elif orientation == "S":
		return i + 1, j
	else:
		return i, j - 1


def grilleMarques(lab):
	"""Renvoie une matrice de dictionnaires ayant les dimensions de <lab>. Pour toute case (i,j) de <lab>, le dictionnaire en
		(i,j) a quatre clés : une pour chaque direction ('N' pour nord, 'E' pour est, ...) disponible à partir de la case (i,j).
		A chacune de ces clés est associée une valeur entière comprise entre 0 et 2 appelée marque du chemin désigné."""
	marks = []
	
	for i in range(len(lab) - 1):
		marks.append([])
		
		for j in range(len(lab[0]) - 1):
			marks[i].append({})
			
			for voisin in voisinsAccessiblesAv(i, j, lab):
				marks[i][j][orientationAssociee(i, j, voisin)] = 0
	
	return marks


def prochainePositionIATremaux(i, j, orientation, marques, marquePrec, lab):
	"""Renvoie la prochaine position indiquée par l'algorithme de Trémaux à partir de (i,j) dans <lab>, avec l'<orientation>,
		la grille de marques <marques> la marque <marquePrec> que la personne a retenu depuis le dernier croisement."""
	dictVoisins = list(marques[i][j].keys())															# On récupère les voisins (voir grilleMarques pour la structure).
	random.shuffle(dictVoisins)																			# Si on veut ajouter de l'aléatoire aux choix arbitraires.
	
	if len(dictVoisins) == 1:																			# Si on est pas à un croisement,
		if marquePrec <= 1:
			return prochainePositionIATenirGauche(i, j, orientation, lab) + tuple([marquePrec + 1])		# on utilise la main gauche,
		else:
			return prochainePositionIATenirGauche(i, j, orientation, lab) + tuple([2])					# et on augmente la marque en cours
	
	elif len(dictVoisins) == 2:
		return prochainePositionIATenirGauche(i, j, orientation, lab) + tuple([marquePrec])				# si on fait demi-tour, mais sans dépasser 2.
	
	else:
		marques[i][j][orientationOpposee(orientation)] = marquePrec										# Sinon, c'est qu'on vient d'un croisement,
		marksCount = 0																					# qu'on est passé par des non-carrefours,
		
		for orVoisin in dictVoisins:																	# et qu'on vient d'arriver sur un nouveaux carrefour -> on le marque.
			if marques[i][j][orVoisin] >= 1:
				marksCount += 1																			# On compte le nombre de voisins marqué.
		
		if marksCount <= 1:																				# Si seulement d'où on vient est marqué,
			for orVoisin in dictVoisins:
				if marques[i][j][orVoisin] == 0:														# on prend un chemin jamais marqué
					marques[i][j][orVoisin] = 1															# et on l'emprunte en marquant ce début.
					return positionAssociee(i, j, orVoisin) + (orVoisin, False, 1)
		else:
			if marques[i][j][orientationOpposee(orientation)] == 1:										# Sinon, si d'où l'on vient n'a qu'une seule marque,
				marques[i][j][orientationOpposee(orientation)] = 2										# on en rajoute une deuxième et on fait demi-tour.
				return positionAssociee(i, j, orientationOpposee(orientation)) + (orientationOpposee(orientation), False, 2)
			else:
				for orVoisin in dictVoisins:															# Sinon on emprunte une voie restante ayant un minimum de marques,
					if marques[i][j][orVoisin] == 0:
						marques[i][j][orVoisin] = 1														# en la marquant
						return positionAssociee(i, j, orVoisin) + (orVoisin, False, 1)
				else:
					for orVoisin in dictVoisins:
						if marques[i][j][orVoisin] == 1:
							marques[i][j][orVoisin] = 2
							return positionAssociee(i, j, orVoisin) + (orVoisin, False, 2)				# adéquatement.