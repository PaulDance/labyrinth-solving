import sqlite3, os, tqdm, pylab, numpy
from scipy import stats
from decimal import Decimal
from scipy.optimize import least_squares
from Exploration import *
# Ce fichier permet d'utiliser les fichiers Labyrinthes.py, Exploration.py, "Script DB percolation.sql", "Script DB méthodes.sql",
# "Résultats sur parfaits.sqlite", "Résultats sur imparfaits.sqlite" et "Tests percolation.sqlite" pour résoudre un labyrinthe
# selon un certaine méthode, de créer des bases de données, de réaliser de nombreux tests du nombre de pas que requiert une méthode
# pour les stocker ensuite dans une base de donnée SQLite, et enfin d'afficher certaines analyse des calculs sauvegardés.


# Liste complète de toute les IA implémentées :
listeNomsIA = ["Aléatoire", "Chemin plus court", "Main gauche", "Pledge", "Trémaux"]


def resoudrePar(nomIA, i1, j1, i2, j2, lab):
	"""Renvoie le nombre de pas qu'a nécessité la méthode <nomIA> en partant de (i1, j1) dans <lab> pour arriver en (i2, j2)."""
	if nomIA == "Chemin plus court":
		return len(cheminPlusCourt(i1, j1, i2, j2, lab))
	else:
		steps = 1
		i, j = i1, j1
		orientation = "N"
		surPlace = False
		
		if nomIA == "Aléatoire":
			while i != i2 or j != j2:
				i, j, surPlace = prochainePositionIAMouvementAleatoire(i, j, lab)
				
				if not surPlace:
					steps += 1
			
			return steps
		
		elif nomIA == "Main gauche":
			while i != i2 or j != j2:
				i, j, orientation, surPlace = prochainePositionIATenirGauche(i, j, orientation, lab)
				
				if not surPlace:
					steps += 1
			
			return steps
		
		elif nomIA == "Pledge":
			counter = 0
			
			while i != i2 or j != j2:
				i, j, orientation, counter, surPlace = prochainePositionIAPledge(i, j, orientation, counter, lab)
				
				if not surPlace:
					steps += 1
			
			return steps
		
		elif nomIA == "Trémaux":
			marquePrec = 0
			marques = grilleMarques(lab)
			
			while i != i2 or j != j2:
				i, j, orientation, surPlace, marquePrec = prochainePositionIATremaux(i, j, orientation, marques, marquePrec, lab)
				
				if not surPlace:
					steps += 1
				
			return steps
		
		else:
			raise Exception("'{}' n'est pas une méthode de résolution connue.".format(nomIA))


def creerBaseDonneesMethodes(nomFichier = "Résultats.sqlite"):
	"""Prend en entrée un <nomfichier> SQLite puis crée une base de données SQLite vide mais comprenant la structure décrite par 'Script DB méthodes.sql'"""
	connexion = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier)
	curseur = connexion.cursor()
	
	with open(os.path.dirname(os.path.realpath(__file__)) + "\\Script DB méthodes.sql", mode = 'r', encoding = "utf-8") as file:
		curseur.executescript(file.read())
	
	connexion.commit()
	curseur.close()
	connexion.close()


def realiserTests(N, largeur, hauteur, i1, j1, i2, j2, nomFichier = "Résultats.sqlite", listeIA = listeNomsIA, labParfait = True, r = 20):
	"""Permet de réaliser N tests de résolution de labyrinthes (im)parfaits aléatoires pour des dimensions <hauteur>*<largeur> en partant
		de (i1,j1) pour arriver en (i2,j2), puis stocker ces résultats (nombre de pas, nom de la méthode, dimensions, ...) dans une
		base de donnée SQLite <nomFichier>, selon plusieurs méthodes données dans <listeIA>"""
	if not os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier):
		creerBaseDonneesMethodes(nomFichier)		# On crée la DB si elle n'existe pas
	
	connexion = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier)
	curseur = connexion.cursor()
	
	try:											# On essaie de récupérer le dernier identifiant généré.
		previousLastLabId = curseur.execute("SELECT labId FROM Données").fetchall()[-1][0]
	except IndexError:								# Si on peut, c'est que la table des données n'est pas vide,
		previousLastLabId = 0						# sinon, on la remplit comme une première fois.
	
	for iD in range(1, N + 1):						# Enfin, on réalise les tests souhaités.
		if labParfait:
			lab = creerLabParfait(largeur, hauteur)
		else:
			lab = creerLabPresqueParfait(largeur, hauteur, r)
		
		for IA in listeIA:
			steps = resoudrePar(IA, i1, j1, i2, j2, lab)
			curseur.execute(''' INSERT INTO Données (labId, largeurLab, hauteurLab, methodId, i1, j1, i2, j2, stepsNbr)
								VALUES (?, ?, ?, (SELECT id FROM Algorithmes
								WHERE nom = ?), ?, ?, ?, ?, ?)''', (iD + previousLastLabId, largeur, hauteur, IA, i1, j1, i2, j2, steps))
	
	connexion.commit()
	curseur.close()
	connexion.close()


