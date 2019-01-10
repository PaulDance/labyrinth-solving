import random
random.seed()
# Ce fichier donne les fonctions de bases des labyrinthes, telles que créer un labyrinthe, en demander un, le modifier,
# accéder à diverses informations de voisinage, créer des labyrinthes parfaits et imparfaits aléatoirement, déterminer
# la carte des distances de toutes les cases d'un labyrinthe à une case donnée, chercher un chemin de plus courte longeur...


def creerLab(l, h):
	"""Renvoie une matrice h*l aux valeurs initiales False"""
	lab = [[]] * h
	for i in range(h):
		lab[i] = [False] * l
	return lab

def creerLabAv(l, h):
	"""Renvoie un labyrinthe avancé consistant en une matrice où chaque coefficient est un couple
	de booléens indiquant s'il y a un mur respectivement à gauche de la case puis à sa droite."""
	lab = [[]] * (h+1)
	
	lab[0] = [[True, True]]					# Ce premier paquet est pour la première ligne, spéciale.
	for a in range(1, l):
		lab[0].append([False, True])
	lab[0].append([True, False])
	
	for i in range(1, h):
		lab[i] = [[True, False]]			# Celui-là est pour les lignes communes, qui sont identiques
		for b in range(1, l):
			lab[i].append([False, False])
		lab[i].append([True, False])
	
	for c in range(0, l):					# Ce dernier est pour la dernière ligne, spéciale.
		lab[h].append([False, True])
	lab[h].append([False, False])
	
	return lab


def demanderLabAv(l, h):
	"""Demande position par position la valeur de la case du labyrinthe avancé h*l que l'utilisateur souhaite créer, puis le renvoie."""
	lab = creerLabAv(l, h)
	
	for i in range(h):
		for j in range(l):
			ans = input("Case ({0}, {1}), à gauche ?\n".format(i, j))
			
			while ans not in ["y", "n"]:
				print("Entrée non valable")
				ans = input("Case ({0}, {1}), à gauche ?\n".format(i, j))
			
			lab[i][j][0] = ans == "y"
			ans = input("Case ({0}, {1}), en haut ?\n".format(i, j))
			
			while ans not in ["y", "n"]:
				print("Entrée non valable")
				ans = input("Case ({0}, {1}), en haut ?\n".format(i, j))
			
			lab[i][j][1] = ans == "y"
	
	return lab


def creerLabAvAleatoire(l, h, r = 30):
	"""Renvoie un labyrinthe avancé totalement aléatoire, r est la probabilité de présence des murs, en %"""
	lab = creerLabAv(l, h)
	
	for i in range(0, len(lab)-1):
		for j in range(0, len(lab[0])-1):
			if random.random() <= r / 100:
				lab[i][j][0] = True
			if random.random() <= r / 100:
				lab[i][j][1] = True
	
	return lab


def voisinsAccessiblesAv(i, j, lab):
	"""Renvoie la liste des voisins directs de la case (i,j) qui lui sont accessibles,
		i.e. pour lesquels il n'y a pas de mur entre eux et (i,j)."""
	r = []
	
	if 0 <= i < len(lab) - 1 and 0 <= j < len(lab[0]) - 1:
		if not lab[i][j][1]:
			r.append([i - 1, j])
		if not lab[i][j + 1][0]:
			r.append([i, j + 1])
		if not lab[i + 1][j][1]:
			r.append([i + 1, j])
		if not lab[i][j][0]:
			r.append([i, j - 1])
	else:
		raise Exception(i, "et/ou", j, "ne sont pas des positions de cases possibles du labyrinthe avancé.")
	
	return r


def insererSiNouveau(x, l):
	"""Insère l'élément x dans la liste l seulement si x n'est pas déjà dans l."""
	if x not in l:
		l.append(x)


def insererSiNouveaux(l2, l1):
	"""Ajoute tous les éléments de la liste l2 non présent dans l1 à la fin de l1."""
	for a in l2:
		insererSiNouveau(a, l1)


