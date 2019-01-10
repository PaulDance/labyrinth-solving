CREATE TABLE Données (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	labId INT NOT NULL,
	largeurLab INT,
	hauteurLab INT,
	methodId INT,
	i1 INT,
	j1 INT,
	i2 INT,
	j2 INT,
	stepsNbr INT
) ;

CREATE TABLE Algorithmes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	nom TEXT
) ;

INSERT INTO Algorithmes (nom) VALUES ("Aléatoire") ;
INSERT INTO Algorithmes (nom) VALUES ("Chemin plus court") ;
INSERT INTO Algorithmes (nom) VALUES ("Main gauche") ;
INSERT INTO Algorithmes (nom) VALUES ("Pledge") ;
INSERT INTO Algorithmes (nom) VALUES ("Trémaux") ;