def serieTestsCarres(tailleDepart, tailleArrivee, nbrTests, nomFichier = "Résultats.sqlite", listeIA = listeNomsIA, labParfait = True, r = 20):
	"""Réalise des tests de résolution grâce réaliserTests() avec des labyrinthes (im)parfaits carrés et <nbrTests> par taille et la taille
		variant entre <tailleDepart> et <tailleArrivee> pour les sauvegarder ensuite dans la base de donnée SQLite <nomFichier>"""
	for taille in tqdm.trange(tailleDepart, tailleArrivee + 1, desc = "Progress :", dynamic_ncols = True):
		realiserTests(nbrTests, taille, taille, 0, 0, taille - 1, taille - 1, nomFichier, listeIA, labParfait, r)


def analyseResultats(tailleDepart, tailleArrivee, nomFichier = "Résultats.sqlite", listeIA = listeNomsIA, typeAnalyse = "affichage", nbDeci = 5):
	"""Charge les résultats stockés dans la base de donnée SQLite <nomFichier> pour les afficher ou en plus de réaliser des analyses statistiques."""
	if not os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier):
		raise FileNotFoundError
	
	connexion = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier)
	curseur = connexion.cursor()
	dictDonnees = {}
	
	
	for IA in listeIA:
		dictDonnees[IA] = ([], [])							# : ([taille], [nbrPasMoyen])
		
		for taille in range(tailleDepart, tailleArrivee + 1):
			tmp = [element[0] for element in curseur.execute("""SELECT stepsNbr FROM Données WHERE largeurLab = ? AND hauteurLab = ?
			                                                AND methodId = (SELECT id FROM Algorithmes WHERE nom = ?) AND i1 = ? AND j1 = ? AND i2 = ? AND j2 = ?""",
			                                                (taille, taille, IA, 0, 0, taille - 1, taille - 1))]
			
			dictDonnees[IA][0].append(taille)
			dictDonnees[IA][1].append(sum(tmp) / len(tmp))
			tmp.clear()
	
	pylab.close("all")
	pylab.figure("Résultats", figsize = (17, 9))			# Partie présentation grâce à matplotlib (incluant pylab)
	plotsId = []
	
	for IA in listeIA:										# On affiche chaque courbe de données.
		plotsId.append(pylab.plot(dictDonnees[IA][0], dictDonnees[IA][1], label = IA)[0])
	
	if typeAnalyse in ("linéaire", "lin"):					# Si l'on souhaite réaliser des régressions linéaires,
		for IA in listeIA:
			slope, intercept, r_value, p_value, std_err = stats.linregress(dictDonnees[IA][0], dictDonnees[IA][1])
			coeffs = (c[0] + '.' + c[1][0:min(nbDeci, len(c[1]))] for c in (str(Decimal(e)).split('.') for e in (slope, intercept)))
			plotsId.append(pylab.plot(dictDonnees[IA][0], slope * numpy.array(dictDonnees[IA][0]) + intercept, label = "Régression {}; ({}, {})".format(IA, *coeffs))[0])
			
		pylab.title("Régressions linéaires")
	
	elif typeAnalyse in ("quadratique", "quad"):			# ou "quadratiques" c'est-à-dire une parabole,
		for IA in listeIA:
			def f(x, t, y):
				return x[0] * t ** 2 + x[1] * t + x[2] - y
			
			x0 = numpy.array([1, 1, 1])
			t = numpy.array(dictDonnees[IA][0])
			y = numpy.array(dictDonnees[IA][1])
			res = least_squares(f, x0, args = (t, y))		# méthode des moindres carrés SciPy pour n'importe quel modèle.
			
			coeffs = (c[0] + '.' + c[1][0:min(nbDeci, len(c[1]))] for c in (str(Decimal(e)).split('.') for e in res.x))
			plotsId.append(pylab.plot(t, f(res.x, t, 0), label = "Régression {}; ({}, {}, {})".format(IA, *coeffs))[0])
			
		pylab.title("Régressions quadratiques")
	
	elif typeAnalyse in ("affichage", "aff", ""):			# sinon par défaut seulement l'affichage,
		pylab.title("Evolution des algorithmes")			# (gestion du titre ici).
	else:
		raise ValueError("'{}' n'est pas un type d'analyse".format(typeAnalyse))
	
	pylab.xlabel("Taille")
	pylab.ylabel("Nombre de pas moyen")
	pylab.legend(handles = plotsId, loc = "upper left")
	figManager = pylab.get_current_fig_manager()
	figManager.full_screen_toggle()
	pylab.show()
	
	connexion.commit()
	curseur.close()
	connexion.close()