def elementAuHasard(l):
	"""Renvoie un élément de la liste l choisi au hasard."""
	return l[random.randint(0, len(l) - 1)]


def caseAuHasard(lab):
	"""Renvoie un couple de position choisi au hasard par rapport aux dimensions du labyrinthe lab donné."""
	return random.randint(0, len(lab)), random.randint(0, len(lab[0]))


def ajouterDesMursPartout(lab):
	"""Prend en entrée n'importe quel labyrinthe avancé lab et le remplit entièrement en murs."""
	for i in range(0, len(lab) - 1):
		for j in range(0, len(lab[0]) - 1):
			lab[i][j] = [True, True]


def retirerUnMur(pos1, pos2, lab):
	"""Retire le mur qui se trouve entre les position pos1 et pos2 du labyrinthe avancé lab."""
	if pos1[0] == pos2[0] - 1:
		lab[pos2[0]][pos2[1]][1] = False
	elif pos1[0] == pos2[0] + 1:
		lab[pos1[0]][pos1[1]][1] = False
	elif pos1[1] == pos2[1] - 1:
		lab[pos2[0]][pos2[1]][0] = False
	elif pos1[1] == pos2[1] + 1:
		lab[pos1[0]][pos1[1]][0] = False


def voisinsPotentiels(i, j, lab):
	"""Renvoie la liste des voisins directs de la case (i,j) du labyrinthe lab."""
	if i < 0 or i >= len(lab) - 1 or j < 0 and j >= len(lab) - 1:
		raise Exception(i, "et/ou", j, "ne sont pas des positions de cases possibles du labyrinthe avancé.")
	
	l = [[i-1, j], [i, j+1], [i+1, j], [i, j-1]]
	r = []
	for a in range(0, 4):
		if 0 <= l[a][0] < len(lab) - 1 and 0 <= l[a][1] < len(lab[0]) - 1:
			r.append(l[a])
	
	return r


def creerLabParfait(l, h):
	"""Renvoie un labyrinthe parfait aléatoire de dimensions h*l, grâce à une variante de l'algorithme de Prim"""
	lab = creerLabAv(l, h)
	ajouterDesMursPartout(lab)
	casesAccess = []						# 'casesAcces' = cases accessibles
	a = random.randint(0, h - 1)
	b = random.randint(0, l - 1)
	
	ite = creerLab(l, h)				# On crée une grille vide,
	ite[a][b] = True					# qui aura des valeurs vraies pour dire : 'ite' = visitée
	casesAccess.extend(voisinsPotentiels(a, b, lab))
	
	caseHas = []
	newPot = []
	visit = []
	
	while casesAccess != []:
		caseHas = list(elementAuHasard(casesAccess))		# 'has' = case au hasard
		ite[caseHas[0]][caseHas[1]] = True
		
		newPot = voisinsPotentiels(caseHas[0], caseHas[1], lab)		# 'newPot' = Nouveaux Potentiels
		visit.clear()						# 'visit' = visités
		
		for a in newPot:
			if ite[a[0]][a[1]]:
				visit.append(a)
			else:
				casesAccess.append(a)
		
		newCasesAccess = []
		for b in casesAccess:				# Cette partie là est pour éliminer les cases qui auraient pu devenir visitées.
			if not ite[b[0]][b[1]]:
				newCasesAccess.append(b)
		
		casesAccess = list(newCasesAccess)
		retirerUnMur(caseHas, visit[random.randint(0, len(visit) - 1)], lab)
	
	return lab


