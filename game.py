#import sys      #to get the argument in the terminal python mvp.py var1 var2 var3
import random
from random import randint

import tmdbsimple as tmdb
tmdb.API_KEY = '6145823fab96263074a06f65d932162d'


top_actor = []

def get_acteur_e_liste():
	with open("actor.txt", "r") as ins:
		for line in ins:
			top_actor.append(line)
	with open("actress.txt", "r") as ins :
		for line in ins :
			top_actor.append(line)
			
#obtenir la liste des acteurs de ce film, cette fonction appelle pas IMDB
def get_acteur_list(movie):
	acteur = []
	if movie:
		cast = movie.get('cast')
		for actor in cast:
			acteur.append(actor['name'])
	return acteur

def get_movie_list(top) :
	#movies_id = []
	if len(top_actor) <= 1:
		get_acteur_e_liste()
	indice = randint(0,top-1) 
	#print indice
	#print len(top_actor)
	global actor_nom
	actor_nom = top_actor[indice]
	search = tmdb.Search()
	actor1 = search.person(query=actor_nom)
	#print len(actor1)
	while not actor1:
		actor1 = search.person(query=actor_nom)
	#print "search results: "
	#print len(actor1)
	actor_id = search.results[0]['id']
	actor = tmdb.People(actor_id)
	if not actor :
		return get_movie_list(top)
	movies_list = actor.movie_credits()
	if movies_list == None :
		return get_movie_list(top)
	if ( len(movies_list['cast']) < 2) :
		return get_movie_list(top)
	# list1 = get_acteur_list(movies_list[0])
	#for i in movies_list['cast']:
	#	movies_id.append(i.movieID)
	(film1, film2) = random.sample(movies_list['cast'] , 2) 
	#film1 = ia.get_movie(film1id)
	#film2 = ia.get_movie(film2id)
	# print film1['title']
	# print film2['title']
	return (actor,film1,film2)

def question(film1,film2,top,nom_acteur):
	option_list = []
	actors = []
	for i in range(4):
		indice = randint(0,top-1) 
		# print 'indice: ' 
		# print indice
		actors.append(top_actor[indice])
	option_a = nom_acteur
	answer = nom_acteur
	option_b = actors[1]
	option_c = actors[2]
	option_d = actors[3]
	option_list.append(option_a)
	option_list.append(option_b)
	option_list.append(option_c)
	option_list.append(option_d)
	random.shuffle(option_list)  
	return (film1, film2, option_list, answer)

def get_acteur_commun(acteur_list1, acteur_list2):
	return list(set(acteur_list1) & set(acteur_list2))

def get_cover(film):
	# movie = ia.search_movie(MovieName)[0]
	# movie = ia.get_movie(movie.movieID)
	if film['poster_path']:
		return 'http://image.tmdb.org/t/p/w185/'+ film['poster_path']
	return 0

def main(top):
	top = int(top)
	(actor,film1,film2) = get_movie_list(top)
	q = question(film1,film2,top,actor_nom)
	
	return (q[0], q[1], q[2], q[3])#(film1, film2, option_list, answer)