def creerBaseDonneesPercolation(nomFichier = "Résultats.sqlite"):
	"""Prend en entrée un <nomfichier> SQLite puis crée une base de données SQLite vide mais comprenant la structure décrite par 'Script DB percolation.sql'"""
	connexion = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier)
	curseur = connexion.cursor()
	
	with open(os.path.dirname(os.path.realpath(__file__)) + "\\Script DB percolation.sql", mode = 'r', encoding = "utf-8") as file:
		curseur.executescript(file.read())
	
	connexion.commit()
	curseur.close()
	connexion.close()


def testsPercolation(taille, nombreEssais, pasProbaP = 1, nomFichier = "Résultats.sqlite"):
	"""Réalise de nombreuses expériences aléatoires ayant pour succès l'existence d'un chemin entre (0,0) et (-1,-1) dans un labyrinthe
		avancé aléatoire de taille <taille> avec <nombreEssais> d'essais par probabilité de présence des murs et cette proba variant
		entre 0 et 1 avec un pas de <pasProba>"""
	if not os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier):
		creerBaseDonneesPercolation(nomFichier)
	
	connexion = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier)
	curseur = connexion.cursor()
	
	for p in tqdm.tqdm(numpy.arange(0, 100 + pasProbaP, pasProbaP)):
		for test in range(nombreEssais):
			curseur.execute("""INSERT INTO Données (taille, probaP, succes)
							VALUES (?, ?, ?)""",
							(taille, float(p), bool(carteDistances(0, 0, creerLabAvAleatoire(taille, taille, r = float(p)))[taille - 1][taille - 1])))
	
	connexion.commit()
	curseur.close()
	connexion.close()


def afficherResultatsPercolation(taille, nomFichier = "Résultats.sqlite"):
	"""Affiche la courbe du succès moyen en fonction de la probabilité de présence des murs."""
	if not os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier):
		raise FileNotFoundError
	
	connexion = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\" + nomFichier)
	curseur = connexion.cursor()
	
	donnees = list(curseur.execute("SELECT succes, probaP FROM Données WHERE taille = ? ORDER BY probaP ASC", (taille,)))
	resultats = [[], []]
	tmpProba = donnees[0][1]
	tmpSum = 0
	tmpNum = 0
	
	for couple in donnees:
		if couple[1] > tmpProba:
			resultats[0].append(tmpSum / tmpNum)
			resultats[1].append(tmpProba / 100)
			tmpProba = couple[1]
			tmpSum = tmpNum = 0
		else:
			tmpSum += int(couple[0])
			tmpNum += 1
	
	resultats[1].reverse()
	pylab.close("all")
	pylab.figure("Résultats", figsize = (17, 9))
	
	pylab.plot(resultats[1], resultats[0])
	
	pylab.xlabel("Probabilité de liaison")
	pylab.ylabel("Succès moyen")
	pylab.title("Simulation de percolation sur [|1, {0}|]²".format(taille))
	figManager = pylab.get_current_fig_manager()
	figManager.full_screen_toggle()
	pylab.show()
	
	connexion.commit()
	curseur.close()
	connexion.close()


#serieTestsCarres(150, 200, 20, nomFichier="Résultats sur imparfaits.sqlite", listeIA=["Trémaux"], labParfait=False)
analyseResultats(10, 200, listeIA=["Chemin plus court", "Main gauche", "Pledge", "Trémaux"], nomFichier="Résultats sur imparfaits.sqlite", typeAnalyse="quad")
#testsPercolation(100, 100, pasProbaP=0.1, nomFichier = "Tests Percolation.sqlite")
#afficherResultatsPercolation(100, "Tests Percolation.sqlite")
#["Chemin plus court", "Main gauche", "Pledge", "Trémaux"]