def creerLabParfaitRB(l, h):
	"""Renvoie un labyrinthe parfait aléatoire selon un algorithme de type 'depth first', nommée 'Recursive backtracker'."""
	lab = creerLabAv(l, h)
	ajouterDesMursPartout(lab)
	cellulesVisitees = creerLab(l, h)
	pileCases = []
	i, j = random.randint(0, h - 1), random.randint(0, l - 1)
	pileCases.append([i, j])
	cellulesVisitees[i][j] = True
	
	while pileCases != []:				# Tant qu'on a encore des cases à visiter,
		celluleEnCours = pileCases.pop()
		voisinsEnCours = [voisin for voisin in voisinsPotentiels(celluleEnCours[0], celluleEnCours[1], lab) if not cellulesVisitees[voisin[0]][voisin[1]]]
		
		if voisinsEnCours != []:		# si la case où l'on se trouve a au moins un voisin non visité,
			celluleSuivante = elementAuHasard(voisinsEnCours)						# on en choisit un au hasard,
			retirerUnMur(celluleEnCours, celluleSuivante, lab)						# on casse le mur entre elle et nous,
			cellulesVisitees[celluleSuivante[0]][celluleSuivante[1]] = True			# on la marque visitée,
			pileCases.extend([celluleEnCours, celluleSuivante])						# et on rajoute les deux cases à la pile.
	
	return lab


def creerLabPresqueParfait(l, h, r = 20):
	"""Renvoie un labyrinthe presque parfait aléatoire de dimensions h*l en retirant les murs d'un labyrinthe parfait aléatoire avec une probabilité de r%"""
	lab = creerLabParfait(l, h)
	
	for i in range(len(lab) - 1):
		for j in range(len(lab[0]) - 1):
			if lab[i][j][0] and j != 0:
				if random.random() <= r / 100:
					lab[i][j][0] = False
			
			if lab[i][j][1] and i != 0:
				if random.random() <= r / 100:
					lab[i][j][1] = False
	
	return lab


def carteDistances(i, j, lab):
	"""Utilise une version simplifiée de l'algorithme de Dijkstra pour renvoyer la carte des distances de chaque case du labyrinthe lab à la case (i,j)"""
	carte = creerLab(len(lab[0]) - 1, len(lab) - 1)
	vis = list(carte)				# Une liste qui indique quelle case est déjà visitée.
	
	def voisins(i, j, lab):			# Une fonction qui renvoie les voisins accessibles non visités d'une case aux positions i et j dans un labyrinthe lab.
		l = []
		for b in voisinsAccessiblesAv(i, j, lab):
			if not vis[b[0]][b[1]]:
				l.append(b)
		
		return l
	
	vis[i][j] = True				# On visite la case de départ.
	dis = 0
	lCases = [[i, j]]				# Une liste de cases à visiter.
	newLCases = []					# Une liste qui va uniquement contenir les cases dont on va créer la liste de voisins.
	
	while lCases != []:
		dis += 1
		
		for a in lCases:
			for b in voisins(a[0], a[1], lab):
				vis[b[0]][b[1]] = True  	# On 'visite' ici.
				carte[b[0]][b[1]] = dis
				newLCases.append(b)
			
		lCases.clear()
		lCases = list(newLCases)	# On remplace ici lCases par newLCases pour ne travailler que sur les cases
		newLCases.clear()			# intéressantes et donc pour que la condition de la boucle while soit correcte.
	
	carte[i][j] = 0					# On applique à la case de départ une distance de 0.
	return carte


def cheminPlusCourt(i1, j1, i2, j2, lab):
	"""Renvoie la liste des cases composant un chemin de plus courte longeur entre les cases (i1,j1) et (i2,j2) du labyrinthe lab."""
	def voisin(i, j, lab, dis):		# Une fonction qui renvoie un des voisins accessibles à la distance = distance en cours - 1.
		for b in voisinsAccessiblesAv(i, j, lab):
			if carte[b[0]][b[1]] == dis - 1:
				return b
	
	carte = carteDistances(i2, j2, lab)
	chemin = [[i1, j1]]
	i = i1
	j = j1
	dis = carte[i1][j1]
	
	while i != i2 or j != j2:
		v = voisin(i, j, lab, dis)
		i = v[0]
		j = v[1]
		chemin.append([i, j])
		dis -= 1
	
	chemin.append([i2, j2])
	return chemin