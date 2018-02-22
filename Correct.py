# -*- coding: utf-8 -*-

from math import *
from difflib import SequenceMatcher

#Dictionnaire des coordonnées du clavier pour la prise en compte de la proximité dans le calcul de distance
COORD_LETTRES= {
	'a' : {'y':0,'x':0},
	'z' : {'y':0,'x':1},
	'e' : {'y':0,'x':2},
	'r' : {'y':0,'x':3},
	't' : {'y':0,'x':4},
	'y' : {'y':0,'x':5},
	'u' : {'y':0,'x':6},
	'i' : {'y':0,'x':7},
	'o' : {'y':0,'x':8},
	'p' : {'y':0,'x':9},
	'q' : {'y':1,'x':0},
	's' : {'y':1,'x':1},
	'd' : {'y':1,'x':2},
	'f' : {'y':1,'x':3},
	'g' : {'y':1,'x':4},
	'h' : {'y':1,'x':5},
	'j' : {'y':1,'x':6},
	'k' : {'y':1,'x':7},
	'l' : {'y':1,'x':8},
	'm' : {'y':1,'x':9},
	'w' : {'y':2,'x':0},
	'x' : {'y':2,'x':1},
	'c' : {'y':2,'x':2},
	'v' : {'y':2,'x':3},
	'b' : {'y':2,'x':4},
	'n' : {'y':2,'x':5}
}

#Distance entre 2 lettres
def distance_lettres(a,b):
     X = (COORD_LETTRES[a]['x']-COORD_LETTRES[b]['x'])**2
     Y = (COORD_LETTRES[a]['y']-COORD_LETTRES[b]['y'])**2
     return sqrt(X+Y)

#Distance entre 2  mots
def distance_mots(a,b):
	d=0
	for i in range(0,min(len(a),len(b))) :
		d=d+distance_lettres(a[i],b[i])
	d=d+ max(len(a),len(b)) - min(len(a),len(b))
	return(d)
#fonction indicateur d'égalité peut être écrite en retu
def indic(a,b):
	return(a!=b)
#Distance entre 2 mots par fonction de levenshtein
def distance_mots_LD(a,b):
	i=len(a)-1
	j=len(b)-1
	if min(i,j)==0 :
		return(max(i,j))
	elif (i>1 and j>1 and a[i]==b[j-1] and a[i-1]==b[j]):
		return(min(distance_mots_LD(a[0:i],b)+1,distance_mots_LD(a[0:i],b[0:j])+indic(a[i],b[j]),distance_mots_LD(b[0:i],a)+1, distance_mots_LD(a[0:i-1],b[0:j-1])))
	else:
		return( min(distance_mots_LD(a[0:i],b)+1,distance_mots_LD(a[0:i],b[0:j])+indic(a[i],b[j]),distance_mots_LD(b[0:i],a)+1)	)
 # Fonction prédéfinie python qui donne la distance aussi ( pour l'instant la plus effective)
def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
